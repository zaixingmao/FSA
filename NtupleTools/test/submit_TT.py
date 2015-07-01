#!/usr/bin/env python
import os


skimCuts = {"ID": "object.tauID(\\\"decayModeFinding\\\") > 0.5 || object.tauID(\\\"decayModeFindingNewDMs\\\") > 0.5",
            "Pt": "object.pt() > 45",
#             "anti-Ele": "object.tauID(\\\"againstElectronVLooseMVA5\\\")>0.5",
#             "anti-Mu": "object.tauID(\\\"againstMuonLoose3\\\")>0.5",
#             "iso": "object.tauID(\\\"byCombinedIsolationDeltaBetaCorrRaw3Hits\\\")<10.0"
            }


cmd = "./make_ntuples_cfg.py eventsToProcess=1:905:90421  outputFile=myTestFile.root useMiniAOD=1 inputFiles=file:///hdfs/store/mc/Phys14DR/VBF_HToTauTau_M-125_13TeV-powheg-pythia6/MINIAODSIM/PU20bx25_tsg_PHYS14_25_V1-v2/00000/CE7A1D9C-9F77-E411-BEB3-00266CF9B184.root channels=tt isMC=1 nExtraJets=10 svFit=0 "
# cmd = "./make_ntuples_cfg.py maxEvents=1000  outputFile=myTestFile.root useMiniAOD=1 inputFiles=file:///hdfs/store/mc/Phys14DR/VBF_HToTauTau_M-125_13TeV-powheg-pythia6/MINIAODSIM/PU20bx25_tsg_PHYS14_25_V1-v2/00000/66E71D9C-9F77-E411-BFE9-00266CF9B184.root channels=tt isMC=1 nExtraJets=6 svFit=0 "

cuts = "skimCuts=\""
for ikey in skimCuts.keys():
    cuts+= "%s," %(skimCuts[ikey].replace("object", "daughter(0)"))
    cuts+= "%s," %(skimCuts[ikey].replace("object", "daughter(1)"))
cuts = cuts[0: len(cuts)-1] + "\""
cmd += cuts
tempFile = "do_test.sh"
outFile = "do.sh"
cmd = "submit_job.py SYNC4 make_ntuples_cfg.py channels=\"tt\" isMC=1 useMiniAOD=1 nExtraJets=8 svFit=0"
cmd += " --campaign-tag=\"Phys14DR-PU20bx25*\" --das-replace-tuple=$fsa/MetaData/tuples/MiniAOD-13TeV.json --samples \"VBF*\" -o %s" %tempFile
os.system(cmd)


lines = open(tempFile, "r").readlines()
output = open(outFile, "w")

for i in range(0, len(lines)):
    currentLine = lines[i]

    if currentLine.find("svFit=1") != -1 and currentLine.find("farmoutAnalysisJobs") != -1:
        currentLine = currentLine[0:currentLine.find("svFit=1")]
        currentLine += "svFit=1 %s" %cuts
        currentLine += "  'inputFiles=$inputFileNames' 'outputFile=$outputFileName'"
    currentLine += '\n'
    print currentLine
    output.writelines(currentLine)
output.close()
