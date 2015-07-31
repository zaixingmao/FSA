'''

Ntuple branch template sets for muon objects.

Each string is transformed into an expression on a FinalStateEvent object.

{object} should be replaced by an expression which evaluates to a pat::Muon
i.e. daughter(1) or somesuch.

Author: Evan K. Friis

'''

import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.cfgtools import PSet

# ID and isolation
id = PSet(
    objectPFIDTight = 'isTightMuon({object_idx})',
    objectPFIDLoose = '{object}.isLooseMuon()',
    objectRelIso = '{object}.userFloat("relIso")',

    # For charged, we use ALL charged particles
    objectEffectiveArea2012 = '{object}.userFloat("ea_comb_iso04_kt6PFJCNth05")',
    objectEffectiveArea2011 = '{object}.userFloat("ea_comb_iso04_kt6PFJCth05")',
    objectRho = cms.string('{object}.userFloat("rhoCSA14")'),
    objectPFChargedIso = cms.string('{object}.userIsolation("PfChargedHadronIso")'),
    objectPFNeutralIso = cms.string('{object}.userIsolation("PfNeutralHadronIso")'),
    objectPFPhotonIso  = cms.string('{object}.userIsolation("PfGammaIso")'),
    objectPFPUChargedIso = cms.string('{object}.userIsolation("PfPUChargedHadronIso")'),
    objectRelPFIsoDBDefault = cms.string(
        "({object}.chargedHadronIso()"
        "+max({object}.photonIso()"
        "+{object}.neutralHadronIso()"
        "-0.5*{object}.puChargedHadronIso,0.0))"
        "/{object}.pt()"
    ),
    objectRelPFIsoRho = cms.string(
        '({object}.chargedHadronIso()'
        '+max(0.0,{object}.neutralHadronIso()'
        '+{object}.photonIso()'
        '-{object}.userFloat("rhoCSA14")*{object}.userFloat("ea_comb_iso04_kt6PFJCNth05")))'
        '/{object}.pt()'
    ),
    objectRelPFIsoRhoFSR = cms.string(
        '({object}.chargedHadronIso()'
        '+max(0.0,{object}.neutralHadronIso()'
        '+{object}.photonIso() - userFloat("leg{object_idx}fsrIsoCorr")'
        '-{object}.userFloat("rhoCSA14")*{object}.userFloat("ea_comb_iso04_kt6PFJCNth05")))'
        '/{object}.pt()'
    ),
    objectIsMediumMuon = '{object}.isMediumMuon',
    objectIsPFMuon = '{object}.isPFMuon',
    objectIsGlobal = '{object}.isGlobalMuon',
    objectIsTracker = '{object}.isTrackerMuon',
    objectTypeCode = cms.vstring('{object}.type','I'),
    objectBestTrackType = '{object}.muonBestTrackType',
    objectGenMotherPdgId = '? (getDaughterGenParticleMotherSmart({object_idx}, 13, 1).isAvailable && getDaughterGenParticleMotherSmart({object_idx}, 13, 1).isNonnull) ? getDaughterGenParticleMotherSmart({object_idx}, 13, 1).pdgId() : -999',
    objectComesFromHiggs = 'comesFromHiggs({object_idx}, 13, 1)',

    objectGenPdgId       = '? (getDaughterGenParticle({object_idx}, 13, 1, 0.5, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 13, 1, 0.5, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 1, 0.5, 0.5).pdgId() : -999',
    objectGenMass      = '? (getDaughterGenParticle({object_idx}, 13, 1, 0.5, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 13, 1, 0.5, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 1, 0.5, 0.5).mass() : -999',
    objectGenEta         = '? (getDaughterGenParticle({object_idx}, 13, 1, 0.5, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 13, 1, 0.5, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 1, 0.5, 0.5).eta()   : -999',
    objectGenPhi         = '? (getDaughterGenParticle({object_idx}, 13, 1, 0.5, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 13, 1, 0.5, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 1, 0.5, 0.5).phi()   : -999',
    objectGenPt          = '? (getDaughterGenParticle({object_idx}, 13, 1, 0.5, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 13, 1, 0.5, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 1, 0.5, 0.5).pt()   : -999',
    objectGenVZ          = '? (getDaughterGenParticle({object_idx}, 13, 1, 0.5, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 13, 1, 0.5, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 1, 0.5, 0.5).vz()   : -999',
    objectGenVtxPVMatch  = 'genVtxPVMatch({object_idx})', # is PV closest vtx to gen vtx?

    objectGenTauMass      = '? (getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).mass() : -999',
    objectGenTauEta         = '? (getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).eta()   : -999',
    objectGenTauPhi         = '? (getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).phi()   : -999',
    objectGenTauPt          = '? (getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).isAvailable && getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 1, 1.0, 0.5).pt()   : -999',

)

energyCorrections = PSet(
    # left as template
    #objectERochCor2012 = 'getUserLorentzVector({object_idx},"p4_RochCor2012").t',
    #objectPtRochCor2012 = 'getUserLorentzVector({object_idx},"p4_RochCor2012").Pt',
    #objectEtaRochCor2012 = 'getUserLorentzVector({object_idx},"p4_RochCor2012").Eta',
    #objectPhiRochCor2012 = 'getUserLorentzVector({object_idx},"p4_RochCor2012").Phi',
    #objectEErrRochCor2012 = '{object}.userFloat("p4_RochCor2012_tkFitErr")'
)

# Information about the associated track
tracking = PSet(
    objectPixHits = '? {object}.innerTrack.isNonnull ? '
        '{object}.innerTrack.hitPattern.numberOfValidPixelHits :-1',
    objectNormTrkChi2 = "? {object}.combinedMuon.isNonnull ? "
        "{object}.combinedMuon.normalizedChi2 : 1e99",
    objectTkLayersWithMeasurement = '? {object}.innerTrack.isNonnull ? '
        '{object}.innerTrack().hitPattern().trackerLayersWithMeasurement : -1',
    objectMuonHits = '? {object}.globalTrack.isNonnull ? '
        '{object}.globalTrack().hitPattern().numberOfValidMuonHits() : -1',
    objectMatchedStations = '{object}.numberOfMatchedStations',
    #objectD0 = '{object}.dB("PV3D")',
)

# Trigger matching
trigger = PSet(
    objectMu23El12 = 'matchToHLTFilter({object_idx}, "hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered23", 0.5)',
    objectMu8El23 = 'matchToHLTFilter({object_idx}, "hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered8", 0.5)',
    objectIsoMu24 = 'matchToHLTFilter({object_idx}, "hltL3crIsoL1sMu20Eta2p1L1f0L2f10QL3f24QL3trkIsoFiltered0p09", 0.5)',
    objectIsoMu27 = 'matchToHLTFilter({object_idx}, "hltL3crIsoL1sMu25L1f0L2f10QL3f27QL3trkIsoFiltered0p09", 0.5)',
    objectMuTau = 'matchToHLTFilter({object_idx}, "hltL3crIsoL1sMu16erTauJet20erL1f0L2f10QL3f17QL3trkIsoFiltered0p09", 0.5)',
    objectMuTauOverlap = 'matchToHLTFilter({object_idx}, "hltOverlapFilterIsoMu17LooseIsoPFTau20", 0.5)',
 )


