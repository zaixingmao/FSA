#!/usr/bin/env python
import os
import optparse
import localJob_cfg

def expandFinalStates(FS):
    return [x.strip() for x in FS.split(',')]

def getSamples(sample):
    samples = " "
    for x in sample.split(','):
        samples += "\""
        samples += x
        samples += "\" "
    return samples

def subsitute(command, option, newSetting):
    if command.find(option) == -1:
        return command
    startPosition = command.find(option)+len(option)
    output = command[0:startPosition]
    output += newSetting
    tmpString = command[startPosition:]
    output += tmpString[tmpString.find(" "):]
    return output

def opts():
    parser = optparse.OptionParser()
    parser.add_option("--local", dest="runLocal", default=False, action="store_true", help="run local jobs")
    parser.add_option("--doMVAMET", dest="doMVAMET", default=False, action="store_true", help="do MVAMET")
    parser.add_option("--doTauTauMVAMET", dest="doTauTauMVAMET", default=False, action="store_true", help="do Jan's MVAMET")
    parser.add_option("--singleJob", dest="singleJob", default=False, action="store_true", help="run 1 job")
    parser.add_option("--resubmit-dir", dest="resubmitDir", default='', help="resubmit failed jobs dir")
    parser.add_option("--nJobs", dest="nJobs", default=9999, help="run n job")
    parser.add_option("-o", dest="name", default='SYNC_745', help="name of output dir")
    parser.add_option("--sample", dest="sample", default='SUSY', help="sample name VBF, SUSY")
    parser.add_option("--memory", dest="memory", default=False, action="store_true", help="profile memory usage (igprof mp)")
    parser.add_option("--cpu", dest="cpu", default=False, action="store_true", help="profile CPU usage (igprof pp)")
    parser.add_option("--FS", dest="FS", default='tt', help="final state: tt, et, mt, em")
    parser.add_option("--isData", dest="isData", default=False, action="store_true", help="run over data")
    parser.add_option("--is50ns", dest="is50ns", default=False, action="store_true", help="run over 50ns sample")
    parser.add_option("--TNT", dest="TNT", default=False, action="store_true", help="store TNT stuff")
    parser.add_option("--notFromDAS", dest="notFromDAS", default=False, action="store_true", help="submit files defined in data13TeV.py")
    parser.add_option("--atFNAL", dest="atFNAL", default=False, action="store_true", help="at fnal")
    parser.add_option("--resubmit", dest="resubmit", default=False, action="store_true", help="at fnal")
    parser.add_option("--maxEvents", dest="maxEvents", default=-1, help="max events to run over")
    parser.add_option("--directQuery", dest="directQuery", default=False, action="store_true", help="at fnal")
    parser.add_option("--newXROOTD", dest="newXROOTD", default="", help="run over data")
    parser.add_option("--sys", dest="sys", default="", help="jetEC, jetBTag, tauEC")

    options, args = parser.parse_args()

    return options

options = opts()


def writeSubmitTemplate(command, options):
    template_location = "%s/template.submit" %(os.path.dirname(os.path.realpath(__file__)))
    f_tmp = open(template_location,'w')
    command = command[command.find('channels'): ]
    if options.maxEvents != -1:
        command = ('maxEvents=%s %s' %(options.maxEvents, command))
    f_tmp.write(command)
    f_tmp.close()
    return template_location

if options.singleJob:
    nJobs = "1"
else:
    nJobs = options.nJobs

resubmitDir = options.resubmitDir
if resubmitDir != '':
    if resubmitDir[len(resubmitDir)-1] == "/":
        resubmitDir = resubmitDir[0:resubmitDir[len(resubmitDir)-1]]

if resubmitDir != '':
    print 'moving previous log file to %s_old' %resubmitDir
    os.system("mv %s %s_old" %(resubmitDir, resubmitDir))
    os.system("ls %s" %(resubmitDir[:resubmitDir.rfind('/')]))

skimCuts = {}
skimCuts['tt'] = {"ID_t": "object.tauID(\\\"decayModeFindingNewDMs\\\") > 0.5",
                 "Pt_t": "object.pt() > 25",
                  "Eta_t": "abs(object.eta()) < 2.1",
                  }
skimCuts['et'] = {# "ID_e": "object.userFloat(\'MVANonTrigWP80\')> 0.5",
                  "Pt_e": "object.pt() > 25",
                  "Eta_e": "abs(object.eta()) < 2.1",
                  "ID_t": "object.tauID(\\\"decayModeFindingNewDMs\\\") > 0.5",
                  "decayMode_t": "object.decayMode() < 4 || object.decayMode() > 8",
                  "Pt_t": "object.pt() > 18",
                  "Eta_t": "abs(object.eta()) < 2.1",
                  }
skimCuts['em'] = {
                  "Pt_e": "object.pt() > 13",
                  "Eta_e": "abs(object.eta()) < 2.5",
                  "ID_m": "object.userInt(\\\"ShortTermMediumID\\\") > 0.5",
                  "Pt_m": "object.pt() > 10",
                  "Eta_m": "abs(object.eta()) < 2.4",
                  }
skimCuts['mm'] = {"Pt": "object.pt() > 10",
                  "ID": "object.isMediumMuon() > 0.5",
                  "Eta": "abs(object.eta()) < 2.4",
                  }

skimCuts['mt'] = {"ID_m": "object.userInt(\\\"ShortTermMediumID\\\") > 0.5",
                  "Pt_m": "object.pt() > 25",
                  "Eta_m": "abs(object.eta()) < 2.1",
                  "ID_t": "object.tauID(\\\"decayModeFindingNewDMs\\\") > 0.5",
                  "decayMode_t": "object.decayMode() < 4 || object.decayMode() > 8",
                  "Pt_t": "object.pt() > 18",
                  "Eta_t": "abs(object.eta()) < 2.1",
                  }
skimCuts['ee'] = {"Pt": "object.pt() > 13",
                  "Eta": "abs(object.eta()) < 2.1",
                  }
skimCuts['emtt'] = {
                  "Pt_e": "object.pt() > 13",
                  "Eta_e": "abs(object.eta()) < 2.5",
                  "ID_m": "object.isMediumMuon() > 0.5",
                  "Pt_m": "object.pt() > 10",
                  "Eta_m": "abs(object.eta()) < 2.4",
                  "ID_t": "object.tauID(\\\"decayModeFindingNewDMs\\\") > 0.5",
                  "Pt_t": "object.pt() > 25",
                  "Eta_t": "abs(object.eta()) < 2.1",
                  }
skimCuts['tttt'] = {"ID_t": "object.tauID(\\\"decayModeFindingNewDMs\\\") > 0.5",
                    "Pt_t": "object.pt() > 25",
                    "Eta_t": "abs(object.eta()) < 2.1",
                    }



MVAMET = 1 if options.doMVAMET else 0
TauTauMVAMET = 1 if options.doTauTauMVAMET else 0
isMC = 0 if options.isData else 1
TNT = 1 if options.TNT else 0


# useLumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-258750_13TeV_PromptReco_Collisions15_25ns_JSON.txt' if options.isData else ''
useLumiMask = 'json/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt' if options.isData else ''
localJobInfo = localJob_cfg.localJobInfo

inputFiles = localJobInfo['inputFile']
outputFile = localJobInfo['outputFile']
outputFile = './localRunOutputs/%s' %outputFile

if ":" in localJobInfo['eventsToProcess']:
    cmd = './make_ntuples_cfg.py eventsToProcess=%s outputFile=%s inputFiles=%s channels=%s isMC=%i TNT=%i lumiMask=%s nExtraJets=8 sys=%s runMVAMET=%i runTauTauMVAMET=%i ' %(localJobInfo['eventsToProcess'], outputFile, inputFiles, options.FS, isMC, TNT, useLumiMask, options.sys, MVAMET, TauTauMVAMET)

else:
    cmd = './make_ntuples_cfg.py maxEvents=%i outputFile=%s inputFiles=%s channels=%s isMC=%i TNT=%i lumiMask=%s nExtraJets=8 sys=%s runMVAMET=%i runTauTauMVAMET=%i ' %(localJobInfo['maxEvents'], outputFile, inputFiles, options.FS, isMC, TNT, useLumiMask, options.sys, MVAMET, TauTauMVAMET)

if options.memory:
    checkCmd = 'igprof -d -mp -z -o igprof.mp.gz  cmsRun '#"valgrind --tool=memcheck `cmsvgsupp` --leak-check=yes --show-reachable=yes --num-callers=20 --track-fds=yes cmsRun "
    cmd =  checkCmd + cmd
elif options.cpu:
    checkCmd = 'igprof -d -pp -z -o igprof.pp.gz  cmsRun '
    cmd =  checkCmd + cmd

fs = expandFinalStates(options.FS)

cuts = " "
for iFS in fs:
    if iFS in skimCuts.keys():    
        cuts += "skimCuts-%s=\"" %iFS
        for ikey in skimCuts[iFS].keys():
            for iLeg in range(len(iFS)):
                if '_%s' %iFS[iLeg] in ikey:
                    cuts+= "%s," %(skimCuts[iFS][ikey].replace("object", "daughter(%i)" %iLeg))
        cuts = cuts[0: len(cuts)-1] + "\" "

cmd += cuts

if options.atFNAL:
    submit_script = "submit_job_fnal.py"
else:
    submit_script = "submit_job.py"


template_location = writeSubmitTemplate(cmd, options)

if not options.runLocal:
    samples = getSamples(options.sample)
    tempFile = "do_test.sh"
    outFile = "do.sh"
    sys = "sys=%s" %options.sys
    if options.sys == '':
        sys = ""
    cmd = "%s %s make_ntuples_cfg.py channels=\"%s\" isMC=%i  TNT=%i lumiMask=%s nExtraJets=8 %s runMVAMET=%i runTauTauMVAMET=%i" %(submit_script, options.name, options.FS, isMC, TNT, useLumiMask, sys, MVAMET, TauTauMVAMET)
    if options.is50ns:
        cmd += ' use25ns=0'
    else:
        cmd += ' use25ns=1'

    if options.atFNAL:
        if options.resubmit:
            cmd += " --resubmit-failed-jobs "
        if nJobs != 9999:
            cmd += " --nJobs %s " %nJobs
    if options.directQuery:
        cmd += " --directQuery"

    cmd += " --comand-template=%s" %template_location
    if isMC:
        cmd += " --das-replace-tuple=$fsa/MetaData/tuples/MiniAOD-13TeV_RunIISummer16MiniAODv2.json --samples %s -o %s" %(samples, tempFile)
        if not options.notFromDAS:
            if options.is50ns:
                cmd += " --campaign-tag=\"RunIISpring15DR74-Asympt50ns*\" "
            else:
                if "DYJetsToLL_M-50" in options.sample:
                    cmd += " --campaign-tag=\"RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2\" "
                elif "DY" in options.sample:
                    cmd += " --campaign-tag=\"RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext*\" "
                elif ("TT_LO" in options.sample) or ("ZPrime" in options.sample) or ("WZTo2L2Q" in options.sample):
                    cmd += " --campaign-tag=\"RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1\" "
                elif "ST_tW" in options.sample or "VV" in options.sample or "WZTo2L2Q" in options.sample or "WJetsToLNu_HT-400to600" in options.sample:
                    cmd += " --campaign-tag=\"RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1\" "
                elif ("WJetsToLNu_HT-200to400" in options.sample) or ("WJetsToLNu_HT-100to200" in options.sample) or ("WJetsToLNu_LO" in options.sample):
                    cmd += " --campaign-tag=\"RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1\" "
                else:
                    cmd += " --campaign-tag=\"RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v3\" "

        else:
            cmd += " --input-dir=/nfs_scratch/zmao/"
    else:
        cmd += " --data --das-replace-tuple=$fsa/MetaData/tuples/MiniAOD-13TeV_Data.json --samples %s -o %s" %(samples, tempFile)

if options.memory:
#     cmd += ">& vglog.out &"
    cmd += " >& igtest.mp.log &"
    print cmd
elif options.cpu:
    cmd += " >& igtest.pp.log &"
    print cmd
else:
    print "Running command:"
    print cmd
    os.system(cmd)

if (not options.runLocal) and (not options.atFNAL):
    lines = open(tempFile, "r").readlines()
    output = open(outFile, "w")

    for i in range(0, len(lines)):
        currentLine = lines[i]
        if currentLine.find("runTauTauMVAMET") != -1 and currentLine.find("farmoutAnalysisJobs") != -1:
            newLine = currentLine[0:currentLine.find("farmoutAnalysisJobs")]
            newLine += "farmoutAnalysisJobs "
            if nJobs != 9999:
                newLine += "--job-count=%s " %nJobs
            newLine += "--assume-input-files-exist --vsize-limit=8000 --memory-requirements=8000 "
            newLine += currentLine[currentLine.find("farmoutAnalysisJobs") + 19:currentLine.find("\"--output-dag-file")]
            if resubmitDir != '':
                newLine += "--resubmit-failed-jobs "
            else:
                newLine += currentLine[currentLine.find("\"--output-dag-file"):currentLine.find("\"--output-dir=")]

            newLine += currentLine[currentLine.find("\"--output-dir="):currentLine.find("runTauTauMVAMET")]
            newLine += "runTauTauMVAMET=%i %s" %(TauTauMVAMET, cuts)
            newLine += " 'inputFiles=$inputFileNames' 'outputFile=$outputFileName'"
            currentLine = newLine
        currentLine += '\n'
        if options.newXROOTD != "":
            currentLine = subsitute(currentLine, "--input-dir=root://", options.newXROOTD + "/")
        output.writelines(currentLine)
    output.close()
    print 'bash < do.sh'

if options.atFNAL and (not options.runLocal):
    print 'python submit_FNAL_condor.py'


if resubmitDir != '':
    print 'restoring previous log file from %s_old  to %s' %(resubmitDir, resubmitDir)
    os.system("rm -rf %s" %resubmitDir)
    os.system("mv %s_old %s" %(resubmitDir, resubmitDir))

     
