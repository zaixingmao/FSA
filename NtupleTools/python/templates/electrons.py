'''

Ntuple branch template sets for electron objects.

Each string is transformed into an expression on a FinalStateEvent object.

{object} should be replaced by an expression which evaluates to a pat::Electron
i.e. daughter(1) or somesuch.

Author: Evan K. Friis

'''

import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.cfgtools import PSet

# ID and isolation
id = PSet(
    # PHYS14 IDs (some of which are still CSA14 IDs...)
    objectCBIDVeto = '{object}.userFloat("CBIDVeto")',
    objectCBIDLoose = '{object}.userFloat("CBIDLoose")',
    objectCBIDMedium = '{object}.userFloat("CBIDMedium")',
    objectCBIDTight = '{object}.userFloat("CBIDTight")',
    objectMVANonTrigWP80 = '{object}.userFloat("MVANonTrigWP80")',
    objectMVANonTrigWP90 = '{object}.userFloat("MVANonTrigWP90")',
#     objectHEEPIDD = '{object}.userFloat("heepElectronID")',
    
    # Use cms.string so we get the parentheses formatting bonus
#     objectRelPFIsoDB = cms.string(
#         "({object}.userIso(0)"
#         "+max({object}.userIso(1)"
#         "+{object}.neutralHadronIso()"
#         "-0.5*{object}.userIso(2),0.0))"
#         "/{object}.pt()"
#     ),
#     objectRelPFIsoRho = cms.string(
#         '({object}.chargedHadronIso()'
#         '+max(0.0,{object}.neutralHadronIso()'
#         '+{object}.photonIso()'
#         '-{object}.userFloat("rhoCSA14")*{object}.userFloat("EffectiveArea_HZZ4l2015")))'
#         '/{object}.pt()'
#     ),
# 
#     objectPFChargedIso = cms.string('{object}.userIsolation("PfChargedHadronIso")'),
#     objectPFNeutralIso = cms.string('{object}.userIsolation("PfNeutralHadronIso")'),
#     objectPFPhotonIso  = cms.string('{object}.userIsolation("PfGammaIso")'),
    
    objectPassNumberOfHits = cms.string('{object}.userInt("passNumberOfHits")'),

    objectEffectiveArea2012Data = cms.string('{object}.userFloat("ea_comb_Data2012_iso04_kt6PFJ")'),
    objectEffectiveAreaPHYS14 = cms.string('{object}.userFloat("EffectiveArea_HZZ4l2015")'),

    objectRho = cms.string('{object}.userFloat("rhoCSA14")'),
    objectRelIso = '{object}.userFloat("relIso")',
    objectTrkIsoDR03 = cms.string("{object}.dr03TkSumPt()"),
    objectEcalIsoDR03 = cms.string("{object}.dr03EcalRecHitSumEt()"),
    objectHcalIsoDR03 = cms.string("{object}.dr03HcalTowerSumEt()"),
    # raw energy error
    objectEnergyError = '{object}.corrections().combinedP4Error',
    # shower shape / ID variables
    objectHadronicOverEM = '{object}.hcalOverEcal',
    objectHadronicDepth1OverEm = '{object}.hcalDepth1OverEcal',
    objectHadronicDepth2OverEm = '{object}.hcalDepth2OverEcal',
    objectSigmaIEtaIEta = '{object}.sigmaIetaIeta',
    objectdeltaEtaSuperClusterTrackAtVtx = '{object}.deltaEtaSuperClusterTrackAtVtx',
    objectdeltaPhiSuperClusterTrackAtVtx = '{object}.deltaPhiSuperClusterTrackAtVtx',
    objectfBrem = '{object}.fbrem',
    objecteSuperClusterOverP = '{object}.eSuperClusterOverP',
    objectecalEnergy = '{object}.ecalEnergy',
    objecttrackMomentumAtVtxP = '{object}.trackMomentumAtVtx.r',
    objectHasMatchedConversion = cms.vstring('{object}.userInt("HasMatchedConversion")','I'),    
    objectE1x5 = '{object}.scE1x5',
    objectE2x5Max = '{object}.scE2x5Max',
    objectE5x5 = '{object}.scE5x5',
    objectNearMuonVeto = 'overlapMuons({object_idx},0.05,"isGlobalMuon() & abs(eta()) < 2.4").size()',
    objectGenMotherPdgId = '? (getDaughterGenParticleMotherSmart({object_idx}, 11, 0).isAvailable && getDaughterGenParticleMotherSmart({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticleMotherSmart({object_idx}, 11, 0).pdgId() : -999',
    objectComesFromHiggs = 'comesFromHiggs({object_idx}, 11, 1)',

    objectGenPdgId       = '? (getDaughterGenParticle({object_idx}, 11, 1, 0.5, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 11, 1, 0.5, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 1, 0.5, 0.5).pdgId() : -999',
    objectGenMass      = '? (getDaughterGenParticle({object_idx}, 11, 1, 0.5, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 11, 1, 0.5, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 1, 0.5, 0.5).mass() : -999',
    objectGenEta         = '? (getDaughterGenParticle({object_idx}, 11, 1, 0.5, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 11, 1, 0.5, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 1, 0.5, 0.5).eta()   : -999',
    objectGenPhi         = '? (getDaughterGenParticle({object_idx}, 11, 1, 0.5, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 11, 1, 0.5, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 1, 0.5, 0.5).phi()   : -999',
    objectGenPt          = '? (getDaughterGenParticle({object_idx}, 11, 1, 0.5, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 11, 1, 0.5, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 1, 0.5, 0.5).pt()   : -999',
    objectGenVZ          = '? (getDaughterGenParticle({object_idx}, 11, 1, 0.5, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 11, 1, 0.5, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 1, 0.5, 0.5).vz()   : -999',
    objectGenVtxPVMatch  = 'genVtxPVMatch({object_idx})', # is PV closest vtx to gen vtx?

    objectGenTauPdgId       = '? (getDaughterGenParticle({object_idx}, 15, 1, 1, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 15, 1, 1, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 1, 1, 0.5).pdgId() : -999',
    objectGenTauMass      = '? (getDaughterGenParticle({object_idx}, 15, 1, 1, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 15, 1, 1, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 1, 1, 0.5).mass() : -999',
    objectGenTauEta         = '? (getDaughterGenParticle({object_idx}, 15, 1, 1, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 15, 1, 1, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 1, 1, 0.5).eta()   : -999',
    objectGenTauPhi         = '? (getDaughterGenParticle({object_idx}, 15, 1, 1, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 15, 1, 1, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 1, 1, 0.5).phi()   : -999',
    objectGenTauPt          = '? (getDaughterGenParticle({object_idx}, 15, 1, 1, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 15, 1, 1, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 1, 1, 0.5).pt()   : -999',
    
    # How close is the nearest muon passing some basic quality cuts?
    objectNearestMuonDR = "electronClosestMuonDR({object_idx})",
)

#variables for life-time
TNT_request = PSet(
    object_gsfTrack_normChi2 = cms.string('{object}.gsfTrack().normalizedChi2()'),
    object_gsfTrack_ndof = cms.string('{object}.gsfTrack().ndof()'),
    object_gsfTrack_vtx = cms.string('{object}.gsfTrack().vx()'),
    object_gsfTrack_vty = cms.string('{object}.gsfTrack().vy()'),
    object_gsfTrack_vtz = cms.string('{object}.gsfTrack().vz()'),
    object_dxy = cms.string('{object}.userFloat("_dxy")'),
    object_dxyError = cms.string('{object}.gsfTrack().d0Error()'),
    object_dz = cms.string('{object}.userFloat("_dz")'),
    object_dxy_bs = cms.string('{object}.userFloat("_dxy_bs")'),
    object_expectedMissingInnerHits = cms.string('{object}.userInt("expectedMissingInnerHits")'),
    object_passConversionVeto = cms.string('{object}.userInt("passConversionVeto")'),

    object_gsfTrack_PCAx_bs = cms.string('{object}.userFloat("_gsfTrack_PCAx_bs")'),
    object_gsfTrack_PCAy_bs = cms.string('{object}.userFloat("_gsfTrack_PCAy_bs")'),
    object_gsfTrack_PCAz_bs = cms.string('{object}.userFloat("_gsfTrack_PCAz_bs")'),
    object_gsfTrack_PCAx_pv = cms.string('{object}.userFloat("_gsfTrack_PCAx_pv")'),
    object_gsfTrack_PCAy_pv = cms.string('{object}.userFloat("_gsfTrack_PCAy_pv")'),
    object_gsfTrack_PCAz_pv = cms.string('{object}.userFloat("_gsfTrack_PCAz_pv")'),
    object_gsfTrackFitErrorMatrix_00 = cms.string('{object}.userFloat("_gsfTrackFitErrorMatrix_00")'),
    object_gsfTrackFitErrorMatrix_01 = cms.string('{object}.userFloat("_gsfTrackFitErrorMatrix_01")'),
    object_gsfTrackFitErrorMatrix_02 = cms.string('{object}.userFloat("_gsfTrackFitErrorMatrix_02")'),
    object_gsfTrackFitErrorMatrix_11 = cms.string('{object}.userFloat("_gsfTrackFitErrorMatrix_11")'),
    object_gsfTrackFitErrorMatrix_12 = cms.string('{object}.userFloat("_gsfTrackFitErrorMatrix_12")'),
    object_gsfTrackFitErrorMatrix_22 = cms.string('{object}.userFloat("_gsfTrackFitErrorMatrix_22")'),

    object_isoChargedHadrons = cms.string('{object}.pfIsolationVariables().sumChargedHadronPt'),
    object_isoNeutralHadrons = cms.string('{object}.pfIsolationVariables().sumNeutralHadronEt'),
    object_isoPhotons = cms.string('{object}.pfIsolationVariables().sumPhotonEt'),
    object_isoPU = cms.string('{object}.pfIsolationVariables().sumPUPt'),
)

energyCorrections = PSet(
    # left as template
    #objectECorrSmearedNoReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoSmearedNoRegression").t',
    #objectPtCorrSmearedNoReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoSmearedNoRegression").Pt',
    #objectEtaCorrSmearedNoReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoSmearedNoRegression").Eta',
    #objectPhiCorrSmearedNoReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoSmearedNoRegression").Phi',
    #objectdECorrSmearedNoReg_Jan16ReReco = '{object}.userFloat("EGCorr_Jan16ReRecoSmearedNoRegression_error")',
    #
    #objectECorrSmearedReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoSmearedRegression").t',
    #objectPtCorrSmearedReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoSmearedRegression").Pt',
    #objectEtaCorrSmearedReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoSmearedRegression").Eta',
    #objectPhiCorrSmearedReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoSmearedRegression").Phi',
    #objectdECorrSmearedReg_Jan16ReReco = '{object}.userFloat("EGCorr_Jan16ReRecoSmearedRegression_error")',
    #
    #objectECorrReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoRegressionOnly").t',
    #objectPtCorrReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoRegressionOnly").Pt',
    #objectEtaCorrReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoRegressionOnly").Eta',
    #objectPhiCorrReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoRegressionOnly").Phi',
    #objectdECorrReg_Jan16ReReco = '{object}.userFloat("EGCorr_Jan16ReRecoRegressionOnly_error")',
)

tracking = PSet(
    objectHasConversion = '{object}.userFloat("hasConversion")',
    objectMissingHits = 'getElectronMissingHits({object_idx})',
)

# Information about the matched supercluster
supercluster = PSet(
    objectSCEta = '{object}.superCluster().eta',
    objectSCPhi = '{object}.superCluster().phi',
    objectSCEnergy = '{object}.superCluster().energy',
    objectSCRawEnergy = '{object}.superCluster().rawEnergy',
    objectSCPreshowerEnergy = '{object}.superCluster().preshowerEnergy',
    objectSCPhiWidth = '{object}.superCluster().phiWidth',
    objectSCEtaWidth = '{object}.superCluster().etaWidth'   
)

trigger = PSet(
    objectMu23El12 = 'matchToHLTFilter({object_idx}, "hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter", 0.5)',
    objectMu8El23 = 'matchToHLTFilter({object_idx}, "hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter", 0.5)',
    objectEle22 = 'matchToHLTFilter({object_idx}, "hltEle22WP75L1IsoEG20erTau20erGsfTrackIsoFilter", 0.5)',
    objectOverlapEle22 = 'matchToHLTFilter({object_idx}, "hltOverlapFilterIsoEle22WP75GsfLooseIsoPFTau20", 0.5)',
    objectSingleEle = 'matchToHLTFilter({object_idx}, "hltEle32WP75GsfTrackIsoFilter", 0.5)',
    objectEle22Loose = 'matchToHLTFilter({object_idx}, "hltSingleEle22WPLooseGsfTrackIsoFilter", 0.5)',
    objectOverlapEle22Loose = 'matchToHLTFilter({object_idx}, "hltOverlapFilterIsoEle22WPLooseGsfLooseIsoPFTau20", 0.5)',
    objectSingleEleTight = 'matchToHLTFilter({object_idx}, "hltEle32WPTightGsfTrackIsoFilter", 0.5)',
)

veto = PSet(
    objectElectronVeto = 'veto3rdLepton({object_idx}, 0.1, "pt > 10 & abs(eta) < 2.5 & userFloat(\'MVANonTrigWP90\') > 0.5 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'ipDXY\')) < 0.045   & abs(userFloat(\'relIso\')) < 0.3", "electron").size()',
    objectMuonVeto = 'veto3rdLepton({object_idx}, 0.0, "pt > 10 & abs(eta) < 2.4 & isMediumMuon > 0.5 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'ipDXY\')) < 0.045  & abs(userFloat(\'relIso\')) < 0.3", "muon").size()',
)