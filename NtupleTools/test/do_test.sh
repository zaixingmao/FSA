#!/bin/bash
# Condor submission script
# Generated with submit_job.py at 2015-06-14 20:46:08.007668
# The command was: /nfs_scratch/zmao/miniAOD/bin/slc6_amd64_gcc481/submit_job.py MiniAOD_Test make_ntuples_cfg.py channels=tt isMC=1 nExtraJets=6 svFit=1 --campaign-tag=Phys14DR*30*50* --das-replace-tuple=/nfs_scratch/zmao/miniAOD/src/FinalStateAnalysis//MetaData/tuples/MiniAOD-13TeV.json --samples TTJet* -o do_test.sh

# Submit file for sample TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola
mkdir -p /nfs_scratch/zmao/MiniAOD_Test/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/dags
farmoutAnalysisJobs --infer-cmssw-path "--submit-dir=/nfs_scratch/zmao/MiniAOD_Test/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/submit" "--output-dag-file=/nfs_scratch/zmao/MiniAOD_Test/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/dags/dag" "--output-dir=srm://cmssrm.hep.wisc.edu:8443/srm/v2/server?SFN=/hdfs/store/user/zmao/MiniAOD_Test/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/" --input-files-per-job=1 --input-file-list=/nfs_scratch/zmao/MiniAOD_Test/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/dags/daginputs/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_inputfiles.txt --assume-input-files-exist --input-dir=root://cmsxrootd.fnal.gov/ MiniAOD_Test-TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola make_ntuples_cfg.py channels=tt isMC=1 nExtraJets=6 svFit=1 'inputFiles=$inputFileNames' 'outputFile=$outputFileName'
