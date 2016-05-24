#!/usr/bin/env python
import os


#edit the location of the MINIAOD file to run interactively
file = "/store/mc/RunIISpring16MiniAODv2/DYJetsToLL_M-5to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/60000/0092BE51-8C1B-E611-8B92-5C260AFFFB63.root"

localJobInfo = {'inputFile': file,
                
                #edit the desired output file name
                'outputFile': 'myTestFile.root',

                #edit the desired event to run, given it's 'run:lumi:event' info. By default, all means to run over all the events
                'eventsToProcess':'all',#'1:203675:51109545'

                #edit the desired number of events to run. By default, it's set to 100.
                #Setting it to -1 will run over all the events (not recommended for interactive runs)                                       
                'maxEvents':-1}
