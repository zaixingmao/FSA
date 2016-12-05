#!/usr/bin/env python
import os


#edit the location of the MINIAOD file to run interactively
#file = "/store/mc/RunIISpring16MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/00000/00F0B3DC-211B-E611-A6A0-001E67248A39.root"
#file = "/store/data/Run2016H/SingleMuon/MINIAOD/PromptReco-v3/000/284/036/00000/0E02D50E-989F-E611-A962-FA163EE15C80.root"
#file = "/store/data/Run2016H/SingleMuon/MINIAOD/PromptReco-v2/000/281/207/00000/C01B8838-6282-E611-9884-02163E01414B.root"
file = "/store/data/Run2016B/SingleElectron/MINIAOD/23Sep2016-v2/80000/08A02DC3-608C-E611-ADA5-0025905B85B6.root"

file = "/store/data/Run2016H/SingleElectron/MINIAOD/PromptReco-v3/000/284/036/00000/1257A268-599F-E611-A437-02163E011E7A.root"
#file = ""
#for i in range(1, 51, 1):
#    file += "/store/user/anirban/ZprimeToTauTau_M_2000_GEN_SIM/ZprimeToTauTau_M_2000_step4/160723_124341/0000/ZprimeToTauTau_M_2000_TuneCUETP8M1_tauola_13TeV_pythia8_step4_%i.root" %i
#    if i != 50:
#        file += ","


localJobInfo = {'inputFile': file,
                
                #edit the desired output file name
                'outputFile': 'myTestFile.root',

                #edit the desired event to run, given it's 'run:lumi:event' info. By default, all means to run over all the events
                'eventsToProcess':'all',#'1:203675:51109545'

                #edit the desired number of events to run. By default, it's set to 100.
                #Setting it to -1 will run over all the events (not recommended for interactive runs)                                       
                'maxEvents':1000}
