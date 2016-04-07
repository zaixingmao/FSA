
'''

Ntuple branch template sets for tau objects.

Each string is transformed into an expression on a FinalStateEvent object.

{object} should be replaced by an expression which evaluates to a pat::Muon
i.e. daughter(1) or somesuch.

Author: Evan K. Friis

'''

from FinalStateAnalysis.Utilities.cfgtools import PSet

info = PSet(
    objectGenDecayMode = '? {object}.hasUserInt("genDecayMode")? {object}.userInt("genDecayMode"): -999',
#     objectLeadTrackPt = '{object}.userFloat("ps_ldTrkPt")',
    objectDecayMode = '{object}.decayMode',
#     objectTNPId = '{object}.userInt("ps_sel_nom")',

    objectEC_up = '? {object}.hasUserFloat("tes+")? {object}.userFloat("tes+"): -999',
    objectEC_down = '? {object}.hasUserFloat("tes-")? {object}.userFloat("tes-"): -999',

    # gen matching
    objectPdgId = '? ({object}.genParticleRef().isNonnull && {object}.genParticleRef().isAvailable) ? {object}.genParticleRef().pdgId() : -999',
    objectComesFromHiggs = 'comesFromHiggs({object_idx},15,0)',

    objectGenCharge      = '? (getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5, 0, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5, 0, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5, 0, 0).charge() : -999',
    objectGenEta         = '? (getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5, 0, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5, 0, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5, 0, 0).eta()   : -999',
    objectGenPhi         = '? (getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5, 0, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5, 0, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5, 0, 0).phi()   : -999',
    objectGenPt          = '? (getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5, 0, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5, 0, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5, 0, 0).pt()   : -999',
    objectGenMass        = '? (getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5, 0, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5, 0, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5, 0, 0).mass()   : -999',

    objectMatchToGenMuPt   = '? (getDaughterGenParticle({object_idx}, 13, 1, 1.0, 0.5, 0, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 1, 1.0, 0.5, 0, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 1, 1.0, 0.5, 0, 0).pt() : 0',
    objectMatchToGenElePt  = '? (getDaughterGenParticle({object_idx}, 11, 1, 1.0, 0.5, 0, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 1, 1.0, 0.5, 0, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 1, 1.0, 0.5, 0, 0).pt() : 0',

    objectGenVisPt       = '? getDaughterGenParticleVisMomentum({object_idx}, 15, 1, 1.0, 0.5).pt() > 0 ? getDaughterGenParticleVisMomentum({object_idx}, 15, 1, 1.0, 0.5).pt()  : -999',
    objectGenVisEta       = '? getDaughterGenParticleVisMomentum({object_idx}, 15, 1, 1.0, 0.5).pt() > 0 ? getDaughterGenParticleVisMomentum({object_idx}, 15, 1, 1.0, 0.5).eta()  : -999',
    objectGenVisPhi       = '? getDaughterGenParticleVisMomentum({object_idx}, 15, 1, 1.0, 0.5).pt() > 0 ? getDaughterGenParticleVisMomentum({object_idx}, 15, 1, 1.0, 0.5).phi()  : -999',
    objectGenVisMass       = '? getDaughterGenParticleVisMomentum({object_idx}, 15, 1, 1.0, 0.5).pt() > 0 ? getDaughterGenParticleVisMomentum({object_idx}, 15, 1, 1.0, 0.5).mass()  : -999',

    objectGenNuPt       = '? getGenParticleNuMomentum({object_idx}, 15, 1, 1.0, 0.5).pt() > 0 ? getGenParticleNuMomentum({object_idx}, 15, 1, 1.0, 0.5).pt()  : -999',
    objectGenNuEta       = '? getGenParticleNuMomentum({object_idx}, 15, 1, 1.0, 0.5).pt() > 0 ? getGenParticleNuMomentum({object_idx}, 15, 1, 1.0, 0.5).eta()  : -999',
    objectGenNuPhi       = '? getGenParticleNuMomentum({object_idx}, 15, 1, 1.0, 0.5).pt() > 0 ? getGenParticleNuMomentum({object_idx}, 15, 1, 1.0, 0.5).phi()  : -999',
    objectGenNuMass       = '? getGenParticleNuMomentum({object_idx}, 15, 1, 1.0, 0.5).pt() > 0 ? getGenParticleNuMomentum({object_idx}, 15, 1, 1.0, 0.5).mass()  : -999',

    objectIsPromptElectron  = '? (getDaughterGenParticle({object_idx}, 11, 1, 1, 0.5, 8, 1).isAvailable && getDaughterGenParticle({object_idx}, 11, 1, 1, 0.5, 8, 1).isNonnull) ? 1 : 0',
    objectIsPromptMuon      = '? (getDaughterGenParticle({object_idx}, 13, 1, 1, 0.5, 8, 2).isAvailable && getDaughterGenParticle({object_idx}, 13, 1, 1, 0.5, 8, 2).isNonnull) ? 1 : 0',
    objectIsTau2Electron    = '? (getDaughterGenParticle({object_idx}, 11, 1, 1, 0.5, 8, 3).isAvailable && getDaughterGenParticle({object_idx}, 11, 1, 1, 0.5, 8, 3).isNonnull) ? 1 : 0',
    objectIsTau2Muon        = '? (getDaughterGenParticle({object_idx}, 13, 1, 1, 0.5, 8, 4).isAvailable && getDaughterGenParticle({object_idx}, 13, 1, 1, 0.5, 8, 4).isNonnull) ? 1 : 0',
    objectIsTauh            = '? (getDaughterGenParticle({object_idx}, 15, 1, 1, 0.5, 15, 5).isAvailable && getDaughterGenParticle({object_idx}, 15, 1, 1, 0.5, 15, 5).isNonnull) ? 1 : 0',

    objectGenMatchCategory = 'getGenMatchCategory({object_idx})',

)

# ID and isolation
id = PSet(
    # updated for what is included in PHYS14 MiniAOD
    # TODO: update when new IDs are released: https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePFTauID#Tau_ID_2014_preparation_for_AN1
    # Against Electron
#    objectAgainstElectronLoose  = '{object}.tauID("againstElectronLoose")',
#    objectAgainstElectronMedium = '{object}.tauID("againstElectronMedium")',
#    objectAgainstElectronTight  = '{object}.tauID("againstElectronTight")',
    
    objectAgainstElectronVLooseMVA5 = '{object}.tauID("againstElectronVLooseMVA5")', 
    objectAgainstElectronLooseMVA5  = '{object}.tauID("againstElectronLooseMVA5")',
    objectAgainstElectronMediumMVA5 = '{object}.tauID("againstElectronMediumMVA5")',
    objectAgainstElectronTightMVA5  = '{object}.tauID("againstElectronTightMVA5")',
    
    objectAgainstElectronVLooseMVA6 = '{object}.tauID("againstElectronVLooseMVA6")', 
    objectAgainstElectronLooseMVA6  = '{object}.tauID("againstElectronLooseMVA6")',
    objectAgainstElectronMediumMVA6 = '{object}.tauID("againstElectronMediumMVA6")',
    objectAgainstElectronTightMVA6  = '{object}.tauID("againstElectronTightMVA6")',

    objectAgainstElectronMVA5category = '{object}.tauID("againstElectronMVA5category")',
    objectAgainstElectronMVA5raw      = '{object}.tauID("againstElectronMVA5raw")',

    # Against Muon
#    objectAgainstMuonLoose  = '{object}.tauID("againstMuonLoose")',
#    objectAgainstMuonMedium = '{object}.tauID("againstMuonMedium")',
#    objectAgainstMuonTight  = '{object}.tauID("againstMuonTight")',
    
#    objectAgainstMuonLoose2  = '{object}.tauID("againstMuonLoose2")',
#    objectAgainstMuonMedium2 = '{object}.tauID("againstMuonMedium2")',
#    objectAgainstMuonTight2  = '{object}.tauID("againstMuonTight2")',
    
    objectAgainstMuonLoose3 = '{object}.tauID("againstMuonLoose3")',
    objectAgainstMuonTight3 = '{object}.tauID("againstMuonTight3")',
    
#    objectAgainstMuonLooseMVA  = '{object}.tauID("againstMuonLooseMVA")',
#    objectAgainstMuonMediumMVA = '{object}.tauID("againstMuonMediumMVA")',
#    objectAgainstMuonTightMVA  = '{object}.tauID("againstMuonTightMVA")',
    
#    objectAgainstMuonMVAraw = '{object}.tauID("againstMuonMVAraw")',

    # combined isolation DB corr 3 hits
    objectByLooseCombinedIsolationDeltaBetaCorr3Hits = '{object}.tauID("byLooseCombinedIsolationDeltaBetaCorr3Hits")',
    objectByMediumCombinedIsolationDeltaBetaCorr3Hits = '{object}.tauID("byMediumCombinedIsolationDeltaBetaCorr3Hits")', 
    objectByTightCombinedIsolationDeltaBetaCorr3Hits = '{object}.tauID("byTightCombinedIsolationDeltaBetaCorr3Hits")',
    objectByCombinedIsolationDeltaBetaCorrRaw3Hits = '{object}.tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits")',
    
    # new tau isolation discriminator with dR = 0.3
    objectByLooseCombinedIsolationDeltaBetaCorr3HitsdR03 = '{object}.tauID("byLooseCombinedIsolationDeltaBetaCorr3HitsdR03")',
    objectByMediumCombinedIsolationDeltaBetaCorr3HitsdR03 = '{object}.tauID("byMediumCombinedIsolationDeltaBetaCorr3HitsdR03")', 
    objectByTightCombinedIsolationDeltaBetaCorr3HitsdR03 = '{object}.tauID("byTightCombinedIsolationDeltaBetaCorr3HitsdR03")',

    objectByLooseIsolationMVArun2v1DBdR03oldDMwLT = '{object}.tauID("byLooseIsolationMVArun2v1DBdR03oldDMwLT")',
    objectByMediumIsolationMVArun2v1DBdR03oldDMwLT = '{object}.tauID("byMediumIsolationMVArun2v1DBdR03oldDMwLT")', 
    objectByTightIsolationMVArun2v1DBdR03oldDMwLT = '{object}.tauID("byTightIsolationMVArun2v1DBdR03oldDMwLT")',
    objectByVTightIsolationMVArun2v1DBdR03oldDMwLT = '{object}.tauID("byVTightIsolationMVArun2v1DBdR03oldDMwLT")',

    # BDT based tau ID discriminator based on isolation Pt sums plus tau lifetime information, trained on 1-prong, "2-prong" and 3-prong tau candidates 
    objectByVLooseIsolationMVArun2v1DBnewDMwLT = '{object}.tauID("byVLooseIsolationMVArun2v1DBnewDMwLT")',
    objectByLooseIsolationMVArun2v1DBnewDMwLT = '{object}.tauID("byLooseIsolationMVArun2v1DBnewDMwLT")',
    objectByMediumIsolationMVArun2v1DBnewDMwLT = '{object}.tauID("byMediumIsolationMVArun2v1DBnewDMwLT")', 
    objectByTightIsolationMVArun2v1DBnewDMwLT = '{object}.tauID("byTightIsolationMVArun2v1DBnewDMwLT")',
    objectByVTightIsolationMVArun2v1DBnewDMwLT = '{object}.tauID("byVTightIsolationMVArun2v1DBnewDMwLT")', 
        
    # BDT based tau ID discriminator based on isolation Pt sums plus tau lifetime information, trained on 1-prong and 3-prong tau candidates 
    objectByVLooseIsolationMVArun2v1DBoldDMwLT = '{object}.tauID("byVLooseIsolationMVArun2v1DBoldDMwLT")', 
    objectByLooseIsolationMVArun2v1DBoldDMwLT = '{object}.tauID("byLooseIsolationMVArun2v1DBoldDMwLT")', 
    objectByMediumIsolationMVArun2v1DBoldDMwLT = '{object}.tauID("byMediumIsolationMVArun2v1DBoldDMwLT")', 
    objectByTightIsolationMVArun2v1DBoldDMwLT = '{object}.tauID("byTightIsolationMVArun2v1DBoldDMwLT")', 
    objectByVTightIsolationMVArun2v1DBoldDMwLT = '{object}.tauID("byVTightIsolationMVArun2v1DBoldDMwLT")', 
    
    # DecayModeFinding
    objectDecayModeFinding       = '{object}.tauID("decayModeFinding")',
    objectDecayModeFindingNewDMs = '{object}.tauID("decayModeFindingNewDMs")',

    objectNeutralIsoPtSum = '{object}.tauID("neutralIsoPtSum")',
    objectChargedIsoPtSum = '{object}.tauID("chargedIsoPtSum")',
    objectPuCorrPtSum     = '{object}.tauID("puCorrPtSum")',

)

TNT_request = PSet(
#     object_nProngs = '{object}.signalChargedHadrCands().size()',
#     object_leadChargedCandPt = '{object}.leadChargedHadrCand().hadTauLeadChargedCand().isNonnull() ? {object}.leadChargedHadrCand().hadTauLeadChargedCand().pt() : -9999.',    
#     object_leadChargedCandEta = '{object}.leadChargedHadrCand().hadTauLeadChargedCand().isNonnull() ? {object}.leadChargedHadrCand().hadTauLeadChargedCand().eta() : -9999.',    
#     object_leadChargedCandPhi = '{object}.leadChargedHadrCand().hadTauLeadChargedCand().isNonnull() ? {object}.leadChargedHadrCand().hadTauLeadChargedCand().phi() : -9999.',
#     object_leadChargedCandCharge = '{object}.leadChargedHadrCand().hadTauLeadChargedCand().isNonnull() ? {object}.leadChargedHadrCand().hadTauLeadChargedCand().charge() : -2.',    
#     object_leadChargedCandChi2 = '{object}.leadTrack().isNonnull() ? {object}.leadTrack().chi2() : -9999.',
#     object_leadChargedCandValidHits = '{object}.leadTrack().isNonnull() ? {object}.leadTrack().numberOfValidHits() : -9999.',
#     object_leadChargedCandDxyError = '{object}.leadTrack().isNonnull() ? {object}.leadTrack().d0Error() : -9999.',
#     object_leadChargedCandDzError = '{object}.leadTrack().isNonnull() ? {object}.leadTrack().dzError() : -9999.',
#     object_leadChargedCandNdof = '{object}.leadTrack().isNonnull() ? {object}.leadTrack().ndof() : -9999.',
#     object_leadChargedCandVtx = '{object}.leadTrack().isNonnull() ? {object}.leadTrack().vx() : -9999.',
#     object_leadChargedCandVty = '{object}.leadTrack().isNonnull() ? {object}.leadTrack().vy() : -9999.',
#     object_leadChargedCandVtz = '{object}.leadTrack().isNonnull() ? {object}.leadTrack().vz() : -9999.',
#     object_leadChargedCandTrack_pt = '{object}.leadTrack().isNonnull() ? {object}.leadTrack().pt() : -9999.',
#     object_leadChargedCandTrack_ptError = '{object}.leadTrack().isNonnull() ? {object}.leadTrack().ptError() : -9999.',

    object_leadChargedCandDxy_pv = '{object}.userFloat("_leadChargedCandDxy_pv")',
    object_leadChargedCandDxy_bs = '{object}.userFloat("_leadChargedCandDxy_bs")',
    object_leadChargedCandDz_pv = '{object}.userFloat("_leadChargedCandDz_pv")',
    object_leadChargedCandDz_bs = '{object}.userFloat("_leadChargedCandDz_bs")',

    #default tau POG lifetime variables
    object_defaultDxy = '{object}.dxy()',
    object_defaultDxyError = '{object}.dxy_error()',
    object_defaultDxySig = '{object}.dxy_Sig()',
    object_defaultFlightLengthX = '{object}.flightLength().x()',
    object_defaultFlightLengthY = '{object}.flightLength().y()',
    object_defaultFlightLengthZ = '{object}.flightLength().z()',
    object_defaultFlightLengthSig = '{object}.flightLengthSig()',
    object_default_PCAx_pv = '{object}.dxy_PCA().x()',
    object_default_PCAy_pv = '{object}.dxy_PCA().y()',
    object_default_PCAz_pv = '{object}.dxy_PCA().z()',

    object_leadChargedCandTrack_PCAx_bs = '{object}.userFloat("_leadChargedCandTrack_PCAx_bs")',
    object_leadChargedCandTrack_PCAy_bs = '{object}.userFloat("_leadChargedCandTrack_PCAy_bs")',
    object_leadChargedCandTrack_PCAz_bs = '{object}.userFloat("_leadChargedCandTrack_PCAz_bs")',
    object_leadChargedCandTrack_PCAx_pv = '{object}.userFloat("_leadChargedCandTrack_PCAx_pv")',
    object_leadChargedCandTrack_PCAy_pv = '{object}.userFloat("_leadChargedCandTrack_PCAy_pv")',
    object_leadChargedCandTrack_PCAz_pv = '{object}.userFloat("_leadChargedCandTrack_PCAz_pv")',

    object_leadChargedCandTrackFitErrorMatrix_00 = '{object}.userFloat("_leadChargedCandTrackFitErrorMatrix_00")',
    object_leadChargedCandTrackFitErrorMatrix_01 = '{object}.userFloat("_leadChargedCandTrackFitErrorMatrix_01")',
    object_leadChargedCandTrackFitErrorMatrix_02 = '{object}.userFloat("_leadChargedCandTrackFitErrorMatrix_02")',
    object_leadChargedCandTrackFitErrorMatrix_11 = '{object}.userFloat("_leadChargedCandTrackFitErrorMatrix_11")',
    object_leadChargedCandTrackFitErrorMatrix_12 = '{object}.userFloat("_leadChargedCandTrackFitErrorMatrix_12")',
    object_leadChargedCandTrackFitErrorMatrix_22 = '{object}.userFloat("_leadChargedCandTrackFitErrorMatrix_22")',

)

trigger = PSet(
    objectTau20 = 'matchToHLTFilter({object_idx}, "hltPFTau20TrackLooseIso", 0.5)',
    objectTauOverlapEle = 'matchToHLTFilter({object_idx}, "hltOverlapFilterIsoEle22WP75GsfLooseIsoPFTau20", 0.5)',
    objectTauOverlapEleLoose = 'matchToHLTFilter({object_idx}, "hltOverlapFilterIsoEle22WPLooseGsfLooseIsoPFTau20", 0.5)',
    objectTau20AgainstMuon = 'matchToHLTFilter({object_idx}, "hltPFTau20TrackLooseIsoAgainstMuon", 0.5)',
    objectTauOverlapMu = 'matchToHLTFilter({object_idx}, "hltOverlapFilterIsoMu17LooseIsoPFTau20", 0.5)',
    objectDiTauJet = 'matchToHLTFilter({object_idx}, "hltL1sDoubleTauJet36erORDoubleTauJet68er", 0.5)',
    objectDiIsoTau = 'matchToHLTFilter({object_idx}, "hltDoubleL2IsoTau35eta2p1", 0.5)',
    objectDiPFTau40 = 'matchToHLTFilter({object_idx}, "hltDoublePFTau40TrackPt1MediumIsolationDz02Reg", 0.5)',
    objectDiPFTau35 = 'matchToHLTFilter({object_idx}, "hltDoublePFTau35TrackPt1MediumIsolationDz02Reg", 0.5)',

)
veto = PSet(
    objectElectronVeto = 'veto3rdLepton({object_idx}, 0.0, "pt > 10 & abs(eta) < 2.5 & userFloat(\'MVANonTrigWP90\') > 0.5 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'ipDXY\')) < 0.045   & abs(userFloat(\'relIso\')) < 0.3", "electron").size()',
    objectMuonVeto = 'veto3rdLepton({object_idx}, 0.0, "pt > 10 & abs(eta) < 2.4 & isMediumMuon > 0.5 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'ipDXY\')) < 0.045  & abs(userFloat(\'relIso\')) < 0.3", "muon").size()',
)
