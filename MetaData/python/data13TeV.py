'''
Data definitions for 13 TeV samples.
'''

from datacommon import square, cube, quad, picobarns, br_w_leptons, br_z_leptons, query_cli

data_name_map = {}

datadefs = {}

datadefs["DYJets_M50-PU20bx25"] = {
    'analyses': ['4L'],
    'datasetpath': '/DYJetsToLL_M-50_13TeV-madgraph-pythia8/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 6025.2*picobarns,
}
datadefs["TTJets-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 689.1*picobarns, # might be 809.1, I'm not sure. See https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
}

datadefs["G2HH2tautaubb260"] = {
    'analyses': [],
    'datasetpath': '/GluGluToBulkGravitonToHHTo2B2Tau_M-260_narrow_13TeV-madgraph/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': -999,
}
datadefs["G2HH2tautaubb300"] = {
    'analyses': [],
    'datasetpath': '/GluGluToBulkGravitonToHHTo2B2Tau_M-300_narrow_13TeV-madgraph/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': -999,
}

datadefs["G2HH2tautaubb350"] = {
    'analyses': [],
    'datasetpath': '/GluGluToBulkGravitonToHHTo2B2Tau_M-350_narrow_13TeV-madgraph/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': -999,
}

datadefs["ggHZZ-PU20bx25"] = {
    'analyses': ['4L'],
    'datasetpath': '/GluGluToHToZZTo4L_M-125_13TeV-powheg-pythia6/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 43.62*picobarns*0.00133, # xsec * br. ratio. BR for L=e,mu, might need to use BR with tau? (=0.000294)
}
datadefs["VBFHtt-PU20bx25"] = {
    'analyses': [''],
    'datasetpath': '/VBF_HToTauTau_M-125_13TeV-powheg-pythia6/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v2/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': -999, # xsec * br. ratio. BR for L=e,mu, might need to use BR with tau? (=0.000294)
}

datadefs["ZZTo4L-PU20bx25"] = {
    'analyses': ['4L'],
    'datasetpath': '/ZZTo4L_Tune4C_13TeV-powheg-pythia8/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 15.4*picobarns,
}
datadefs["WZTo3LNu-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/WZJetsTo3LNu_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': -999,
}


if __name__=="__main__":
    query_cli(datadefs)
