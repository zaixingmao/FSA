#!/usr/bin/env python

'''

Create a script file to submit jobs to condor using farmoutAnalysisJobs.
(http://www.hep.wisc.edu/cms/comp/faq.html#how-can-i-use-farmoutanalysisjobs...)

By default, the script is written to stdout, with some logging information 
sent to stderr. If --output_file (-o) is specified, a bash script is
created containing the ouput.


Example to make submit script (stored in test.sh) for WZ analysis on Phys14 miniAOD:
(run from $fsa/NtupleTools/test or use full path to make_ntuples_cfg.py)
    
    submit_job.py 2015-02-26-WZ_ntuples_test make_ntuples_cfg.py \
    channels="eee,mmm,eem,emm" isMC=1 --campaign-tag="Phys14DR-PU20bx25_PHYS14_25_V*" \
    --das-replace-tuple=$fsa/MetaData/tuples/MiniAOD-13TeV.json \
    --samples "W*" "Z*" "D*" "T*" \
    -o test.sh

Note: It's a good idea to put your sample names with wildcards inside quotes,
    as otherwise the unix wildcard will be expanded before it is passed to the 
    program (so a file named 'Wsubmit.sh' in your folder would cause the 
    argument W* to become Wsubmit.sh, which you don't want)

'''

import argparse
import datetime
import fnmatch
import json
import logging
import os
import sys
from socket import gethostname
from FinalStateAnalysis.MetaData.datadefs import datadefs
from FinalStateAnalysis.Utilities.dbsinterface import get_das_info

log = logging.getLogger("submit_job")
logging.basicConfig(level=logging.INFO, stream=sys.stderr)

def getFromDataDefs(dataset_name):
    if dataset_name in datadefs.keys():
        return 'root://cmsxrootd.hep.wisc.edu//store/user/zmao/%s' %datadefs[dataset_name]['datasetpath']
    else:
        print "dataset: %s not found!!" %dataset_name
        return ''

def createJobFiles(dir, fileList, script_content):
    f = open(fileList,'r')
    f_template = open(script_content,'r')
    template = f_template.readline()
    relBase = os.environ.get('CMSSW_BASE')
    cmsrel = relBase[relBase.rfind('CMSSW'):]
    for line in f.readlines():
        currentDir = dir[:dir.find("dag")]+line[line.rfind('/')+1:line.rfind('.')]        
        mkdir_cmd = 'mkdir ' + currentDir
        os.system(mkdir_cmd)
        f_submit = open(currentDir + '/submit','w')
        f_submit.write("#!/bin/bash\n")
        f_submit.write("INPUTTAR=%s\n" %cmsrel)
        f_submit.write("OUTDIR=root://cmseos.fnal.gov//store/user/%s/%s\n" %(os.environ['USER'], dir[dir.find("nobackup")+9:dir.find("dags")]))
        f_submit.write("INPUTFILE=root://cmsxrootd.fnal.gov/%s\n" %line)
        f_submit.write("tar -xf ${INPUTTAR}.tar\n")
        f_submit.write("cd ${INPUTTAR}/src\n")
        f_submit.write("export SCRAM_ARCH=slc6_amd64_gcc493\n")
        f_submit.write("scramv1 b ProjectRename\n")
        f_submit.write("cd FinalStateAnalysis\n")
        f_submit.write("source environment.sh \n")
        f_submit.write("cd NtupleTools/test/\n")
        command = "./make_ntuples_cfg.py maxEvents=100 outputFile=make_ntuples_cfg-%s inputFiles=${INPUTFILE} %s" %(line[line.rfind("/")+1:line.find('root') + 4], template[template.find("channels"):])
        f_submit.write(command + '\n')
        f_submit.write("# copy output to eos\n")
        f_submit.write('echo "xrdcp .root output for condor"\n')
        f_submit.write("for FILE in *.root\n")
        f_submit.write("do\n")
        f_submit.write('  echo "xrdcp -f ${FILE} ${OUTDIR}/${FILE}"\n')
        f_submit.write("  xrdcp -f ${FILE} ${OUTDIR}/${FILE} 2>&1 \n")
        f_submit.write("  XRDEXIT=$?\n")
        f_submit.write("  if [[ $XRDEXIT -ne 0 ]]; then\n")
        f_submit.write("    rm *.root\n")
        f_submit.write('    echo "exit code $XRDEXIT, failure in xrdcp"\n')
        f_submit.write("    exit $XRDEXIT\n")
        f_submit.write("  fi\n")
        f_submit.write("  rm ${FILE}\n")
        f_submit.write("done\n")
        f_submit.close()
        sys.stdout.write(".")
    f.close()

def getFarmoutCommand(args, dataset_name, full_dataset_name):
    ''' Builds the command to submit an ntuple job for the given dataset 

    Builds text for a bash script to submit ntuplization jobs to condor
    via FarmoutAnalysisJobs. Recieves the command line input (via the varialbe 
    args), the dataset shortname (dataset_name) and full name with path 
    (full_dataset_name) as input. Creates the directory dag_dir+"inputs", 
    where dag_dir is a command line argument.

    returns text for the bash script
    '''
    uname = os.environ['USER']
    submit_file_list = []
    scratchDir = '/uscms/home/'
    submit_dir = args.subdir.format(
        scratch = scratchDir,
        user = uname,
        jobid = args.jobid,
        sample = dataset_name
    )
    if os.path.exists(submit_dir):
        command = '# Submission directory for %s already exists\n' % dataset_name
        log.warning("Submit directory for sample %s exists, skipping",
                    dataset_name)
        return command

    log.info("Building submit files for sample %s", dataset_name)

    dag_dir = args.dagdir.format(
        scratch = scratchDir,
        user = uname,
        jobid = args.jobid,
        sample = dataset_name
    )

    output_dir = args.outdir.format(
        user = uname,
        jobid = args.jobid,
        sample = dataset_name
    )

    input_commands = []
    if args.fromDAS or args.isData or args.campaignstring:
        files = get_das_info('file dataset=%s' % full_dataset_name)
        mkdir_cmd = "mkdir -p %s" % (dag_dir+"inputs")
        os.system(mkdir_cmd)
        input_txt = '%s_inputfiles.txt' % dataset_name
        input_txt_path = os.path.join(dag_dir+"inputs", input_txt)
        with open(input_txt_path, 'w') as txt:
            txt.write('\n'.join(files))
        input_commands.extend([
                '--input-file-list=%s' % input_txt_path,
                '--assume-input-files-exist', 
                '--input-dir=root://cmsxrootd.fnal.gov/',
        ])
    else:
        input_commands.extend([
                '--assume-input-files-exist',
                '--input-dir=%s' %getFromDataDefs(dataset_name),
        ])
    command = [
        'farmoutAnalysisJobs',
        '--infer-cmssw-path',
        '"--submit-dir=%s"' % submit_dir,
        '"--output-dag-file=%s"' % dag_dir,
        '"--output-dir=%s"' % output_dir,
        '--input-files-per-job=%i' % args.filesperjob,
    ]
    if args.extraUserCodeFiles:
        command.append('--extra-usercode-files="%s"'%(' '.join(args.extraUserCodeFiles)))
    if args.sharedfs:
        command.append('--shared-fs')
    command.extend(input_commands)
    command.extend([
        # The job ID
        '%s-%s' % (args.jobid, dataset_name),
        args.cfg
    ])

    command.extend(args.cmsargs)
    command.append("'inputFiles=$inputFileNames'")
    command.append("'outputFile=$outputFileName'")

    # temp hardcode
    #if args.apply_cms_lumimask:
    #    filename = 'Cert_246908-254349_13TeV_PromptReco_Collisions15_JSON.txt'
    #    lumi_mask_path = os.path.join('/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV',filename)
    #    command.append('lumiMask=%s' % lumi_mask_path)

    #if args.apply_cms_lumimask and 'lumi_mask' in sample_info:
    #    lumi_mask_path = os.path.join(
    #        os.environ['CMSSW_BASE'], 'src', sample_info['lumi_mask'])
    #    command.append('lumiMask=%s' % lumi_mask_path)
    #    firstRun = sample_info.get('firstRun', -1)
    #    if firstRun > 0:
    #        command.append('firstRun=%i' % firstRun)
    #    lastRun = sample_info.get('lastRun', -1)
    #    if lastRun > 0:
    #        command.append('lastRun=%i' % lastRun)

    farmout_command = '# Submit file for sample %s\n' % dataset_name
    farmout_command += 'mkdir -p %s\n' % os.path.dirname(dag_dir)
    farmout_command += ' '.join(command) + '\n'
    createJobFiles(dag_dir, input_txt_path, args.command_template)

    for ifile in files:
        submit_file_list.append(dag_dir[:dag_dir.rfind('dags')] + ifile[ifile.rfind("/")+1: ifile.rfind(".")])
    return farmout_command, submit_file_list

def datasets_from_das(args):
    ''' Build submit script using datasets from DAS

    Builds text for a bash script to submit ntuplization jobs to condor
    via FarmoutAnalysisJobs. Recieves the command line input (via the varialbe 
    args) as input. The MINIAOD file to be ntuplized is found by searching for 
    files in DAS matching args.samples in the campaign args.campaignstring. If 
    args.dastuple is specified (a json file), this is used as a simpler lookup 
    method rather than searching through all of DAS. 

    If a submit folder already exists with the same name, it will not be
    recreated. A warning is written to the submit script.

    returns a string containing the text of the bash submit script.

    '''
    fileList = []
    script_content = ""
    # this part searches for MC
    if args.campaignstring:
        dbs_datasets = get_das_info('/*/%s/MINIAODSIM' % args.campaignstring)
        # check sample wildcards
        for dataset in dbs_datasets:
            dataset_name = dataset.split('/')[1] 
            passes_filter = True
            passes_wildcard = False
            for pattern in args.samples:
                if args.dastuple: # check json for shorthand
                    with open(args.dastuple) as tuple_file:
                        tuple_info = json.load(tuple_file)
                        matching_datasets = []
                        for shorthand, fullname in tuple_info.iteritems():
                            if fullname in dataset_name:
                                if fnmatch.fnmatchcase(shorthand, pattern):
                                    passes_wildcard = True
                else: # check das directly
                    if fnmatch.fnmatchcase(dataset_name, pattern):
                        passes_wildcard = True
            passes_filter = passes_wildcard and passes_filter
            if passes_filter:
                tmp_content, tmp_file_list= getFarmoutCommand(args, dataset_name, dataset)
                script_content += tmp_content
                fileList += tmp_file_list
    # special handling for data
    if args.isData:
        data_patterns = [x for x in args.samples if 'data_' in x]
        data_datasets = get_das_info('/*/*/MINIAOD')
        for dataset in data_datasets:
            passes_filter = True
            passes_wildcard = False
            name_to_use = 'data_' + '_'.join(dataset.split('/'))
            for pattern in data_patterns:
                if args.dastuple: # check json for shorthand, links to full dataset name
                    with open(args.dastuple) as tuple_file:
                        tuple_info = json.load(tuple_file)
                        matching_datasets = []
                        for shorthand, fullname in tuple_info.iteritems():
                            if fullname in dataset:
                                if fnmatch.fnmatchcase(shorthand, pattern):
                                    passes_wildcard = True
                                    name_to_use = shorthand
                else: # check das directly
                    if fnmatch.fnmatchcase(dataset, pattern):
                        passes_wildcard = True
            passes_filter = passes_wildcard and passes_filter
            if passes_filter:
                tmp_content, tmp_file_list= getFarmoutCommand(args, name_to_use, dataset)
                script_content += tmp_content
                fileList += tmp_file_list
    if "Submit file" not in script_content:
        log.warning("No datasets found matching %s", args.samples)

    input_txt_path = "%s/submit_files.txt" %os.getcwd()
    with open(input_txt_path, 'w') as txt:
        txt.write('\n'.join(fileList))

    return script_content

def datasets_from_datadefs(args):
    script_content = ''
    for pattern in args.samples:
        script_content += getFarmoutCommand(args, pattern, '')
    return script_content

def get_com_line_args():
    parser = argparse.ArgumentParser()

    cmsrun_group = parser.add_argument_group('Analysis and cmsRun options')

    cmsrun_group.add_argument('jobid', type=str,
                        help='String description of job')

    cmsrun_group.add_argument('cfg', type=str, help='Config file to run')

    cmsrun_group.add_argument(
        'cmsargs', metavar='arg', nargs='*',
        help = 'VarParsing arguments passed to cmsRun.'
        ' Note that inputFiles and outputFiles are always passed.'
    )

    cmsrun_group.add_argument(
        '--apply-cmsRun-lumimask', dest='apply_cms_lumimask',
        action='store_true', help = 'If specified, pass the appropriate '
        'lumiMask=XXX.json and firstRun etc to cmsRun'
    )
    cmsrun_group.add_argument(
        '--das-replace-tuple', dest='dastuple',
         help = 'JSON file listing shorthand names for DAS samples.'
    )

    input_group = parser.add_mutually_exclusive_group(required=True)

    input_group.add_argument(
        '--input-dir', dest='inputdir',
        help = 'Input dir argument passed to farmout.'
    )
    input_group.add_argument(
        '--campaign-tag', dest='campaignstring',
        help = 'DAS production campaign string for query.'
               ' For a given DAS query, it is the second part'
               ' (dataset=/*/[campaign-tag]/MINIAODSIM).'
    )
    input_group.add_argument(
        '--data', dest='isData', action='store_true',
        help = 'Run over data',
    )
    input_group.add_argument(
        '--fromDAS', dest='fromDAS', action='store_true',
        help = 'get info from DAS',
    )

    filter_group = parser.add_argument_group('Sample Filters')
    filter_group.add_argument('--samples', nargs='+', type=str, required=False,
                        help='Filter samples using list of patterns (shell style)')

    farmout_group = parser.add_argument_group("farmout",
                                              description="Farmout options")

    farmout_group.add_argument(
        '--extra-usercode-files', nargs='*', type=str, dest='extraUserCodeFiles',
        help = 'Space-separated list of extra directories that need to be included '
               'in the user_code tarball sent with the job. Paths relative to $CMSSW_BASE.'
    )

    farmout_group.add_argument(
        '--output-dag-file', dest='dagdir',
        default='/{scratch}/{user}/nobackup/{jobid}/{sample}/dags/dag',
        help = 'Where to put dag files',
    )

    farmout_group.add_argument(
        '--shared-fs', dest='sharedfs', action='store_true',
        help = 'Use only nodes with access to AFS',
    )

    farmout_group.add_argument(
        '--submit-dir', dest='subdir',
        default='/{scratch}/{user}/{jobid}/{sample}/submit',
        help = 'Where to put submit files. Default: %s(default)s',
    )

    farmout_group.add_argument(
        '--output-dir', dest='outdir',
        default='srm://cmssrm.hep.wisc.edu:8443/srm/v2/server?SFN=/hdfs/store/user/{user}/{jobid}/{sample}/',
        help = 'Where to put the output.  Default: %(default)s'
    )

    farmout_group.add_argument('--input-files-per-job', type=int, dest='filesperjob',
                        default=1, help='Files per job')

    parser.add_argument('--output_file', '-o', type=str, default="",
                        required=False, help="Create bash script OUTPUT_FILE file with ouput "
                        "rather than printing information to stdout")

    parser.add_argument('--comand-template', '-t', type=str, default="",
                        dest='command_template', help="commands")

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    script_content = '# Condor submission script\n'
    script_content += '# Generated with submit_job.py at %s\n' % datetime.datetime.now()
    script_content += '# The command was: %s\n\n' % ' '.join(sys.argv)
    args = get_com_line_args()
    # first, make DAS query for dataset if not using local dataset or hdfs/dbs tuple list
    if args.campaignstring or args.isData:
        script_content += datasets_from_das(args)
        print script_content
    else:
        # this is the old version that uses datadefs
        script_content += datasets_from_datadefs(args)


    thisDir = os.getcwd()
    relBase = os.environ.get ('CMSSW_BASE')
    print relBase
    tarfile = ('/uscms/home/%s/nobackup/%s' %(os.environ['USER'], relBase[relBase.rfind('CMSSW'):]))+'.tar'

    if os.path.exists(tarfile):
            os.system("rm %s" %tarfile)

    os.chdir(relBase)
    os.chdir('../')
    print 'tar -cf',tarfile,' ',relBase.split('/')[-1],'/'
    os.system('tar -cf '+tarfile+' '+relBase.split('/')[-1])
    os.chdir(thisDir)

#     if args.output_file == "":
#         sys.stdout.write(script_content)
#     else:
#         with open(args.output_file, "w") as file:
#             file.write("#!/bin/bash\n")
#             file.write(script_content)
#         sys.stdout.write("\nWrote submit script %s\n\n" % args.output_file)
