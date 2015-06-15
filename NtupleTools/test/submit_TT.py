#!/usr/bin/env python
import os


skimCuts = {"ID": "object.tauID(\\\"decayModeFinding\\\") > 0.5 || object.tauID(\\\"decayModeFindingNewDMs\\\") > 0.5",
            "anti-Ele": "object.tauID(\\\"againstElectronVLooseMVA5\\\")>0.5",
            "anti-Mu": "object.tauID(\\\"againstMuonLoose3\\\")>0.5",
            "iso": "object.tauID(\\\"byCombinedIsolationDeltaBetaCorrRaw3Hits\\\")<10.0"
            }


cmd = "./make_ntuples_cfg.py maxEvents=1000 outputFile=myTestFile.root useMiniAOD=1 inputFiles=file:/hdfs/store/mc/Phys14DR/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/MINIAODSIM/PU30bx50_PHYS14_25_V1-v1/00000/48D2DDEC-1281-E411-BF3C-002590AC4FEA.root channels=tt isMC=1 nExtraJets=8 svFit=1 "

cuts = "skimCuts=\""
for ikey in skimCuts.keys():
    cuts+= "%s," %(skimCuts[ikey].replace("object", "daughter(0)"))
    cuts+= "%s," %(skimCuts[ikey].replace("object", "daughter(1)"))
cuts = cuts[0: len(cuts)-1] + "\""

tempFile = "do_test.sh"
outFile = "do.sh"
cmd = "submit_job.py MiniAOD_Test make_ntuples_cfg.py channels=\"tt\" isMC=1 nExtraJets=6 svFit=1"
cmd += " --campaign-tag=\"Phys14DR*30*50*\" --das-replace-tuple=$fsa/MetaData/tuples/MiniAOD-13TeV.json --samples \"TTJet*\" -o %s" %tempFile
print cmd
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
#cmd += "\" --campaign-tag=\"Phys14DR-PU20bx25_tsg_PHYS14_25_V*\" --das-replace-tuple=$fsa/MetaData/tuples/MiniAOD-13TeV.json --samples \"VBF*\" -o do_test.sh"
#os.system(cmd)
#print cmd
