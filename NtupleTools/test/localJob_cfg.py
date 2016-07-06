#!/usr/bin/env python
import os


#edit the location of the MINIAOD file to run interactively
file = "/store/mc/RunIISpring16MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/00000/00F0B3DC-211B-E611-A6A0-001E67248A39.root"
file = "/store/mc/RunIISpring16MiniAODv2/ZprimeToTauTau_M-1750_TuneCUETP8M1_13TeV-pythia8-tauola/MINIAODSIM/PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/00000/02AA02E0-1843-E611-B889-00266CFEFE08.root"

localJobInfo = {'inputFile': file,
                
                #edit the desired output file name
                'outputFile': 'myTestFile.root',

                #edit the desired event to run, given it's 'run:lumi:event' info. By default, all means to run over all the events
                'eventsToProcess':'all',#'1:203675:51109545'

                #edit the desired number of events to run. By default, it's set to 100.
                #Setting it to -1 will run over all the events (not recommended for interactive runs)                                       
                'maxEvents':1000}
