
'''

Ntuple branch template sets for tau objects.

Each string is transformed into an expression on a FinalStateEvent object.

{object} should be replaced by an expression which evaluates to a pat::Muon
i.e. daughter(1) or somesuch.

Author: Evan K. Friis

'''

from FinalStateAnalysis.Utilities.cfgtools import PSet

info = PSet(
    objectGenDecayMode = '{object}.userInt("genDecayMode")',
    objectLeadTrackPt = '{object}.userFloat("ps_ldTrkPt")',
    objectDecayMode = '{object}.decayMode',
    objectTNPId = '{object}.userInt("ps_sel_nom")',

    # gen matching
#     objectPdgId = '? ({object}.genParticleRef().isNonnull && {object}.genParticleRef().isAvailable) ? {object}.genParticleRef().pdgId() : -999',
#     objectComesFromHiggs = 'comesFromHiggs({object_idx},15,0)',
#     objectGenPt = '? ({object}.genParticleRef().isNonnull && {object}.genParticleRef().isAvailable) ? {object}.genParticleRef().pt() : -999',
#     objectGenEta = '? ({object}.genParticleRef().isNonnull && {object}.genParticleRef().isAvailable) ? {object}.genParticleRef().eta() : -999',
#     objectGenPhi = '? ({object}.genParticleRef().isNonnull && {object}.genParticleRef().isAvailable) ? {object}.genParticleRef().phi() : -999',
#     objectGenMass = '? ({object}.genParticleRef().isNonnull && {object}.genParticleRef().isAvailable) ? {object}.genParticleRef().mass() : -999',
    objectGenPdgId       = '? (getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).pdgId() : -999',
    objectGenCharge      = '? (getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).charge() : -999',
    objectGenEnergy      = '? (getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).energy() : -999',
    objectGenEta         = '? (getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).eta()   : -999',
    objectGenPhi         = '? (getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).phi()   : -999',
    objectGenPt          = '? (getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).pt()   : -999',
    objectGenMass        = '? (getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).mass()   : -999',

    objectGenVisPt       = '? getDaughterGenParticleVisMomentum({object_idx}, 15, 1, 1.0, 0.5).pt() > 0 ? getDaughterGenParticleVisMomentum({object_idx}, 15, 1, 1.0, 0.5).pt()  : -999',
    objectGenVisEta       = '? getDaughterGenParticleVisMomentum({object_idx}, 15, 1, 1.0, 0.5).pt() > 0 ? getDaughterGenParticleVisMomentum({object_idx}, 15, 1, 1.0, 0.5).eta()  : -999',
    objectGenVisPhi       = '? getDaughterGenParticleVisMomentum({object_idx}, 15, 1, 1.0, 0.5).pt() > 0 ? getDaughterGenParticleVisMomentum({object_idx}, 15, 1, 1.0, 0.5).phi()  : -999',
    objectGenVisMass       = '? getDaughterGenParticleVisMomentum({object_idx}, 15, 1, 1.0, 0.5).pt() > 0 ? getDaughterGenParticleVisMomentum({object_idx}, 15, 1, 1.0, 0.5).mass()  : -999',

    objectGenNuPt       = '? getGenParticleNuMomentum({object_idx}, 15, 1, 1.0, 0.5).pt() > 0 ? getGenParticleNuMomentum({object_idx}, 15, 1, 1.0, 0.5).pt()  : -999',
    objectGenNuEta       = '? getGenParticleNuMomentum({object_idx}, 15, 1, 1.0, 0.5).pt() > 0 ? getGenParticleNuMomentum({object_idx}, 15, 1, 1.0, 0.5).eta()  : -999',
    objectGenNuPhi       = '? getGenParticleNuMomentum({object_idx}, 15, 1, 1.0, 0.5).pt() > 0 ? getGenParticleNuMomentum({object_idx}, 15, 1, 1.0, 0.5).phi()  : -999',
    objectGenNuMass       = '? getGenParticleNuMomentum({object_idx}, 15, 1, 1.0, 0.5).pt() > 0 ? getGenParticleNuMomentum({object_idx}, 15, 1, 1.0, 0.5).mass()  : -999',
)

# ID and isolation
id = PSet(
    # updated for what is included in PHYS14 MiniAOD
    # TODO: update when new IDs are released: https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePFTauID#Tau_ID_2014_preparation_for_AN1
    # Against Electron
    objectAgainstElectronLoose  = '{object}.tauID("againstElectronLoose")',
    objectAgainstElectronMedium = '{object}.tauID("againstElectronMedium")',
    objectAgainstElectronTight  = '{object}.tauID("againstElectronTight")',
    
    objectAgainstElectronVLooseMVA5 = '{object}.tauID("againstElectronVLooseMVA5")', 
    objectAgainstElectronLooseMVA5  = '{object}.tauID("againstElectronLooseMVA5")',
    objectAgainstElectronMediumMVA5 = '{object}.tauID("againstElectronMediumMVA5")',
    objectAgainstElectronTightMVA5  = '{object}.tauID("againstElectronTightMVA5")',
    objectAgainstElectronVTightMVA5 = '{object}.tauID("againstElectronVTightMVA5")',
    
    objectAgainstElectronMVA5category = '{object}.tauID("againstElectronMVA5category")',
    objectAgainstElectronMVA5raw      = '{object}.tauID("againstElectronMVA5raw")',

    # Against Muon
    objectAgainstMuonLoose  = '{object}.tauID("againstMuonLoose")',
    objectAgainstMuonMedium = '{object}.tauID("againstMuonMedium")',
    objectAgainstMuonTight  = '{object}.tauID("againstMuonTight")',
    
    objectAgainstMuonLoose2  = '{object}.tauID("againstMuonLoose2")',
    objectAgainstMuonMedium2 = '{object}.tauID("againstMuonMedium2")',
    objectAgainstMuonTight2  = '{object}.tauID("againstMuonTight2")',
    
    objectAgainstMuonLoose3 = '{object}.tauID("againstMuonLoose3")',
    objectAgainstMuonTight3 = '{object}.tauID("againstMuonTight3")',
    
    objectAgainstMuonLooseMVA  = '{object}.tauID("againstMuonLooseMVA")',
    objectAgainstMuonMediumMVA = '{object}.tauID("againstMuonMediumMVA")',
    objectAgainstMuonTightMVA  = '{object}.tauID("againstMuonTightMVA")',
    
    objectAgainstMuonMVAraw = '{object}.tauID("againstMuonMVAraw")',

    # combined isolation DB corr 3 hits
    objectByLooseCombinedIsolationDeltaBetaCorr3Hits = '{object}.tauID("byLooseCombinedIsolationDeltaBetaCorr3Hits")',
    objectByMediumCombinedIsolationDeltaBetaCorr3Hits = '{object}.tauID("byMediumCombinedIsolationDeltaBetaCorr3Hits")', 
    objectByTightCombinedIsolationDeltaBetaCorr3Hits = '{object}.tauID("byTightCombinedIsolationDeltaBetaCorr3Hits")',
    objectByCombinedIsolationDeltaBetaCorrRaw3Hits = '{object}.tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits")',
    
    # BDT based tau ID discriminator based on isolation Pt sums plus tau lifetime information, trained on 1-prong, "2-prong" and 3-prong tau candidates 
    objectByVLooseIsolationMVA3newDMwLT = '{object}.tauID("byVLooseIsolationMVA3newDMwLT")',
    objectByLooseIsolationMVA3newDMwLT = '{object}.tauID("byLooseIsolationMVA3newDMwLT")',
    objectByMediumIsolationMVA3newDMwLT = '{object}.tauID("byMediumIsolationMVA3newDMwLT")', 
    objectByTightIsolationMVA3newDMwLT = '{object}.tauID("byTightIsolationMVA3newDMwLT")',
    objectByVTightIsolationMVA3newDMwLT = '{object}.tauID("byVTightIsolationMVA3newDMwLT")', 
    objectByVVTightIsolationMVA3newDMwLT = '{object}.tauID("byVVTightIsolationMVA3newDMwLT")', 
    objectByIsolationMVA3newDMwLTraw = '{object}.tauID("byIsolationMVA3newDMwLTraw")',
    
    # BDT based tau ID discriminator based on isolation Pt sums, trained on 1-prong, "2-prong" and 3-prong tau candidates 
    objectByVLooseIsolationMVA3newDMwoLT = '{object}.tauID("byVLooseIsolationMVA3newDMwoLT")', 
    objectByLooseIsolationMVA3newDMwoLT = '{object}.tauID("byLooseIsolationMVA3newDMwoLT")', 
    objectByMediumIsolationMVA3newDMwoLT = '{object}.tauID("byMediumIsolationMVA3newDMwoLT")', 
    objectByTightIsolationMVA3newDMwoLT = '{object}.tauID("byTightIsolationMVA3newDMwoLT")', 
    objectByVTightIsolationMVA3newDMwoLT = '{object}.tauID("byVTightIsolationMVA3newDMwoLT")', 
    objectByVVTightIsolationMVA3newDMwoLT = '{object}.tauID("byVVTightIsolationMVA3newDMwoLT")',
    objectByIsolationMVA3newDMwoLTraw = '{object}.tauID("byIsolationMVA3newDMwoLTraw")', 
    
    # BDT based tau ID discriminator based on isolation Pt sums plus tau lifetime information, trained on 1-prong and 3-prong tau candidates 
    objectByVLooseIsolationMVA3oldDMwLT = '{object}.tauID("byVLooseIsolationMVA3oldDMwLT")', 
    objectByLooseIsolationMVA3oldDMwLT = '{object}.tauID("byLooseIsolationMVA3oldDMwLT")', 
    objectByMediumIsolationMVA3oldDMwLT = '{object}.tauID("byMediumIsolationMVA3oldDMwLT")', 
    objectByTightIsolationMVA3oldDMwLT = '{object}.tauID("byTightIsolationMVA3oldDMwLT")', 
    objectByVTightIsolationMVA3oldDMwLT = '{object}.tauID("byVTightIsolationMVA3oldDMwLT")', 
    objectByVVTightIsolationMVA3oldDMwLT = '{object}.tauID("byVVTightIsolationMVA3oldDMwLT")',
    objectByIsolationMVA3oldDMwLTraw = '{object}.tauID("byIsolationMVA3oldDMwLTraw")', 
    
    # BDT based tau ID discriminator based on isolation Pt sums, trained on 1-prong and 3-prong tau candidates 
    objectByVLooseIsolationMVA3oldDMwoLT = '{object}.tauID("byVLooseIsolationMVA3oldDMwoLT")', 
    objectByLooseIsolationMVA3oldDMwoLT = '{object}.tauID("byLooseIsolationMVA3oldDMwoLT")', 
    objectByMediumIsolationMVA3oldDMwoLT = '{object}.tauID("byMediumIsolationMVA3oldDMwoLT")', 
    objectByTightIsolationMVA3oldDMwoLT = '{object}.tauID("byTightIsolationMVA3oldDMwoLT")', 
    objectByVTightIsolationMVA3oldDMwoLT = '{object}.tauID("byVTightIsolationMVA3oldDMwoLT")', 
    objectByVVTightIsolationMVA3oldDMwoLT = '{object}.tauID("byVVTightIsolationMVA3oldDMwoLT")',
    objectByIsolationMVA3oldDMwoLTraw = '{object}.tauID("byIsolationMVA3oldDMwoLTraw")', 

    # DecayModeFinding
    objectDecayModeFinding       = '{object}.tauID("decayModeFinding")',
    objectDecayModeFindingNewDMs = '{object}.tauID("decayModeFindingNewDMs")',

    objectNeutralIsoPtSum = '{object}.tauID("neutralIsoPtSum")',
    objectChargedIsoPtSum = '{object}.tauID("chargedIsoPtSum")',
    objectPuCorrPtSum     = '{object}.tauID("puCorrPtSum")',
)


trigger = PSet(
    objectTau20 = 'matchToHLTFilter({object_idx}, "hltPFTau20TrackLooseIso", 0.5)',
    objectTauOverlapEle = 'matchToHLTFilter({object_idx}, "hltOverlapFilterIsoEle22WP75GsfLooseIsoPFTau20", 0.5)',
    objectTau20AgainstMuon = 'matchToHLTFilter({object_idx}, "hltPFTau20TrackLooseIsoAgainstMuon", 0.5)',
    objectTauOverlapMu = 'matchToHLTFilter({object_idx}, "hltOverlapFilterIsoMu17LooseIsoPFTau20", 0.5)',
    objectDiTauJet = 'matchToHLTFilter({object_idx}, "hltL1sDoubleTauJet36erORDoubleTauJet68er", 0.5)',
    objectDiIsoTau = 'matchToHLTFilter({object_idx}, "hltDoubleL2IsoTau35eta2p1", 0.5)',
    objectDiPFTau40 = 'matchToHLTFilter({object_idx}, "hltDoublePFTau40TrackPt1MediumIsolationDz02Reg", 0.5)',
)
