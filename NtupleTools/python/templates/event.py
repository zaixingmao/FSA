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

mvamet = PSet(
    mvametEt       = 'evt.met("mvamet").et',
    mvametPhi      = 'evt.met("mvamet").phi',

    #mvamet cov matrix
    mvametCovariance_00 = 'evt.met("mvamet").getSignificanceMatrix()[0][0]',
    mvametCovariance_01 = 'evt.met("mvamet").getSignificanceMatrix()[0][1]',
    mvametCovariance_10 = 'evt.met("mvamet").getSignificanceMatrix()[1][0]',
    mvametCovariance_11 = 'evt.met("mvamet").getSignificanceMatrix()[1][1]',
)

tautauMVAMET = PSet(
    tautauMVAMETEt        = 'tautauMVAMET.et',
    tautauMVAMETPhi       = 'tautauMVAMET.phi',
    tautauMVAMETCovariance_00 = 'tautauMVAMET.getSignificanceMatrix()[0][0]',
    tautauMVAMETCovariance_01 = 'tautauMVAMET.getSignificanceMatrix()[0][1]',
    tautauMVAMETCovariance_10 = 'tautauMVAMET.getSignificanceMatrix()[1][0]',
    tautauMVAMETCovariance_11 = 'tautauMVAMET.getSignificanceMatrix()[1][1]',
)


met = PSet(

    pfMetEt        = 'evt.met4vector("pfmet","",1).Et',
    pfMetPhi       = 'evt.met4vector("pfmet","",1).Phi',
#     pfMetNoHFEt        = 'evt.met4vector("pfmetNoHF","",1).Et',
#     pfMetNoHFPhi       = 'evt.met4vector("pfmetNoHF","",1).Phi',
    metPuppiEt        = 'evt.met4vector("pfmetPuppi","",1).Et',
    metPuppiPhi       = 'evt.met4vector("pfmetPuppi","",1).Phi',

    #systematics
    pfMet_eesUp_Et   = 'evt.met4vector("pfmet_eesUp","", 1).Et',
    pfMet_mesUp_Et   = 'evt.met4vector("pfmet_mesUp","", 1).Et',
    pfMet_tesUp_Et   = 'evt.met4vector("pfmet_tesUp","", 1).Et',
    pfMet_jesUp_Et   = 'evt.met4vector("pfmet_jesUp","", 1).Et',
    pfMet_jresUp_Et   = 'evt.met4vector("pfmet_jresUp","", 1).Et',
    pfMet_uesUp_Et   = 'evt.met4vector("pfmet_uesUp","", 1).Et',

    pfMet_eesDown_Et   = 'evt.met4vector("pfmet_eesDown","", 1).Et',
    pfMet_mesDown_Et   = 'evt.met4vector("pfmet_mesDown","", 1).Et',
    pfMet_tesDown_Et   = 'evt.met4vector("pfmet_tesDown","", 1).Et',
    pfMet_jesDown_Et   = 'evt.met4vector("pfmet_jesDown","", 1).Et',
    pfMet_jresDown_Et   = 'evt.met4vector("pfmet_jresDown","", 1).Et',
    pfMet_uesDown_Et   = 'evt.met4vector("pfmet_uesDown","", 1).Et',

    pfMet_eesUp_Phi   = 'evt.met4vector("pfmet_eesUp","", 1).Phi',
    pfMet_mesUp_Phi   = 'evt.met4vector("pfmet_mesUp","", 1).Phi',
    pfMet_tesUp_Phi   = 'evt.met4vector("pfmet_tesUp","", 1).Phi',
    pfMet_jesUp_Phi   = 'evt.met4vector("pfmet_jesUp","", 1).Phi',
    pfMet_jresUp_Phi   = 'evt.met4vector("pfmet_jresUp","", 1).Phi',
    pfMet_uesUp_Phi   = 'evt.met4vector("pfmet_uesUp","", 1).Phi',

    pfMet_eesDown_Phi   = 'evt.met4vector("pfmet_eesDown","", 1).Phi',
    pfMet_mesDown_Phi   = 'evt.met4vector("pfmet_mesDown","", 1).Phi',
    pfMet_tesDown_Phi   = 'evt.met4vector("pfmet_tesDown","", 1).Phi',
    pfMet_jesDown_Phi   = 'evt.met4vector("pfmet_jesDown","", 1).Phi',
    pfMet_jresDown_Phi   = 'evt.met4vector("pfmet_jresDown","", 1).Phi',
    pfMet_uesDown_Phi   = 'evt.met4vector("pfmet_uesDown","", 1).Phi',   

    #pfmet cov matrix
    pfmetCovariance_00 = 'evt.met("pfmet").getSignificanceMatrix()[0][0]',
    pfmetCovariance_01 = 'evt.met("pfmet").getSignificanceMatrix()[0][1]',
    pfmetCovariance_10 = 'evt.met("pfmet").getSignificanceMatrix()[1][0]',
    pfmetCovariance_11 = 'evt.met("pfmet").getSignificanceMatrix()[1][1]',

#     pfmetNoHF cov matrix
#     pfmetNoHFCovariance_00 = 'evt.met("pfmetNoHF").getSignificanceMatrix()[0][0]',
#     pfmetNoHFCovariance_01 = 'evt.met("pfmetNoHF").getSignificanceMatrix()[0][1]',
#     pfmetNoHFCovariance_10 = 'evt.met("pfmetNoHF").getSignificanceMatrix()[1][0]',
#     pfmetNoHFCovariance_11 = 'evt.met("pfmetNoHF").getSignificanceMatrix()[1][1]',
# 
#     pfmetNoHF cov matrix
#     metPuppiCovariance_00 = 'evt.met("pfmetPuppi").getSignificanceMatrix()[0][0]',
#     metPuppiCovariance_01 = 'evt.met("pfmetPuppi").getSignificanceMatrix()[0][1]',
#     metPuppiCovariance_10 = 'evt.met("pfmetPuppi").getSignificanceMatrix()[1][0]',
#     metPuppiCovariance_11 = 'evt.met("pfmetPuppi").getSignificanceMatrix()[1][1]',


    recoilDaught='getDaughtersRecoil().R()',
    recoilWithMet='getDaughtersRecoilWithMet().R()',
)

gen = PSet(
    # Process ID used to simulate in Pythia
    processID='evt.genEventInfo.signalProcessID',
    isZtautau='evt.findDecay(23,15)',
    isZee='evt.findDecay(23,11)',
    isZmumu='evt.findDecay(23,13)',
    isGtautau='evt.findDecay(22,15)',
    isWtaunu='evt.findDecay(24,15)',
    isWmunu='evt.findDecay(24,13)',
    isWenu='evt.findDecay(24,11)',
    X_to_ee='evt.findGenMotherMass(11, 23)',
    X_to_mumu='evt.findGenMotherMass(13, 23)',
    X_to_tautau='evt.findGenMotherMass(15, 23)',
    X_to_ll='evt.findGenMotherMass(11, 23)+evt.findGenMotherMass(13, 23)+evt.findGenMotherMass(15, 23)',
    
    binningValue = '? evt.genEventInfo.binningValues().size()>0 ? evt.genEventInfo.binningValues()[0]: -9999',
    binningValue2 = '? evt.genEventInfo.binningValues().size()>1 ? evt.genEventInfo.binningValues()[1]: -9999',

    nPromptTaus='evt.findPromptDecay(15, 2)',
    nPromptElec='evt.findPromptDecay(11, 1)',
    nPromptMuon='evt.findPromptDecay(13, 1)',
    nTauNuFromPromptTaus='evt.nDirectPromptTauDecayProductFinalState(16)',


    NUP='evt.lesHouches.NUP',
    genHT = 'evt.genHT',
    genHT_BSM3G = 'evt.genHT_BSM3G',
    EmbPtWeight='evt.generatorFilter.filterEfficiency',
    genEventWeight='evt.weight("genEventWeight")',
    topPtWeight='evt.weight("ptWeight")',
    genNuPt       = '? getGenNu().pt() > 0 ? getGenNu().pt() : -999',
    genNuEta       = '? getGenNu().pt() > 0 ? getGenNu().eta()  : -999',
    genNuPhi       = '? getGenNu().pt() > 0 ? getGenNu().phi()  : -999',
    genNuMass       = '? getGenNu().pt() > 0 ? getGenNu().mass()  : -999',
    genMetEt = 'evt.getGenMET().et',
    genMetPhi = 'evt.getGenMET().phi',
    pdfWeights = 'evt.getPDFWeight()',
    pdfIDs = 'evt.getPDFID()',
)

tauSpinner = PSet(
    tauSpinnerWeight = 'evt.weight("tauSpinnerWeight")'
)


