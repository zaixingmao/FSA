#!/usr/bin/env python
import os
import optparse


def opts():
    parser = optparse.OptionParser()
    parser.add_option("--local", dest="runLocal", default=False, action="store_true", help="run local jobs")
    parser.add_option("--doSVFit", dest="doSVFit", default=False, action="store_true", help="do SVFit")
    parser.add_option("--singleJob", dest="singleJob", default=False, action="store_true", help="run 1 job")
    parser.add_option("-o", dest="name", default='SYNC_745', help="name of output dir")
    parser.add_option("--sample", dest="sample", default='SUSY', help="sample name VBF, SUSY")

    options, args = parser.parse_args()

    return options

options = opts()

skimCuts = {"ID": "object.tauID(\\\"decayModeFinding\\\") > 0.5 || object.tauID(\\\"decayModeFindingNewDMs\\\") > 0.5",
            "Pt": "object.pt() > 45",
            "Eta": "abs(object.eta()) < 2.1",
#             "anti-Ele": "object.tauID(\\\"againstElectronVLooseMVA5\\\")>0.5",
#             "anti-Mu": "object.tauID(\\\"againstMuonLoose3\\\")>0.5",
#             "iso": "object.tauID(\\\"byCombinedIsolationDeltaBetaCorrRaw3Hits\\\")<10.0"
            }

localJobInfo = {'inputFile': "file:///hdfs/store/mc/RunIISpring15DR74/SUSYGluGluToBBHToTauTau_M-160_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v2/50000/1A81092B-1A11-E511-B683-002618943849.root",
                'eventsToProcess': 'all',
                'maxEvents': 1000}


SVFit = 1 if options.doSVFit else 0

if ":" in localJobInfo['eventsToProcess']:
    cmd = "./make_ntuples_cfg.py eventsToProcess=%s outputFile=myTestFile.root inputFiles=%s channels=tt isMC=1 nExtraJets=8 svFit=%i " %(localJobInfo['eventsToProcess'], localJobInfo['inputFile'], SVFit)
else:
    cmd = "./make_ntuples_cfg.py maxEvents=%i outputFile=myTestFile.root inputFiles=%s channels=tt isMC=1 nExtraJets=8 svFit=%i " %(localJobInfo['maxEvents'], localJobInfo['inputFile'], SVFit)


cuts = "skimCuts=\""
for ikey in skimCuts.keys():
    cuts+= "%s," %(skimCuts[ikey].replace("object", "daughter(0)"))
    cuts+= "%s," %(skimCuts[ikey].replace("object", "daughter(1)"))
cuts = cuts[0: len(cuts)-1] + "\""
cmd += cuts

if not options.runLocal:
    tempFile = "do_test.sh"
    outFile = "do.sh"
    cmd = "submit_job.py %s make_ntuples_cfg.py channels=\"tt\" isMC=1 nExtraJets=8 svFit=%i" %(options.name, SVFit)
#     cmd += " --campaign-tag=\"RunIISpring15DR74-Asympt25ns*\" --das-replace-tuple=$fsa/MetaData/tuples/MiniAOD-13TeV_RunIISpring15DR74.json --samples \"%s*\" -o %s" %(options.sample, tempFile)
    cmd += " --campaign-tag=\"Phys14DR-PU20bx25*\" --das-replace-tuple=$fsa/MetaData/tuples/MiniAOD-13TeV_PHYS14DR.json --samples \"%s*\" -o %s" %(options.sample, tempFile)
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
