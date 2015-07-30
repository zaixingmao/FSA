'''

Ntuple branch template sets for event level quantities

Each string is transformed into an expression on a FinalStateEvent object.

Author: Evan K. Friis

'''

import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.cfgtools import PSet

# Vetos on extra stuff in the event
num = PSet(
    #evt=cms.vstring('evt.evtId.event', 'I'),  # use int branch
    evt=cms.vstring('evt.event', 'I'),  # use int branch
    lumi=cms.vstring('evt.evtId.luminosityBlock', 'I'),  # use int branch
    run=cms.vstring('evt.evtId.run', 'I'),  # use int branch
    isdata=cms.vstring('evt.isRealData', 'I'),
)

pileup = PSet(
    rho='evt.rho',
    #nvtx='evt.recoVertices.size',
    nvtx='evt.numberVertices',
    # Number of true PU events
    nTruePU='? evt.puInfo.size > 0 ? evt.puInfo[1].getTrueNumInteractions :-1',
)

pv_info = PSet(
    pvX='? evt.pv.isNonnull() ? evt.pv.x : -999',
    pvY='? evt.pv.isNonnull() ? evt.pv.y : -999',
    pvZ='? evt.pv.isNonnull() ? evt.pv.z : -999',
    pvDX='? evt.pv.isNonnull() ? evt.pv.xError : -999',
    pvDY='? evt.pv.isNonnull() ? evt.pv.yError : -999',
    pvDZ='? evt.pv.isNonnull() ? evt.pv.zError : -999',
    pvChi2='? evt.pv.isNonnull() ? evt.pv.chi2 : -999',
    pvndof='? evt.pv.isNonnull() ? evt.pv.ndof : -999',
    pvNormChi2='? evt.pv.isNonnull() ? evt.pv.normalizedChi2 : -999',
    pvIsValid=cms.vstring('? evt.pv.isNonnull() ? evt.pv.isValid : 0', 'I'),
    pvIsFake=cms.vstring('? evt.pv.isNonnull() ? evt.pv.isFake : 1', 'I'),
    pvRho = 'evt.pv.position.Rho',
)

met = PSet(
    mvametEt       = 'evt.met("mvamet").et',
    mvametPhi      = 'evt.met("mvamet").phi',
    pfMetEt        = 'evt.met4vector("pfmet","",1).Et',
    pfMetPhi       = 'evt.met4vector("pfmet","",1).Phi',
    type1_pfMetEt  = 'evt.met4vector("pfmet","type1",1).Et', #1 --> phi correction not in miniAOD
    type1_pfMetPhi = 'evt.met4vector("pfmet","type1",1).Phi',
    #systematics
    pfMet_mes_Et   = 'evt.met4vector("pfmet","mes+", 1).Et',
    pfMet_tes_Et   = 'evt.met4vector("pfmet","tes+", 1).Et',
    pfMet_jes_Et   = 'evt.met4vector("pfmet","jes+", 1).Et',
    pfMet_ues_Et   = 'evt.met4vector("pfmet","ues+", 1).Et',

    pfMet_mes_Phi  = 'evt.met4vector("pfmet","mes+", 1).Phi',
    pfMet_tes_Phi  = 'evt.met4vector("pfmet","tes+", 1).Phi',
    pfMet_jes_Phi  = 'evt.met4vector("pfmet","jes+", 1).Phi',
    pfMet_ues_Phi  = 'evt.met4vector("pfmet","ues+", 1).Phi',
    
    #mvamet cov matrix
    mvametCovariance_00 = 'evt.met("mvamet").getSignificanceMatrix()[0][0]',
    mvametCovariance_01 = 'evt.met("mvamet").getSignificanceMatrix()[0][1]',
    mvametCovariance_10 = 'evt.met("mvamet").getSignificanceMatrix()[1][0]',
    mvametCovariance_11 = 'evt.met("mvamet").getSignificanceMatrix()[1][1]',

    #pfmet cov matrix
    pfmetCovariance_00 = 'evt.met("pfmet").getSignificanceMatrix()[0][0]',
    pfmetCovariance_01 = 'evt.met("pfmet").getSignificanceMatrix()[0][1]',
    pfmetCovariance_10 = 'evt.met("pfmet").getSignificanceMatrix()[1][0]',
    pfmetCovariance_11 = 'evt.met("pfmet").getSignificanceMatrix()[1][1]',

    tautauMVAMETEt        = 'evt.met4vector("tautauMVAMET","",1).Et',
    tautauMVAMETPhi       = 'evt.met4vector("tautauMVAMET","",1).Phi',
    tautauMVAMETCovariance_00 = 'evt.met("tautauMVAMET").getSignificanceMatrix()[0][0]',
    tautauMVAMETCovariance_01 = 'evt.met("tautauMVAMET").getSignificanceMatrix()[0][1]',
    tautauMVAMETCovariance_10 = 'evt.met("tautauMVAMET").getSignificanceMatrix()[1][0]',
    tautauMVAMETCovariance_11 = 'evt.met("tautauMVAMET").getSignificanceMatrix()[1][1]',


    genMetEt = 'evt.getGenMET().et',
    genMetPhi = 'evt.getGenMET().phi',

    recoilDaught='getDaughtersRecoil().R()',
    recoilWithMet='getDaughtersRecoilWithMet().R()',
)

gen = PSet(
    # Process ID used to simulate in Pythia
    processID='evt.genEventInfo.signalProcessID',
    isZtautau='evt.findDecay(23,15)',
    isGtautau='evt.findDecay(22,15)',
    isWtaunu='evt.findDecay(24,15)',
    isWmunu='evt.findDecay(24,13)',
    NUP='evt.lesHouches.NUP',
    EmbPtWeight='evt.generatorFilter.filterEfficiency',
    genEventWeight='evt.weight("genEventWeight")',
    genNuPt       = '? getGenNu().pt() > 0 ? getGenNu().pt() : -999',
    genNuEta       = '? getGenNu().pt() > 0 ? getGenNu().eta()  : -999',
    genNuPhi       = '? getGenNu().pt() > 0 ? getGenNu().phi()  : -999',
    genNuMass       = '? getGenNu().pt() > 0 ? getGenNu().mass()  : -999',

)

tauSpinner = PSet(
    tauSpinnerWeight = 'evt.weight("tauSpinnerWeight")'
)


