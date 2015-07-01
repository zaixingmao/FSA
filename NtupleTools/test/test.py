#!/usr/bin/env python
import os


skimCuts = {"ID": "object.tauID(\\\"decayModeFinding\\\") > 0.5 || object.tauID(\\\"decayModeFindingNewDMs\\\") > 0.5",
            "Pt": "object.pt() > 45",
            }


cmd = "./make_ntuples_cfg.py maxEvents=1000  outputFile=myTestFile.root useMiniAOD=1 inputFiles=file:///hdfs/store/mc/Phys14DR/VBF_HToTauTau_M-125_13TeV-powheg-pythia6/MINIAODSIM/PU20bx25_tsg_PHYS14_25_V1-v2/10000/6617651C-4977-E411-9156-3417EBE2F493.root channels=tt isMC=1 nExtraJets=6 svFit=0 "

cuts = "skimCuts=\""
for ikey in skimCuts.keys():
    cuts+= "%s," %(skimCuts[ikey].replace("object", "daughter(0)"))
    cuts+= "%s," %(skimCuts[ikey].replace("object", "daughter(1)"))
cuts = cuts[0: len(cuts)-1] + "\""
cmd += cuts
os.system(cmd)
