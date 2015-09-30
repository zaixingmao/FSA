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
    parser.add_option("--doSVFit", dest="doSVFit", default=False, action="store_true", help="do SVFit")
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

    parser.add_option("--newXROOTD", dest="newXROOTD", default="", help="run over data")

    options, args = parser.parse_args()

    return options

options = opts()

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

skimCuts = {}
skimCuts['tt'] = {"ID": "object.tauID(\\\"decayModeFindingNewDMs\\\") > 0.5",
                 "Pt": "object.pt() > 45",
                  "Eta": "abs(object.eta()) < 2.1",
                  }
skimCuts['et'] = {# "ID_e": "object.userFloat(\'MVANonTrigWP80\')> 0.5",
                  "Pt_e": "object.pt() > 23",
                  "Eta_e": "abs(object.eta()) < 2.1",
                  "ID_t": "object.tauID(\\\"decayModeFindingNewDMs\\\") > 0.5",
                  "Pt_t": "object.pt() > 20",
                  "Eta_t": "abs(object.eta()) < 2.3",
                  }
skimCuts['em'] = {# "ID_e": "object.userFloat(\'MVANonTrigWP80\')> 0.5",
                  "Pt_e": "object.pt() > 13",
                  "Eta_e": "abs(object.eta()) < 2.5",
                  "ID_m": "object.isMediumMuon() > 0.5",
                  "Pt_m": "object.pt() > 10",
                  "Eta_m": "abs(object.eta()) < 2.4",
                  }
skimCuts['mt'] = {"ID_m": "object.isMediumMuon() > 0.5",
                  "Pt_m": "object.pt() > 18",
                  "Eta_m": "abs(object.eta()) < 2.1",
                  "ID_t": "object.tauID(\\\"decayModeFindingNewDMs\\\") > 0.5",
                  "Pt_t": "object.pt() > 20",
                  "Eta_t": "abs(object.eta()) < 2.3",
                  }
skimCuts['ee'] = {"Pt": "object.pt() > 13",
                  "Eta": "abs(object.eta()) < 2.1",
                  }

SVFit = 1 if options.doSVFit else 0
MVAMET = 1 if options.doMVAMET else 0
TauTauMVAMET = 1 if options.doTauTauMVAMET else 0
isMC = 0 if options.isData else 1
TNT = 1 if options.TNT else 0

#useLumiMask =  '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-254349_13TeV_PromptReco_Collisions15_JSON.txt' if options.isData else ''
useLumiMask =  '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-256869_13TeV_PromptReco_Collisions15_25ns_JSON.txt' if options.isData else ''
localJobInfo = localJob_cfg.localJobInfo

samples = getSamples(options.sample)

if ":" in localJobInfo['eventsToProcess']:
    cmd = "./make_ntuples_cfg.py eventsToProcess=%s outputFile=myTestFile.root inputFiles=%s channels=%s isMC=%i TNT=%i lumiMask=%s nExtraJets=8 runMVAMET=%i runTauTauMVAMET=%i svFit=%i " %(localJobInfo['eventsToProcess'], localJobInfo['inputFile'], options.FS, isMC, TNT, useLumiMask, MVAMET, TauTauMVAMET, SVFit)
else:
    cmd = "./make_ntuples_cfg.py maxEvents=%i outputFile=myTestFile.root inputFiles=%s channels=%s isMC=%i TNT=%i lumiMask=%s nExtraJets=8 runMVAMET=%i runTauTauMVAMET=%i svFit=%i " %(localJobInfo['maxEvents'], localJobInfo['inputFile'], options.FS, isMC, TNT, useLumiMask, MVAMET, TauTauMVAMET, SVFit)

if options.memory:
    checkCmd = 'igprof -d -mp -z -o igprof.mp.gz  cmsRun '#"valgrind --tool=memcheck `cmsvgsupp` --leak-check=yes --show-reachable=yes --num-callers=20 --track-fds=yes cmsRun "
    cmd =  checkCmd + cmd
elif options.cpu:
    checkCmd = 'igprof -d -pp -z -o igprof.pp.gz  cmsRun '
    cmd =  checkCmd + cmd

fs = expandFinalStates(options.FS)

cuts = " "
for iFS in fs:
    cuts += "skimCuts-%s=\"" %iFS
    if iFS == 'tt' or iFS == 'ee':
        for ikey in skimCuts[iFS].keys():
            cuts+= "%s," %(skimCuts[iFS][ikey].replace("object", "daughter(0)"))
            cuts+= "%s," %(skimCuts[iFS][ikey].replace("object", "daughter(1)"))
    else:
        for ikey in skimCuts[iFS].keys():
            if '_%s' %iFS[0] in ikey:
                cuts+= "%s," %(skimCuts[iFS][ikey].replace("object", "daughter(0)"))
            if '_%s' %iFS[1] in ikey:
                cuts+= "%s," %(skimCuts[iFS][ikey].replace("object", "daughter(1)"))
    cuts = cuts[0: len(cuts)-1] + "\" "
cmd += cuts

if not options.runLocal:
    tempFile = "do_test.sh"
    outFile = "do.sh"
    cmd = "submit_job.py %s make_ntuples_cfg.py channels=\"%s\" isMC=%i  TNT=%i lumiMask=%s nExtraJets=8 runMVAMET=%i runTauTauMVAMET=%i svFit=%i" %(options.name, options.FS, isMC, TNT, useLumiMask,MVAMET, TauTauMVAMET, SVFit)
    if options.is50ns:
        cmd += ' use25ns=0'
    else:
        cmd += ' use25ns=1'

    if isMC:
        if options.is50ns:
            cmd += " --campaign-tag=\"RunIISpring15DR74-Asympt50ns*\" --das-replace-tuple=$fsa/MetaData/tuples/MiniAOD-13TeV_RunIISpring15DR74.json --samples %s -o %s" %(samples, tempFile)
        else:
            cmd += " --campaign-tag=\"RunIISpring15DR74-Asympt25ns*\" --das-replace-tuple=$fsa/MetaData/tuples/MiniAOD-13TeV_RunIISpring15DR74.json --samples %s -o %s" %(samples, tempFile)
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
    os.system(cmd)

if not options.runLocal:
    lines = open(tempFile, "r").readlines()
    output = open(outFile, "w")

    for i in range(0, len(lines)):
        currentLine = lines[i]
        if currentLine.find("svFit") != -1 and currentLine.find("farmoutAnalysisJobs") != -1:
            newLine = currentLine[0:currentLine.find("farmoutAnalysisJobs")]
            newLine += "farmoutAnalysisJobs "
            if nJobs != 9999:
                newLine += "--job-count=%s " %nJobs
            newLine += "--assume-input-files-exist --vsize-limit=8000 "
            newLine += currentLine[currentLine.find("farmoutAnalysisJobs") + 19:currentLine.find("\"--output-dag-file")]
            if resubmitDir != '':
                newLine += "--resubmit-failed-jobs "
            else:
                newLine += currentLine[currentLine.find("\"--output-dag-file"):currentLine.find("\"--output-dir=")]

            newLine += currentLine[currentLine.find("\"--output-dir="):currentLine.find("svFit")]
            newLine += "svFit=%i %s" %(SVFit, cuts)
            newLine += " 'inputFiles=$inputFileNames' 'outputFile=$outputFileName'"
            currentLine = newLine
        currentLine += '\n'
        if options.newXROOTD != "":
            currentLine = subsitute(currentLine, "--input-dir=root://", options.newXROOTD + "/")
        output.writelines(currentLine)
    output.close()
    print 'bash < do.sh'

if resubmitDir != '':
    print 'restoring previous log file from %s_old  to %s' %(resubmitDir, resubmitDir)
    os.system("rm -rf %s" %resubmitDir)
    os.system("mv %s_old %s" %(resubmitDir, resubmitDir))

     
