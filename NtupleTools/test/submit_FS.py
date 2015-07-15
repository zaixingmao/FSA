#!/usr/bin/env python
import os
import optparse
import localJob_cfg

def expandFinalStates(FS):
    return [x.strip() for x in FS.split(',')]

def opts():
    parser = optparse.OptionParser()
    parser.add_option("--local", dest="runLocal", default=False, action="store_true", help="run local jobs")
    parser.add_option("--doSVFit", dest="doSVFit", default=False, action="store_true", help="do SVFit")
    parser.add_option("--singleJob", dest="singleJob", default=False, action="store_true", help="run 1 job")
    parser.add_option("-o", dest="name", default='SYNC_745', help="name of output dir")
    parser.add_option("--sample", dest="sample", default='SUSY', help="sample name VBF, SUSY")
    parser.add_option("--memory", dest="memory", default=False, action="store_true", help="profile memory usage (igprof mp)")
    parser.add_option("--cpu", dest="cpu", default=False, action="store_true", help="profile CPU usage (igprof pp)")
    parser.add_option("--FS", dest="FS", default='tt', help="final state: tt, et, mt, em")

    options, args = parser.parse_args()

    return options

options = opts()

skimCuts = {}
skimCuts['tt'] = {"ID": "object.tauID(\\\"decayModeFindingNewDMs\\\") > 0.5",
                  "Pt": "object.pt() > 45",
                  "Eta": "abs(object.eta()) < 2.1",
                  }
skimCuts['et'] = {"ID_e": "object.userFloat(\'MVANonTrigWP80\')> 0.5",
                  "Pt_e": "object.pt() > 23",
                  "Eta_e": "abs(object.eta()) < 2.1",
                  "ID_t": "object.tauID(\\\"decayModeFindingNewDMs\\\") > 0.5",
                  "Pt_t": "object.pt() > 20",
                  "Eta_t": "abs(object.eta()) < 2.3",
                  }
skimCuts['em'] = {"ID_e": "object.userFloat(\'MVANonTrigWP80\')> 0.5",
                  "Pt_e": "object.pt() > 13",
                  "Eta_e": "abs(object.eta()) < 2.5",
                  "ID_m": "object.isMediumMuon() > 0.5",
                  "Pt_m": "object.pt() > 9",
                  "Eta_m": "abs(object.eta()) < 2.4",
                  }
skimCuts['mt'] = {"ID_m": "object.isMediumMuon() > 0.5",
                  "Pt_m": "object.pt() > 18",
                  "Eta_m": "abs(object.eta()) < 2.1",
                  "ID_t": "object.tauID(\\\"decayModeFindingNewDMs\\\") > 0.5",
                  "Pt_t": "object.pt() > 20",
                  "Eta_t": "abs(object.eta()) < 2.3",
                  }

SVFit = 1 if options.doSVFit else 0

localJobInfo = localJob_cfg.localJobInfo

if ":" in localJobInfo['eventsToProcess']:
    cmd = "./make_ntuples_cfg.py eventsToProcess=%s outputFile=myTestFile.root inputFiles=%s channels=%s isMC=1 nExtraJets=8 svFit=%i " %(localJobInfo['eventsToProcess'], localJobInfo['inputFile'], options.FS, SVFit)
else:
    cmd = "./make_ntuples_cfg.py maxEvents=%i outputFile=myTestFile.root inputFiles=%s channels=%s isMC=1 nExtraJets=8 svFit=%i " %(localJobInfo['maxEvents'], localJobInfo['inputFile'], options.FS, SVFit)

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
    if iFS == 'tt':
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
    cmd = "submit_job.py %s make_ntuples_cfg.py channels=\"%s\" isMC=1 nExtraJets=8 svFit=%i" %(options.name, options.FS, SVFit)
    cmd += " --campaign-tag=\"RunIISpring15DR74-Asympt25ns*\" --das-replace-tuple=$fsa/MetaData/tuples/MiniAOD-13TeV_RunIISpring15DR74.json --samples \"%s*\" -o %s" %(options.sample, tempFile)
#     cmd += " --campaign-tag=\"Phys14DR-PU20bx25*\" --das-replace-tuple=$fsa/MetaData/tuples/MiniAOD-13TeV_PHYS14DR.json --samples \"%s*\" -o %s" %(options.sample, tempFile)

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
            if options.singleJob:
                newLine += "--job-count=1 "
            newLine += currentLine[currentLine.find("farmoutAnalysisJobs") + 19:currentLine.find("svFit")]
            newLine += "svFit=%i %s" %(SVFit, cuts)
            newLine += " 'inputFiles=$inputFileNames' 'outputFile=$outputFileName'"
            currentLine = newLine
        currentLine += '\n'
        output.writelines(currentLine)
    output.close()
    print 'bash < do.sh'
