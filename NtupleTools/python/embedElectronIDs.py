import FWCore.ParameterSet.Config as cms

def embedElectronIDs(process, use25ns, eSrc, vtxSrc, beamSrc, TNT):
    from PhysicsTools.SelectorUtils.tools.vid_id_tools import setupAllVIDIdsInModule, setupVIDElectronSelection, switchOnVIDElectronIdProducer, DataFormat
    switchOnVIDElectronIdProducer(process, DataFormat.MiniAOD)
    process.load("RecoEgamma.ElectronIdentification.egmGsfElectronIDs_cfi")
    process.egmGsfElectronIDs.physicsObjectSrc = cms.InputTag(eSrc)
    if use25ns:
        id_modules = [
            'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_25ns_V1_cff',
#             'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_PHYS14_PU20bx25_nonTrig_V1_cff',
            'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_nonTrig_V1_cff',
            'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV60_cff',
            ]
    else:
        print "50 ns cut based electron IDs don't exist yet for PHYS14. Using CSA14 cuts."
        id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_CSA14_50ns_V1_cff']
    for idmod in id_modules:
        setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)
    
    CBIDLabels = ["CBIDVeto", "CBIDLoose", "CBIDMedium", "CBIDTight", "MVANonTrigWP80", "MVANonTrigWP90", "heepElectronID"] # keys of cut based id user floats
    if use25ns:
        CBIDTags = [
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-veto'),
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-loose'),
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-medium'),
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-tight'),
#             cms.InputTag("egmGsfElectronIDs:mvaEleID-PHYS14-PU20bx25-nonTrig-V1-wp80"),
#             cms.InputTag("egmGsfElectronIDs:mvaEleID-PHYS14-PU20bx25-nonTrig-V1-wp90"),
            cms.InputTag("egmGsfElectronIDs:mvaEleID-Spring15-25ns-nonTrig-V1-wp80"),
            cms.InputTag("egmGsfElectronIDs:mvaEleID-Spring15-25ns-nonTrig-V1-wp90"),
            cms.InputTag("egmGsfElectronIDs:heepElectronID-HEEPV60"),
            ]
    else:
        CBIDTags = [ # almost certainly wrong. Just don't use 50ns miniAOD any more
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-CSA14-50ns-V1-standalone-veto'),
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-CSA14-50ns-V1-standalone-loose'),
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-CSA14-50ns-V1-standalone-medium'),
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-CSA14-50ns-V1-standalone-tight'),
            ]
    if use25ns:
        mvaValueLabels = ["BDTIDNonTrig"]
        mvaValues = [
            cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values"),
            ]
        mvaCategoryLabels = ["BDTIDNonTrigCategory"]
        mvaCategories = [
            cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Categories"),
            ]
    else:
        mvaValueLabels = []
        mvaValues = []
        mvaCategoryLabels = []
        mvaCategories = []

    # Embed cut-based VIDs
    process.miniAODElectronID = cms.EDProducer(
        "MiniAODElectronIDEmbedder",
        src=cms.InputTag(eSrc),
        vtxSrc=cms.InputTag(vtxSrc),
        beamSrc=cms.InputTag(beamSrc),
        idLabels = cms.vstring(*CBIDLabels),
        ids = cms.VInputTag(*CBIDTags),
        valueLabels = cms.vstring(*mvaValueLabels),       # labels for MVA values
        values = cms.VInputTag(*mvaValues),               # mva values
        categoryLabels = cms.vstring(*mvaCategoryLabels),
        categories = cms.VInputTag(*mvaCategories),
        patElectron_vtx_ndof_min = cms.int32(4),
        patElectron_vtx_rho_max = cms.int32(2),
        patElectron_vtx_position_z_max = cms.double(24.),
        TNT = cms.bool(bool(TNT)),
    )
    eSrc = "miniAODElectronID"
    
    process.miniAODElectrons = cms.Path(
        process.egmGsfElectronIDSequence+
        process.miniAODElectronID
        )
    process.schedule.append(process.miniAODElectrons)

    return eSrc