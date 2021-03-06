'''

Ntuple branch template sets for applying cleaning and extra object vetoes

Each string is transformed into an expression on a FinalStateEvent object.

{object} should be replaced by an expression which evaluates to a pat::Muon
i.e. daughter(1) or somesuch.

Author: Evan K. Friis

'''

from FinalStateAnalysis.Utilities.cfgtools import PSet

# Vetos on extra stuff in the event
vetos = PSet(
    #MUON VETOS
    extramuon_veto = 'vetoMuons(0.0, "pt > 10 & abs(eta) < 2.4 & userInt(\'mediumID\') > 0.5 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'ipDXY\')) < 0.045  & (chargedHadronIso + max(photonIso + neutralHadronIso - 0.5*puChargedHadronIso, 0))/pt < 0.3").size()',
    extramuon_veto_ptEta = 'vetoMuons(0.0, "pt > 10 & abs(eta) < 2.4").size()',
    extramuon_veto_ID = 'vetoMuons(0.0, "pt > 10 & abs(eta) < 2.4 & userInt(\'mediumID\') > 0.5").size()',
    extramuon_veto_dXYZ = 'vetoMuons(0.0, "pt > 10 & abs(eta) < 2.4 & userInt(\'mediumID\') > 0.5 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'ipDXY\')) < 0.045").size()',

    extramuon_veto_user = 'vetoMuons(0.0, "pt > 10 & abs(eta) < 2.4 & userInt(\'mediumID\') > 0.5 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'ipDXY\')) < 0.045  & (userIso(0) + max(photonIso + neutralHadronIso - 0.5*puChargedHadronIso, 0))/pt < 0.3").size()',
    extramuon_veto_015 = 'vetoMuons(0.0, "pt > 10 & abs(eta) < 2.4 & userInt(\'mediumID\') > 0.5 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'ipDXY\')) < 0.045  & (chargedHadronIso + max(photonIso + neutralHadronIso - 0.5*puChargedHadronIso, 0))/pt < 0.15").size()',

#     muGlbIsoVetoPt10 = 'vetoMuons(0.4, "isGlobalMuon & isTrackerMuon & pt > 10 & abs(eta) < 2.4 & (userIso(0) + max(photonIso + neutralHadronIso - 0.5*puChargedHadronIso, 0))/pt < 0.4").size()',
#     muVetoPt5IsoIdVtx = 'vetoMuons(0.4, "pt > 5 & abs(eta) < 2.4 & userInt(\'tightID\') > 0.5 & ((userIso(0) + max(photonIso()+neutralHadronIso()-0.5*puChargedHadronIso,0.0))/pt()) < 0.15 & userFloat(\'dz\') < 0.2").size()',
#     muVetoPt15IsoIdVtx = 'vetoMuons(0.4, "pt > 15 & abs(eta) < 2.4 & userInt(\'tightID\') > 0.5 & ((userIso(0) + max(photonIso()+neutralHadronIso()-0.5*puChargedHadronIso,0.0))/pt()) < 0.15 & userFloat(\'dz\') < 0.2").size()',
    
    #TAU VETOS
    #OLD DMs
#     tauVetoPt20Loose3HitsVtx = 'vetoTaus(0.4, "pt > 20 & abs(eta) < 2.5 & tauID(\'decayModeFinding\') & tauID(\'byLooseCombinedIsolationDeltaBetaCorr3Hits\') & userFloat(\'dz\') < 0.2").size()',
#     tauVetoPt20VLooseHPSVtx  = 'vetoTaus(0.4, "pt > 20 & abs(eta) < 2.5 & tauID(\'decayModeFinding\') & tauID(\'byVLooseCombinedIsolationDeltaBetaCorr\') & userFloat(\'dz\') < 0.2").size()',
#     tauVetoPt20TightMVALTVtx = 'vetoTaus(0.4, "pt > 20 & abs(eta) < 2.5 & tauID(\'decayModeFinding\') & tauID(\'byTightIsolationMVA3oldDMwLT\') & userFloat(\'dz\') < 0.2").size()',
#     tauVetoPt20TightMVAVtx   = 'vetoTaus(0.4, "pt > 20 & abs(eta) < 2.5 & tauID(\'decayModeFinding\') & tauID(\'byTightIsolationMVA3oldDMwoLT\') & userFloat(\'dz\') < 0.2").size()',

    #NEW DMs
#     tauVetoPt20Loose3HitsNewDMVtx = 'vetoTaus(0.4, "pt > 20 & abs(eta) < 2.5 & tauID(\'decayModeFindingNewDMs\') & tauID(\'byLooseCombinedIsolationDeltaBetaCorr3Hits\') & userFloat(\'dz\') < 0.2").size()',
#     tauVetoPt20VLooseHPSNewDMVtx  = 'vetoTaus(0.4, "pt > 20 & abs(eta) < 2.5 & tauID(\'decayModeFindingNewDMs\') & tauID(\'byVLooseCombinedIsolationDeltaBetaCorr\') & userFloat(\'dz\') < 0.2").size()',
#     tauVetoPt20TightMVALTNewDMVtx = 'vetoTaus(0.4, "pt > 20 & abs(eta) < 2.5 & tauID(\'decayModeFinding\') & tauID(\'byTightIsolationMVA3newDMwLT\') & userFloat(\'dz\') < 0.2").size()',
#     tauVetoPt20TightMVANewDMVtx   = 'vetoTaus(0.4, "pt > 20 & abs(eta) < 2.5 & tauID(\'decayModeFinding\') & tauID(\'byTightIsolationMVA3newDMwoLT\') & userFloat(\'dz\') < 0.2").size()',
    
    #ELECTRON VETOS
#     extraelec_veto = 'vetoElectrons(0., "pt > 10 & abs(eta) < 2.5 & userFloat(\'CBIDMedium\') > 0.5 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'ipDXY\')) < 0.045  & (chargedHadronIso + max(photonIso + neutralHadronIso - 0.5*puChargedHadronIso, 0))/pt < 0.3").size()',
    extraelec_veto_user = 'vetoElectrons(0., "pt > 10 & abs(eta) < 2.5 & userFloat(\'CBIDVeto\') > 0.5 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'ipDXY\')) < 0.045 & (userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt < 0.3").size()',
    extraelec_veto = 'vetoElectrons(0., "pt > 10 & abs(eta) < 2.5 & userFloat(\'CBIDVeto\') > 0.5 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'ipDXY\')) < 0.045 & (chargedHadronIso + max(photonIso + neutralHadronIso - 0.5*puChargedHadronIso, 0))/pt < 0.3").size()',
    extraelec_veto_ptEta = 'vetoElectrons(0., "pt > 10 & abs(eta) < 2.5").size()',
    extraelec_veto_ID = 'vetoElectrons(0., "pt > 10 & abs(eta) < 2.5 & userFloat(\'CBIDVeto\') > 0.5").size()',
    extraelec_veto_dXYZ = 'vetoElectrons(0., "pt > 10 & abs(eta) < 2.5 & userFloat(\'CBIDVeto\') > 0.5 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'ipDXY\')) < 0.045").size()',

    extraelec_veto_015 = 'vetoElectrons(0., "pt > 10 & abs(eta) < 2.5 & userFloat(\'CBIDVeto\') > 0.5 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'ipDXY\')) < 0.045 & (chargedHadronIso + max(photonIso + neutralHadronIso - 0.5*puChargedHadronIso, 0))/pt < 0.3").size()',
    extraelec_veto_01 = 'vetoElectrons(0., "pt > 10 & abs(eta) < 2.5 & userFloat(\'CBIDVeto\') > 0.5 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'ipDXY\')) < 0.045 & (chargedHadronIso + max(photonIso + neutralHadronIso - 0.5*puChargedHadronIso, 0))/pt < 0.3").size()',

#     eVetoMVAIsoVtx = 'vetoElectrons(0.4, "pt > 10 & abs(eta) < 2.5 & userInt(\'mvaidwp\') > 0.5 & ((userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt) < 0.3 & userFloat(\'dz\') < 0.2").size()',
#     eVetoMVAIso = 'vetoElectrons(0.4, "pt > 10 & abs(eta) < 2.5 & userInt(\'mvaidwp\') > 0.5 & (userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt < 0.3").size()',
#     eVetoCicTightIso = 'vetoElectrons(0.4, "pt > 10 & abs(eta) < 2.5 &  test_bit(electronID(\'cicTight\'), 0) > 0.5 & (userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt < 0.3").size()',
    
    #B-JET Vetos
#     bjetVeto = 'vetoJets(0.4, "pt > 20 & abs(eta) < 2.4  & bDiscriminator(\'\') > 3.3").size()',
#     bjetCSVVeto = 'vetoJets(0.4, "pt > 20 & abs(eta) < 2.4 & bDiscriminator(\'combinedSecondaryVertexBJetTags\') > 0.679").size()',
#     bjetCSVVetoZHLike = 'vetoJets(0.4, "pt > 20 & abs(eta) < 2.4 &  bDiscriminator(\'combinedSecondaryVertexBJetTags\') > 0.898").size()',
#     bjetCSVVetoZHLikeNoJetId = 'vetoJets(0.4, "pt > 20 & abs(eta) < 2.4 & bDiscriminator(\'combinedSecondaryVertexBJetTags\') > 0.898").size()',
#     bjetCSVVeto30 = 'vetoJets(0.4, "pt > 30 & abs(eta) < 2.4 & bDiscriminator(\'combinedSecondaryVertexBJetTags\') > 0.679").size()',

    #JET VETOS
#     jetVeto20 = 'vetoJets(0.4, "pt > 20 & abs(eta) < 5.0").size()',
#     jetVeto20_DR05 = 'vetoJets(0.5, "pt > 20 & abs(eta) < 5.0").size()',
#     jetVeto30 = 'vetoJets(0.4, "pt > 30 & abs(eta) < 5.0").size()',
#     jetVeto30_DR05 = 'vetoJets(0.5, "pt > 30 & abs(eta) < 5.0").size()',
#     jetVeto40 = 'vetoJets(0.4, "pt > 40 & abs(eta) < 5.0").size()',
#     jetVeto40_DR05 = 'vetoJets(0.5, "pt > 40 & abs(eta) < 5.0").size()',
    #leadingJetPt = '? (vetoJets(0.4, "abs(eta) < 5.0 & userInt(\'fullIdLoose\')").size() > 0) ? vetoJets(0.4, "abs(eta) < 5.0 & userInt(\'fullIdLoose\')").at(0).pt() : -1.',
)

overlaps = PSet(
    objectElectronPt15IdIsoVtxOverlap = 'overlapElectrons({object_idx}, 0.4, "pt > 15 & abs(eta) < 2.5 & userInt(\'mvaidwp\') > 0.5 & ((userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt) < 0.3 & abs(userFloat(\'dz\')) < 0.2").size()', 
    objectElectronPt10IdIsoVtxOverlap = 'overlapElectrons({object_idx}, 0.4, "pt > 10 & abs(eta) < 2.5 & userInt(\'mvaidwp\') > 0.5 & ((userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt) < 0.3 & abs(userFloat(\'dz\')) < 0.2").size()', 
    objectElectronPt15IdVtxOverlap = 'overlapElectrons({object_idx}, 0.4, "pt > 15 & abs(eta) < 2.5 & userInt(\'mvaidwp\') > 0.5 & abs(userFloat(\'dz\')) < 0.2").size()',
    objectElectronPt10IdVtxOverlap = 'overlapElectrons({object_idx}, 0.4, "pt > 10 & abs(eta) < 2.5 & userInt(\'mvaidwp\') > 0.5 & abs(userFloat(\'dz\')) < 0.2").size()',
   
    objectMuonIdIsoVtxOverlap = 'overlapMuons({object_idx}, 0.4, "pt > 10 & abs(eta) < 2.4 & userInt(\'tightID\') > 0.5 & ((userIso(0) + max(photonIso()+neutralHadronIso()-0.5*puChargedHadronIso,0.0))/pt()) < 0.15 & userFloat(\'dz\') < 0.2").size()',
    objectMuonIdVtxOverlap = 'overlapMuons({object_idx}, 0.4, "pt > 10 & abs(eta) < 2.4 & userInt(\'tightID\') > 0.5 & userFloat(\'dz\') < 0.2").size()',
    objectMuonIdIsoStdVtxOverlap = 'overlapMuons({object_idx}, 0.4, "pt > 10 & abs(eta) < 2.4 & userInt(\'tightID\') > 0.5 & ((chargedHadronIso() + max(photonIso()+neutralHadronIso()-0.5*puChargedHadronIso,0.0))/pt()) < 0.15 & userFloat(\'dz\') < 0.2").size()',
    objectGlobalMuonVtxOverlap = 'overlapMuons({object_idx}, 0.4, "pt > 10 & abs(eta) < 2.4 & isGlobalMuon & userFloat(\'dz\') < 0.2").size()',

    objectMuOverlap = 'overlapMuons({object_idx}, 0.4, "pt > 5").size()',
    objectElecOverlap = 'overlapElectrons({object_idx}, 0.4, "pt > 10").size()',
    objectCiCTightElecOverlap = 'overlapElectrons({object_idx}, 0.4, "pt > 10 & test_bit(electronID(\'cicTight\'), 0)").size()',
)
