#!/usr/bin/env python
import os

files = []
counter = 0
dirName = '/nfs_scratch/zmao/CMSSW_7_4_14/src/FinalStateAnalysis/NtupleTools/test/Zprime500/'
dirName = '/nfs_scratch/zmao/1250v2/'

#for iFile in os.listdir(dirName):                                                                                                                                                   
    #fName = 'file://%s%s' %(dirName, iFile)                                                                                                                                             
#    files.append(fName)
currentlocation = os.getcwd()
files = "file://%s/testFile_76X.root" %currentlocation
files = "root://cmsxrootd.fnal.gov//store/mc/RunIIFall15MiniAODv2/VBFHToTauTau_M125_13TeV_powheg_pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/70000/0AF323E8-EBB9-E511-961D-002590D0AF6C.root"
files = "root://cmsxrootd.fnal.gov//store/mc/RunIIFall15MiniAODv2/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/00000/00D0925F-56B9-E511-8A71-0025907FD2B2.root"

#files = "file:///hdfs/store/mc/RunIISpring15MiniAODv2/DYJetsToLL_M-1000to1500_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt50ns_74X_mcRun2_asymptotic50ns_v0-v1/30000/7064F70B-417D-E511-AB57-AC162DACC3F0.root"
#files = "file:///hdfs/store/mc/RunIISpring15MiniAODv2/ZprimeToTT_M-500_W-5_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/Asympt50ns_74X_mcRun2_asymptotic50ns_v0-v1/60000/22944E0D-3374-E511-9D35-003048C7B950.root"
#files = [#'file:///hdfs/store/mc/RunIISpring15MiniAODv2/DYJetsToLL_M-500to700_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v3/50000/323F5423-A26F-E511-A847-02163E00EA7B.root']
#    'file:///hdfs/store/mc/RunIISpring15MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/00759690-D16E-E511-B29E-00261894382D.root']

localJobInfo = {#'inputFile': "file:///nfs_scratch/zmao/CEAE1A74-3A5F-E511-821F-02163E013938.root",
               #'inputFile': "file:///hdfs/store/data/Run2015B/Tau/MINIAOD/PromptReco-v1/000/251/883/00000/F46D0932-492D-E511-9E48-02163E013417.root",
#                 'inputFile': "file:///hdfs/store/mc/RunIISpring15DR74/SUSYGluGluToHToTauTau_M-160_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/10000/2A3929AE-5303-E511-9EFE-0025905A48C0.root",
                #'inputFile':"file:///hdfs/store/mc/RunIISpring15DR74/SUSYGluGluToHToTauTau_M-160_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/10000/7AED07BC-5303-E511-8B68-00259074AE6A.root",
    'inputFiles': files,
                #'inputFile': "file:///user_data/zmao/testFiles/miniAODSIM_1000.root",
                #'inputFile': "file:///hdfs/store/mc/RunIISpring15DR74/SUSYGluGluToHToTauTau_M-160_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/10000/64BC29B9-5303-E511-8991-0CC47A4D99B0.root",
                'eventsToProcess':'all',#'1:203675:51109545',#'1:10:1947',#'1:1318:256872', #run, lumi, event
                'maxEvents':100}
