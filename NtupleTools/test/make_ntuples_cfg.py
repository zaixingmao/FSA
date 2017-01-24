#!/usr/bin/env cmsRun
'''

Ntuple Generation
=================

Generates the ntuples for a given list of final state generation.

Usage:

./make_ntuples_cfg.py channels="mt,em,mm,eemm" [options]

There are some additional pre-defined groups of channels which are expanded
for your convenience::

zh = eeem, eeet, eemt, eett, emmm, emmt, mmmt, mmtt,
zz = eeee, eemm, mmmm,
zgg = eegg, mmgg
llt = emt, mmt, eet, mmm, emm
zg = mmg,eeg
zgxtra = mgg, emg, egg,

The available options (which are set to zero or one) are::

skipEvents=0 - events to skip (for debugging)
maxEvents=-1 - events to run on
rerunMCMatch=0 - rerun MC matching
eventView=0 - make a row in the ntuple correspond to an event
instead of a final state in an event.
passThru=0 - turn off any preselection/skim
dump=0     - if one, dump process python to stdout
verbose=0 - print out timing information
noPhotons=0 - don't build things which depend on photons.
rerunMVAMET=0 - rerun the MVAMET algorithm
rerunQGJetID=0 - rerun the quark-gluon JetID
rerunJets=0   - rerun with new jet energy corrections
use25ns=1 - run on 25 ns miniAOD (default, 0 = 50ns)
runDQM=0 - run over single object final states to test all object properties (wont check diobject properties)
hzz=0 - Include FSR contribution a la HZZ4l group, include all ZZ candidates (including alternative lepton pairings).
nExtraJets=0 - Include basic info about this many jets (ordered by pt). Ignored if final state involves jets.
paramFile='' - custom parameter file for ntuple production

'''

import FWCore.ParameterSet.Config as cms
import os
from FinalStateAnalysis.NtupleTools.hzg_sync_mod import set_passthru
from FinalStateAnalysis.NtupleTools.ntuple_builder import \
    make_ntuple, add_ntuple
from FinalStateAnalysis.Utilities.version import cmssw_major_version, \
    cmssw_minor_version
import PhysicsTools.PatAlgos.tools.helpers as helpers
#import localJob_cfg
process = cms.Process("Ntuples")

process.options = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True)
)

import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing
options = TauVarParsing.TauVarParsing(
    skipEvents=0,  # Start at an event offset (for debugging)
    reportEvery=1000,
    channels='mm,mjj,mj',
    rerunMCMatch=False,
    eventView=0,  # Switch between final state view (0) and event view (1)
    passThru=0,  # Turn off preselections
    dump=0,  # If one, dump process python to stdout
    verbose=0,  # If one print out the TimeReport
    noPhotons=0,  # If one, don't assume that photons are in the PAT tuples.
    rochCor="",
    eleCor="",
    rerunQGJetID=0,  # If one reruns the quark-gluon JetID
    runMVAMET=0,  # If one, (re)build the MVA MET
    runMETFilters=1,  # If one, run MET filter
    runTauTauMVAMET=0,  # If one, (re)build the MVA MET
    rerunJets=0,
    dblhMode=False, # For double-charged Higgs analysis
    runTauSpinner=0,
    GlobalTag=1,
    use25ns=1,
    runDQM=0,
    hzz=0,
    TNT=0,
    sys="",
    paramFile='',
)

finalStates = ['tt', 'et', 'ee', 'mm', 'mt', 'em', 
               'ttt', 'ett', 'eet', 'mmt', 'mtt', 'emt', 
               'eee', 'emm', 'eem', 'mmm',  
               'eett', 'emtt', 'mmtt', 'mttt', 'ettt', 'tttt',
               'eeee', 'eeem', 'eemm', 'eemt', 'eeet',
               'emmm', 'mmmm', 'mmmt', 'emmt',
              ]

for ifs in finalStates:
    options.register(
        'skimCuts-%s' %ifs,
        '',
        TauVarParsing.TauVarParsing.multiplicity.list,
        TauVarParsing.TauVarParsing.varType.string,
        'additional cuts to impose on the NTuple'
    )

options.register(
    'nExtraJets',
    0,
    TauVarParsing.TauVarParsing.multiplicity.singleton,
    TauVarParsing.TauVarParsing.varType.int,
    'Number of pt-ordered jets to keep some info about. Ignored if final state involves jets.',
)


options.outputFile = "ntuplize.root"
options.parseArguments()

# list of filters to apply
filters = []

if options.TNT:
    print 'running TNT configuration'

# SV Fit requires MVA MET
options.runMVAMET = options.runMVAMET

process.source = cms.Source(
    "PoolSource",
#    fileNames=cms.untracked.vstring(localJob_cfg.localJobInfo['inputFiles']),
    fileNames=cms.untracked.vstring(options.inputFiles),
#    duplicateCheckMode=cms.untracked.string("noDuplicateCheck"),
    skipEvents=cms.untracked.uint32(options.skipEvents),
)

from FinalStateAnalysis.NtupleTools.parameters.default import parameters
if options.paramFile:
    # add custom parameters
    if os.path.isfile(options.paramFile):
        print 'Using custom parameter file %s' % os.path.abspath(options.paramFile)
        import imp
        custParamModule = imp.load_source('custParamModule',options.paramFile)
        from custParamModule import parameters as custParams
        parameters.update(custParams)
    else:
        print 'Failed to load custom parameters, using default.'
    pass

if options.eventsToProcess:
    process.source.eventsToProcess = cms.untracked.VEventRange(
        options.eventsToProcess)

# If desired, apply a luminosity mask
if options.lumiMask:
    print "Applying LumiMask from", options.lumiMask
    import FWCore.PythonUtilities.LumiList as LumiList
    process.source.lumisToProcess = LumiList.LumiList(filename = options.lumiMask).getVLuminosityBlockRange()
#     process.source.lumisToProcess = options.buildPoolSourceLumiMask()

process.TFileService = cms.Service(
    "TFileService", fileName=cms.string(options.outputFile)
)

process.maxEvents = cms.untracked.PSet(
    input=cms.untracked.int32(options.maxEvents))

#process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
#process.printTree = cms.EDAnalyzer("ParticleListDrawer",
#                                   maxEventsToPrint = cms.untracked.int32(100),
#                                   printVertex = cms.untracked.bool(False),
#                                   printOnlyHardInteraction = cms.untracked.bool(False), # Print only status=3 particles. This will not work for Pythia8, which does not have any such particles.
#                                   src = cms.InputTag("prunedGenParticles")
#                                   )
#process.printGen = cms.Path(process.printTree)
process.schedule = cms.Schedule()

if options.TNT:
    process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')
#load magfield and geometry (for mass resolution)
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
# Need the global tag for geometry etc.
envvar = 'mcgt' if options.isMC else 'datagt'
GT = {'mcgt': '80X_mcRun2_asymptotic_2016_TrancheIV_v6',
      'datagt': '80X_dataRun2_Prompt_v14'}#'80X_dataRun2_2016SeptRepro_v4'}

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = cms.string(GT[envvar])
print 'Using globalTag: %s' % process.GlobalTag.globaltag

if not options.GlobalTag:
    print 'Using sqlite'
    dbFile = "sqlite:JEC/"
    dbFile += "Spring16_23Sep2016V2_MC.db" if options.isMC else "Spring16_23Sep2016AllV2_DATA.db"
    tag = "JetCorrectorParametersCollection_Spring16_23Sep2016V2_MC_AK4PFchs"
    if not options.isMC:
        tag = "JetCorrectorParametersCollection_Spring16_23Sep2016AllV2_DATA_AK4PFchs"
    process.load ("CondCore.CondDB.CondDB_cfi")
    from CondCore.CondDB.CondDB_cfi import *
    process.jec = cms.ESSource("PoolDBESSource",
          DBParameters = cms.PSet(
            messageLevel = cms.untracked.int32(0)
            ),
          timetype = cms.string('runnumber'),
          toGet = cms.VPSet(
          cms.PSet(
                record = cms.string('JetCorrectionsRecord'),
                tag    = cms.string(tag),
                label  = cms.untracked.string('AK4PFchs')
                ),
          ), 
          connect = cms.string(dbFile)
    )

    ## add an es_prefer statement to resolve a possible conflict from simultaneous connection to a global tag
    process.es_prefer_jec = cms.ESPrefer('PoolDBESSource','jec')

# Drop the input ones, just to make sure we aren't screwing anything up
process.buildFSASeq = cms.Sequence()
from FinalStateAnalysis.PatTools.patFinalStateProducers \
    import produce_final_states
# Which collections are used to build the final states
fs_daughter_inputs = {
    'electrons': 'slimmedElectrons',
    'muons': 'slimmedMuons',
    'taus': 'slimmedTaus',
    'photons': 'slimmedPhotons',
    'jets': 'slimmedJets',
    'pfmet': 'slimmedMETs',         
    'slimmedMET': 'slimmedMETs',         
    'pfmetNoHF': 'slimmedMETsNoHF',         
    'pfmetPuppi': 'slimmedMETsPuppi',
    'mvamet': 'fixme',              # produced later
    'tautaumvamet': 'fixme',              # produced later
    'fsr': 'slimmedPhotons',
    'vertices': 'offlineSlimmedPrimaryVertices',
    'beamSpots': 'offlineBeamSpot',
    'pfmet_jresUp': 'slimmedMETs',         
    'pfmet_jresDown': 'slimmedMETs',         
    'pfmet_jesUp': 'slimmedMETs',         
    'pfmet_jesDown': 'slimmedMETs',         
    'pfmet_uesUp': 'slimmedMETs',         
    'pfmet_uesDown': 'slimmedMETs',         
    'pfmet_eesUp': 'slimmedMETs',         
    'pfmet_eesDown': 'slimmedMETs',  
    'pfmet_mesUp': 'slimmedMETs',         
    'pfmet_mesDown': 'slimmedMETs',   
    'pfmet_tesUp': 'slimmedMETs',         
    'pfmet_tesDown': 'slimmedMETs',   
}

# embed some things we need that arent in miniAOD yet (like some ids)
output_commands = []

# embed electron ids
electronMVANonTrigIDLabel = "BDTIDNonTrig"
electronMVATrigIDLabel = "BDTIDTrig"


from FinalStateAnalysis.NtupleTools.embedElectronIDs import embedElectronIDs
fs_daughter_inputs['electrons'] = embedElectronIDs(process, True,fs_daughter_inputs['electrons'], fs_daughter_inputs['vertices'], fs_daughter_inputs['beamSpots'], options.TNT)

# Clean out muon "ghosts" caused by track ambiguities
process.ghostCleanedMuons = cms.EDProducer("PATMuonCleanerBySegments",
                                           src = cms.InputTag(fs_daughter_inputs['muons']),
                                           preselection = cms.string("track.isNonnull"),
                                           passthrough = cms.string("isGlobalMuon && numberOfMatches >= 2"),
                                           fractionOfSharedSegments = cms.double(0.499))
# fs_daughter_inputs['muons'] = "ghostCleanedMuons"
# 
# process.miniCleanedMuons = cms.Path(process.ghostCleanedMuons)
# process.schedule.append(process.miniCleanedMuons)

#####################
### Pileup Jet ID ###
#####################

process.load("RecoJets.JetProducers.PileupJetID_cfi")
process.pileupJetIdUpdated = process.pileupJetId.clone(
  jets=cms.InputTag("slimmedJets"),
  inputIsCorrected=True,
  applyJec=True,
  vertexes=cms.InputTag("offlineSlimmedPrimaryVertices")
)

##################
### JEC ##########
##################
isData = not options.isMC

from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
updateJetCollection(
   process,
   jetSource = cms.InputTag('slimmedJets'),
   labelName = 'UpdatedJEC',
   jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None')  # Do not forget 'L2L3Residual' on data!
)
if(isData):
    updateJetCollection.jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']), 'None')
process.updatedPatJetsUpdatedJEC.userData.userFloats.src += ['pileupJetIdUpdated:fullDiscriminant']
process.applyJEC = cms.Path()
process.applyJEC += process.pileupJetIdUpdated
process.applyJEC += process.patJetCorrFactorsUpdatedJEC
process.applyJEC += process.updatedPatJetsUpdatedJEC
process.schedule.append(process.applyJEC)
fs_daughter_inputs['jets'] = 'updatedPatJetsUpdatedJEC'

#######################################
## ReRun Type1 Correction for MET######
#######################################
from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
runMetCorAndUncFromMiniAOD(process, 
                           isData = isData,
                          )
baseMET = "patPFMetT1"
fs_daughter_inputs['pfmet'] = baseMET
process.reRunType1MET = cms.Path(process.patPFMetT1)

variations = {"jres": "JetRes",
              "jes": "JetEn",
              "ues": "UnclusteredEn",
              "ees": "ElectronEn",
              "mes": "MuonEn",
              "tes": "TauEn",
            }
for iVar in variations.keys():
    for sys in ["Up", "Down"]:
        process.reRunType1MET += getattr(process, baseMET+variations[iVar]+sys)
        fs_daughter_inputs['pfmet_%s%s' %(iVar,sys)] = baseMET+variations[iVar]+sys

process.schedule.append(process.reRunType1MET)

#Add met significane for normal RECO METs for svFit testing
process.load("RecoMET.METProducers.METSignificance_cfi")
process.METSignificance.srcMet = cms.InputTag(fs_daughter_inputs['pfmet'])
process.METSignificance.srcPfJets = cms.InputTag(fs_daughter_inputs['jets'])
process.METSigSeq = cms.Path(process.METSignificance)
process.schedule.append(process.METSigSeq)


process.miniPatMuons = cms.EDProducer(
    "MiniAODMuonIDEmbedder",
    src=cms.InputTag(fs_daughter_inputs['muons']),
    vertices=cms.InputTag(fs_daughter_inputs['vertices']),
    beamSrc=cms.InputTag(fs_daughter_inputs['beamSpots']),
    Muon_vtx_ndof_min = cms.int32(4),
    Muon_vtx_rho_max = cms.int32(2),
    Muon_vtx_position_z_max = cms.double(24.),
    TNT = cms.bool(bool(options.TNT)),
)
fs_daughter_inputs['muons'] = "miniPatMuons"

process.miniPatJets = cms.EDProducer(
    "MiniAODJetIdEmbedder",
    isMC=cms.int32(options.isMC),
    src=cms.InputTag(fs_daughter_inputs['jets'])
)
fs_daughter_inputs['jets'] = 'miniPatJets'
process.runMiniAODObjectEmbedding = cms.Path(
    process.miniPatMuons+
    process.miniPatJets
)
process.schedule.append(process.runMiniAODObjectEmbedding)

process.miniMuonsEmbedIp = cms.EDProducer(
    "MiniAODMuonIpEmbedder",
    src = cms.InputTag(fs_daughter_inputs['muons']),
    vtxSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
)
fs_daughter_inputs['muons'] = 'miniMuonsEmbedIp'

process.miniElectronsEmbedIp = cms.EDProducer(
    "MiniAODElectronIpEmbedder",
    src = cms.InputTag(fs_daughter_inputs['electrons']),
    vtxSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
)
fs_daughter_inputs['electrons'] = 'miniElectronsEmbedIp'

process.miniTausEmbedIp = cms.EDProducer(
    "MiniAODTauIpEmbedder",
    src = cms.InputTag(fs_daughter_inputs['taus']),
    vtxSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
    beamSpot =cms.InputTag(fs_daughter_inputs['beamSpots']),
    Tau_vtx_ndof_min = cms.int32(4),
    Tau_vtx_rho_max = cms.int32(2),
    Tau_vtx_position_z_max = cms.double(24.),
    TNT = cms.bool(bool(options.TNT)),
)
fs_daughter_inputs['taus'] = 'miniTausEmbedIp'

process.runMiniAODLeptonIpEmbedding = cms.Path(
    process.miniMuonsEmbedIp+
    process.miniElectronsEmbedIp+
    process.miniTausEmbedIp
)
process.schedule.append(process.runMiniAODLeptonIpEmbedding)

#relIso embedding
process.miniMuonsEmbedRelIso = cms.EDProducer(
    "MiniAODMuonRelIsoEmbedder",
    src = cms.InputTag(fs_daughter_inputs['muons']),
)
fs_daughter_inputs['muons'] = 'miniMuonsEmbedRelIso'

process.miniElectronsEmbedRelIso = cms.EDProducer(
    "MiniAODElectronRelIsoEmbedder",
    src = cms.InputTag(fs_daughter_inputs['electrons']),
)
fs_daughter_inputs['electrons'] = 'miniElectronsEmbedRelIso'
process.runMiniAODLeptonRelIsoEmbedding = cms.Path(
    process.miniMuonsEmbedRelIso+
    process.miniElectronsEmbedRelIso
)
process.schedule.append(process.runMiniAODLeptonRelIsoEmbedding)

# Embed effective areas in muons and electrons
process.load("FinalStateAnalysis.PatTools.electrons.patElectronEAEmbedding_cfi")
process.patElectronEAEmbedder.src = cms.InputTag(fs_daughter_inputs['electrons'])
process.load("FinalStateAnalysis.PatTools.muons.patMuonEAEmbedding_cfi")
process.patMuonEAEmbedder.src = cms.InputTag(fs_daughter_inputs['muons'])
#fs_daughter_inputs['electrons'] = 'patElectronEAEmbedder'
#fs_daughter_inputs['muons'] = 'patMuonEAEmbedder'
# And for electrons, the new HZZ4l EAs as well
process.miniAODElectronEAEmbedding = cms.EDProducer(
    "MiniAODElectronEffectiveArea2015Embedder",
    src = cms.InputTag(fs_daughter_inputs['electrons']),
    label = cms.string("EffectiveArea_HZZ4l2015"), # embeds a user float with this name
    )
#fs_daughter_inputs['electrons'] = 'miniAODElectronEAEmbedding'
process.EAEmbedding = cms.Path(
    process.patElectronEAEmbedder +
    process.patMuonEAEmbedder +
    process.miniAODElectronEAEmbedding
    )
#process.schedule.append(process.EAEmbedding)

# Embed rhos in electrons
process.miniAODElectronRhoEmbedding = cms.EDProducer(
    "ElectronRhoOverloader",
    src = cms.InputTag(fs_daughter_inputs['electrons']),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll"), # not sure this is right
    userLabel = cms.string("rhoCSA14")
    )
#fs_daughter_inputs['electrons'] = 'miniAODElectronRhoEmbedding'

# ... and muons
process.miniAODMuonRhoEmbedding = cms.EDProducer(
    "MuonRhoOverloader",
    src = cms.InputTag(fs_daughter_inputs['muons']),
    srcRho = cms.InputTag("fixedGridRhoFastjetCentralNeutral"), # not sure this is right
    userLabel = cms.string("rhoCSA14")
    )
#fs_daughter_inputs['muons'] = 'miniAODMuonRhoEmbedding'
process.rhoEmbedding = cms.Path(
    process.miniAODElectronRhoEmbedding +
    process.miniAODMuonRhoEmbedding
    )
#process.schedule.append(process.rhoEmbedding)

if options.hzz:
    # Make FSR photon collection, give them isolation
    process.load("FinalStateAnalysis.PatTools.miniAOD_fsrPhotons_cff")
    fs_daughter_inputs['fsr'] = 'boostedFsrPhotons'
    output_commands.append('*_boostedFsrPhotons_*_*')
    process.makeFSRPhotons = cms.Path(process.fsrPhotonSequence)
    process.schedule.append(process.makeFSRPhotons)

    # Embed HZZ ID and isolation decisions because we need to know them for FSR recovery
    idCheatLabel = "HZZ4lIDPass" # Gets loose ID. For tight ID, append "Tight".
    isoCheatLabel = "HZZ4lIsoPass"
    process.electronIDIsoCheatEmbedding = cms.EDProducer(
        "MiniAODElectronHZZIDDecider",
        src = cms.InputTag(fs_daughter_inputs['electrons']),
        idLabel = cms.string(idCheatLabel), # boolean stored as userFloat with this name
        isoLabel = cms.string(isoCheatLabel), # boolean stored as userFloat with this name
        rhoLabel = cms.string("rhoCSA14"), # use rho and EA userFloats with these names
        eaLabel = cms.string("EffectiveArea_HZZ4l2015"),
        vtxSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
        bdtLabel = cms.string(electronMVANonTrigIDLabel),
        )
    fs_daughter_inputs['electrons'] = 'electronIDIsoCheatEmbedding'
    output_commands.append('*_electronIDIsoCheatEmbedding_*_*')
    process.muonIDIsoCheatEmbedding = cms.EDProducer(
        "MiniAODMuonHZZIDDecider",
        src = cms.InputTag(fs_daughter_inputs['muons']),
        idLabel = cms.string(idCheatLabel), # boolean will be stored as userFloat with this name
        isoLabel = cms.string(isoCheatLabel), # boolean will be stored as userFloat with this name
        vtxSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
        # Defaults are correct as of 9 March 2015, overwrite later if needed
        )
    fs_daughter_inputs['muons'] = 'muonIDIsoCheatEmbedding'
    output_commands.append('*_muonIDIsoCheatEmbedding_*_*')
    process.embedHZZ4lIDDecisions = cms.Path(
        process.electronIDIsoCheatEmbedding +
        process.muonIDIsoCheatEmbedding
        )
    process.schedule.append(process.embedHZZ4lIDDecisions)
    

## Do preselection as requested in the analysis parameters
preselections = parameters.get('preselection',{})

from FinalStateAnalysis.NtupleTools.object_parameter_selector import setup_selections, getName
process.preselectionSequence = setup_selections(
    process, 
    "Preselection",
    fs_daughter_inputs,
    preselections,
    )
for ob in preselections:
    fs_daughter_inputs[getName(ob)+'s'] = getName(ob)+"Preselection"
    output_commands.append('*_%sPreselection_*_*'%getName(ob))
process.FSAPreselection = cms.Path(process.preselectionSequence)
process.schedule.append(process.FSAPreselection)


# embed info about nearest jet
process.miniAODElectronJetInfoEmbedding = cms.EDProducer(
    "MiniAODElectronJetInfoEmbedder",
    src = cms.InputTag(fs_daughter_inputs['electrons']),
    embedBtags = cms.bool(False),
    suffix = cms.string(''),
    jetSrc = cms.InputTag(fs_daughter_inputs['jets']),
    maxDeltaR = cms.double(0.1),
)
#fs_daughter_inputs['electrons'] = 'miniAODElectronJetInfoEmbedding'
process.miniAODMuonJetInfoEmbedding = cms.EDProducer(
    "MiniAODMuonJetInfoEmbedder",
    src = cms.InputTag(fs_daughter_inputs['muons']),
    embedBtags = cms.bool(False),
    suffix = cms.string(''),
    jetSrc = cms.InputTag(fs_daughter_inputs['jets']),
    maxDeltaR = cms.double(0.1),
)
#fs_daughter_inputs['muons'] = 'miniAODMuonJetInfoEmbedding'
process.miniAODTauJetInfoEmbedding = cms.EDProducer(
    "MiniAODTauJetInfoEmbedder",
    src = cms.InputTag(fs_daughter_inputs['taus']),
    embedBtags = cms.bool(False),
    suffix = cms.string(''),
    jetSrc = cms.InputTag(fs_daughter_inputs['jets']),
    maxDeltaR = cms.double(0.1),
)
#fs_daughter_inputs['taus'] = 'miniAODTauJetInfoEmbedding'

#process.jetInfoEmbedding = cms.Path(
#    process.miniAODElectronJetInfoEmbedding +
#    process.miniAODMuonJetInfoEmbedding +
#    process.miniAODTauJetInfoEmbedding
#)
#process.schedule.append(process.jetInfoEmbedding)

process.bTagSFJets = cms.EDProducer(
    "MiniAODJetBTagSFEmbedder",
    isMC=cms.int32(options.isMC),
    src=cms.InputTag(fs_daughter_inputs['jets'])
)
fs_daughter_inputs['jets'] = 'bTagSFJets'
process.bTagSFEmbedding = cms.Path(process.bTagSFJets)
process.schedule.append(process.bTagSFEmbedding)

#systematcs embedding
if options.sys == 'tauEC':
    process.sysEmbedTau = cms.EDProducer(
        "PATTauSystematicsEmbedder",
        src = cms.InputTag(fs_daughter_inputs['taus']),
        tauEnergyScale = cms.PSet(
            applyCorrection = cms.bool(False),
            uncLabelUp = cms.string("AK5PF"),
            uncLabelDown = cms.string("AK5PF"),
            uncTag = cms.string("Uncertainty"),
            flavorUncertainty = cms.double(0),
        ),
    )
    fs_daughter_inputs['taus'] = 'sysEmbedTau'
    process.sysEmbedding = cms.Path(process.sysEmbedTau)
    process.schedule.append(process.sysEmbedding)

elif options.sys == 'jetBTag':
    process.bTagSysJets = cms.EDProducer(
        "MiniAODJetBTagSysEmbedder",
        isMC=cms.int32(options.isMC),
        src=cms.InputTag(fs_daughter_inputs['jets'])
    )
    fs_daughter_inputs['jets'] = 'bTagSysJets'
    process.sysEmbedding = cms.Path(process.bTagSysJets)
    process.schedule.append(process.sysEmbedding)

elif options.sys == 'jetEC':
    process.sysEmbedJets = cms.EDProducer(
    "PATJetSystematicsEmbedder",
        src = cms.InputTag(fs_daughter_inputs['jets']),
        corrLabel = cms.string("AK5PF"),
        unclusteredEnergyScale = cms.double(0.1),
    )
    fs_daughter_inputs['jets'] = 'sysEmbedJets'
    process.sysEmbedding = cms.Path(process.sysEmbedJets)
    process.schedule.append(process.sysEmbedding)
    


# add met filters
if options.runMETFilters:
    # flags in miniaod
    listOfFlags = ['Flag_HBHENoiseFilter',
                   'Flag_HBHENoiseIsoFilter',
                   'Flag_globalTightHalo2016Filter',
                   'Flag_EcalDeadCellTriggerPrimitiveFilter',
                   'Flag_goodVertices',
                   'Flag_eeBadScFilter',
                   ]
    listOfLabels = ['HBHENoiseFilterResult',
                   'HBHENoiseIsoFilterResult',
                   'globalTightHalo2016FilterResult',
                   'EcalDeadCellTriggerPrimitiveFilterResult',
                   'goodVerticesResult',
                   'eeBadScFilterResult',
                   ]
    process.MiniAODMETFilterProducer = cms.EDProducer('MiniAODTriggerProducer',
        triggers = cms.vstring(*listOfFlags),
        labels = cms.vstring(*listOfLabels),
        bits = cms.InputTag("TriggerResults"),
        #prescales = cms.InputTag("patTrigger"),
        #objects = cms.InputTag("selectedPatTrigger"),
    )
    filters += [process.MiniAODMETFilterProducer]
    for label in listOfLabels:
        modName = 'Apply{0}'.format(label)
        mod = cms.EDFilter('BooleanFlagFilter',
            inputLabel = cms.InputTag('MiniAODMETFilterProducer',label),
            reverseDecision = cms.bool(True)
        )
        setattr(process,modName,mod)
        filters += [getattr(process,modName)]

    process.load('RecoMET.METFilters.BadPFMuonFilter_cfi')
    process.BadPFMuonFilter.muons = cms.InputTag("slimmedMuons")
    process.BadPFMuonFilter.PFCandidates = cms.InputTag("packedPFCandidates")
    process.BadPFMuonFilter.filter = cms.bool(True)

    process.load('RecoMET.METFilters.BadChargedCandidateFilter_cfi')
    process.BadChargedCandidateFilter.muons = cms.InputTag("slimmedMuons")
    process.BadChargedCandidateFilter.PFCandidates = cms.InputTag("packedPFCandidates")
    process.BadChargedCandidateFilter.filter = cms.bool(True)

    process.additionalMETFilters = cms.Path(
        process.BadPFMuonFilter +
        process.BadChargedCandidateFilter
        )
    process.schedule.append(process.additionalMETFilters)


if options.hzz:    
    # Put FSR photons into leptons as user cands
    from FinalStateAnalysis.PatTools.miniAODEmbedFSR_cfi \
        import embedFSRInElectrons, embedFSRInMuons
    process.electronFSREmbedder = embedFSRInElectrons.clone(
        src = cms.InputTag(fs_daughter_inputs['electrons']),
        srcAlt = cms.InputTag(fs_daughter_inputs['muons']),
        srcPho = cms.InputTag(fs_daughter_inputs['fsr']),
        srcVeto = cms.InputTag(fs_daughter_inputs['electrons']),
        srcVtx = cms.InputTag("offlineSlimmedPrimaryVertices"),
        idDecisionLabel = cms.string(idCheatLabel),
        )
    fs_daughter_inputs['electrons'] = 'electronFSREmbedder'
    output_commands.append('*_electronFSREmbedder_*_*')
    process.muonFSREmbedder = embedFSRInMuons.clone(
        src = cms.InputTag(fs_daughter_inputs['muons']),
        srcAlt = cms.InputTag(fs_daughter_inputs['electrons']),
        srcPho = cms.InputTag(fs_daughter_inputs['fsr']),
        srcVeto = cms.InputTag(fs_daughter_inputs['electrons']),
        srcVtx = cms.InputTag("offlineSlimmedPrimaryVertices"),
        idDecisionLabel = cms.string(idCheatLabel),
        )
    fs_daughter_inputs['muons'] = 'muonFSREmbedder'
    output_commands.append('*_muonFSREmbedder_*_*')
    process.embedFSRInfo = cms.Path(
        process.electronFSREmbedder +
        process.muonFSREmbedder
        )
    process.schedule.append(process.embedFSRInfo)


# Eventually, set buildFSAEvent to False, currently working around bug
# in pat tuples.
produce_final_states(process, fs_daughter_inputs, output_commands, process.buildFSASeq,
                     'puTagDoesntMatter', buildFSAEvent=True,
                     noTracks=True, runMVAMET=options.runMVAMET, runTauTauMVAMET = options.runTauTauMVAMET,
                     hzz=options.hzz, rochCor=options.rochCor,
                     eleCor=options.eleCor, use25ns=options.use25ns, **parameters)
process.buildFSAPath = cms.Path(process.buildFSASeq)
# Don't crash if some products are missing (like tracks)
process.patFinalStateEventProducer.forbidMissing = cms.bool(False)
process.schedule.append(process.buildFSAPath)
# Drop the old stuff.
process.source.inputCommands = cms.untracked.vstring(
    'keep *',
    'drop PATFinalStatesOwned_finalState*_*_*',
    'drop *_patFinalStateEvent*_*_*'
)

suffix = '' # most analyses don't need to modify the final states

if options.hzz:
    process.embedHZZMESeq = cms.Sequence()
    # Embed matrix elements in relevant final states
    suffix = "HZZME"
    for quadFS in ['ElecElecElecElec', 
                   'ElecElecMuMu',
                   'MuMuMuMu']:
        oldName = "finalState%s"%quadFS
        embedProducer = cms.EDProducer(
            "MiniAODHZZMEEmbedder",
            src = cms.InputTag(oldName),
            processes = cms.vstring("p0plus_VAJHU",
                                    "bkg_VAMCFM"),
            )

        # give the FS collection the same name as before, but with an identifying suffix
        newName = oldName + suffix
        setattr(process, newName, embedProducer)
        process.embedHZZMESeq += embedProducer
        output_commands.append('*_%s_*_*'%newName)
            
    process.embedHZZME = cms.Path(process.embedHZZMESeq)
    process.schedule.append(process.embedHZZME)
        


_FINAL_STATE_GROUPS = {
    'zh': 'eeem, eeet, eemt, eett, emmm, emmt, mmmt, mmtt',
    'zz': 'eeee, eemm, mmmm',
    'zgg': 'eegg, mmgg',
    'llt': 'emt, mmt, eet, mmm, emm, mm, ee, em',
    'zg': 'mmg, eeg',
    'zgxtra': 'mgg, emg, egg',
    'dqm': 'e,m,t,g,j',
    '3lep': 'eee, eem, eet, emm, emt, ett, mmm, mmt, mtt, ttt',
    '4lep': 'eeee, eeem, eeet, eemm, eemt, eett, emmm, emmt, emtt, ettt, mmmm, mmmt, mmtt, mttt, tttt',
}

# run dqm
if options.runDQM: options.channels = 'dqm'

# Generate analyzers which build the desired final states.
final_states = [x.strip() for x in options.channels.split(',')]


def order_final_state(state):
    '''
    Sorts final state objects into order expected by FSA.
    
    Sorts string of characters into ordr defined by "order." Invalid 
    characters are ignored, and a warning is pribted to stdout
    
    returns the sorted string
    '''
    order = "emtgj"
    for obj in state:
        if obj not in order:
            print "invalid Final State object "\
                "'%s' ignored" % obj
            state = state.replace(obj, "")
    return ''.join(sorted(state, key=lambda x: order.index(x)))
 
def expanded_final_states(input):
    for fs in input:
        if fs in _FINAL_STATE_GROUPS:
            for subfs in _FINAL_STATE_GROUPS[fs].split(','):
                yield subfs.strip()
        else:
            yield fs

print "Building ntuple for final states: %s" % ", ".join(final_states)

for final_state in expanded_final_states(final_states):
    extraJets = options.nExtraJets if 'j' not in final_state else 0
    final_state = order_final_state(final_state)

    skimCuts = getattr(options, "skimCuts-%s" %final_state)
    print skimCuts
    analyzer = make_ntuple(*final_state, 
                            dblhMode=options.dblhMode,
                            runTauSpinner=options.runTauSpinner, 
                            runMVAMET=options.runMVAMET,
                            runTauTauMVAMET=options.runTauTauMVAMET,
                            skimCuts=skimCuts, suffix=suffix,
                            isMC=options.isMC,
                            hzz=options.hzz, nExtraJets=extraJets, **parameters)
    add_ntuple(final_state, analyzer, process,
               process.schedule, options.eventView, filters)


process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery
process.MessageLogger.categories.append('FSAEventMissingProduct')
process.MessageLogger.categories.append('UndefinedPreselectionInfo')
process.MessageLogger.categories.append('GsfElectronAlgo')

# Don't go nuts if there are a lot of missing products.
process.MessageLogger.cerr.FSAEventMissingProduct = cms.untracked.PSet(
    limit=cms.untracked.int32(10)
)
# process.MessageLogger.suppresssWarning = cms.untracked.vstring("GsfElectronAlgo","UndefinedPreselectionInfo")
process.MessageLogger.cerr.GsfElectronAlgo = cms.untracked.PSet(
    limit = cms.untracked.int32(0)
)
process.MessageLogger.cerr.UndefinedPreselectionInfo = cms.untracked.PSet(
    limit = cms.untracked.int32(0)
)
# process.Tracer = cms.Service("Tracer")

if options.verbose:
    process.options.wantSummary = cms.untracked.bool(True)
if options.passThru:
    set_passthru(process)

if options.dump:
    print process.dumpPython()
