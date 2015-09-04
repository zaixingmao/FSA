'''
Data definitions for 13 TeV samples.
'''

from datacommon import square, cube, quad, picobarns, br_w_leptons, br_z_leptons, query_cli

data_name_map = {}

datadefs = {}

datadefs["DYJets_M10-Asympt25ns"] = {
    'analyses': [],
    'datasetpath': '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 18610.0*picobarns,
}


datadefs["DYJets_M50-Asympt25ns"] = {
    'analyses': [],
    'datasetpath': '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 6025.0*picobarns,
}

datadefs["WJetsToLNu-Asympt25ns"] = {
    'analyses': [],
    'datasetpath': '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 61526.7*picobarns,
}

datadefs["TTJets-Asympt25ns"] = {
    'analyses': [],
    'datasetpath': '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 831.76*picobarns,
}

datadefs["ST_tW_top-Asympt25ns"] = {
    'analyses': [],
    'datasetpath': '/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 35.6*picobarns,
}

datadefs["ST_tW_antitop-Asympt25ns"] = {
    'analyses': [],
    'datasetpath': '/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 35.6*picobarns,
}

datadefs["ST_t-channel_antitop-Asympt25ns"] = {
    'analyses': [],
    'datasetpath': '/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 80.95*picobarns,
}

datadefs["ST_t-channel_top-Asympt25ns"] = {
    'analyses': [],
    'datasetpath': '/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 103.02*picobarns,
}

datadefs["WW-Asympt25ns"] = {
    'analyses': [],
    'datasetpath': '/WW_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 63.21*picobarns,
}

datadefs["WWTo2L2Nu-Asympt25ns"] = {
    'analyses': [],
    'datasetpath': '/WWTo2L2Nu_13TeV-powheg/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 10.481*picobarns,
}

datadefs["WWTo4Q-Asympt25ns"] = {
    'analyses': [],
    'datasetpath': '/WWTo4Q_13TeV-powheg/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 45.20*picobarns,
}

datadefs["WWToLNuQQ-Asympt25ns"] = {
    'analyses': [],
    'datasetpath': '/WWToLNuQQ_13TeV-powheg/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 43.53*picobarns,
}

datadefs["WZ-Asympt25ns"] = {
    'analyses': [],
    'datasetpath': '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 22.82*picobarns,
}

datadefs["WZTo1L1Nu2Q-Asympt25ns"] = {
    'analyses': [],
    'datasetpath': '/WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 10.96*picobarns,
}

datadefs["WZTo3LNu-Asympt25ns"] = {
    'analyses': [],
    'datasetpath': '/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 4.42965*picobarns,
}

datadefs["ZZ-Asympt25ns"] = {
    'analyses': [],
    'datasetpath': '/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 10.32*picobarns,
}
datadefs["ZZTo4L-Asympt25ns"] = {
    'analyses': [],
    'datasetpath': '/ZZTo4L_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 1.256*picobarns,
}


datadefs["ZprimeToTauTau_M_500-Asympt25ns"] = {
    'analyses': [],
    'datasetpath': '/ZprimeToTauTau_M_500_TuneCUETP8M1_tauola_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': -999,
}

datadefs["ZprimeToTauTau_M_2000-Asympt25ns"] = {
    'analyses': [],
    'datasetpath': '/ZprimeToTauTau_M_2000_TuneCUETP8M1_tauola_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': -999,
}

datadefs["ZprimeToTauTau_M_2500-Asympt25ns"] = {
    'analyses': [],
    'datasetpath': '/ZprimeToTauTau_M_2500_TuneCUETP8M1_tauola_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': -999,
}

datadefs["DYJets_M50-PU20bx25"] = {
    'analyses': ['4L'],
    'datasetpath': '/DYJetsToLL_M-50_13TeV-madgraph-pythia8/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 6025.2*picobarns,
}
datadefs["TTJets-PU20bx25"] = {
    'analyses': ['4L'],
    'datasetpath': '/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 689.1*picobarns, # might be 809.1, I'm not sure. See https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
}
datadefs["ggHZZ-PU20bx25"] = {
    'analyses': ['4L'],
    'datasetpath': '/GluGluToHToZZTo4L_M-125_13TeV-powheg-pythia6/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 43.62*picobarns*0.00133, # xsec * br. ratio. BR for L=e,mu, might need to use BR with tau? (=0.000294)
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

datadefs["VBFHtt-PU20bx25"] = {
    'analyses': [''],
    'datasetpath': '/VBF_HToTauTau_M-125_13TeV-powheg-pythia6/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v2/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': -999, # xsec * br. ratio. BR for L=e,mu, might need to use BR with tau? (=0.000294)
}

datadefs["SUSYM160-RunIISpring15DR74-Asympt25ns"] = {
    'analyses': [''],
    'datasetpath': '/SUSYGluGluToHToTauTau_M-160_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': -999, # xsec * br. ratio. BR for L=e,mu, might need to use BR with tau? (=0.000294)                                                                                     
}

#50 ns

datadefs["DYJets_M50-Asympt50ns"] = {
    'analyses': [],
    'datasetpath': '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9-v2/MINIAODSIM',
    'pu': 'Asympt50ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 6025.0*picobarns,
}

datadefs["TTJets-Asympt50ns"] = {
    'analyses': [],
    'datasetpath': '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
    'pu': 'Asympt50ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 831.76*picobarns,
}

datadefs["ZZ-Asympt50ns"] = {
    'analyses': [],
    'datasetpath': '/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
    'pu': 'Asympt50ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 10.32*picobarns,
}

datadefs["WJetsToLNu-Asympt50ns"] = {
    'analyses': [],
    'datasetpath': '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
    'pu': 'Asympt50ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 20509.0*picobarns,
}


datadefs["WW-Asympt50ns"] = {
    'analyses': [],
    'datasetpath': '/WW_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
    'pu': 'Asympt50ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 63.21*picobarns,
}

datadefs["WZJets-Asympt50ns"] = {
    'analyses': [],
    'datasetpath': '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74- Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM',
    'pu': 'Asympt50ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 22.82*picobarns,
}

datadefs["T_tW-Asympt50ns"] = {
    'analyses': [],
    'datasetpath': '/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
    'pu': 'Asympt50ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 35.6*picobarns,
}

datadefs["Tbar_tW-Asympt50ns"] = {
    'analyses': [],
    'datasetpath': '/ST_tW_antitop_5f_mtop1755_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3/MINIAODSIM',
    'pu': 'Asympt50ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 35.6*picobarns,
}

datadefs["GluGluHToTauTau_M125-Asympt25ns"] = {
    'analyses': [],
    'datasetpath': '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': -999,
}
datadefs["VBFHToTauTau_M125-Asympt25ns"] = {
    'analyses': [],
    'datasetpath': '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': -999,
}

if __name__=="__main__":
    query_cli(datadefs)
