#!/usr/bin/env python
import os


#edit the location of the MINIAOD file to run interactively
file = "/store/mc/RunIISpring16MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/00000/00F0B3DC-211B-E611-A6A0-001E67248A39.root"
file = "/store/mc/RunIISpring16MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/50000/0C1A54B9-E21A-E611-B256-7845C4FC39C5.root"

localJobInfo = {'inputFile': file,
                
                #edit the desired output file name
                'outputFile': 'myTestFile.root',

                #edit the desired event to run, given it's 'run:lumi:event' info. By default, all means to run over all the events
                'eventsToProcess':'all',#'1:203675:51109545'

                #edit the desired number of events to run. By default, it's set to 100.
                #Setting it to -1 will run over all the events (not recommended for interactive runs)                                       
                'maxEvents':1000}
