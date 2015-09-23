#include "FinalStateAnalysis/DataAlgos/interface/helpers.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "PhysicsTools/HepMCCandAlgos/interface/GenParticlesHelper.h"

#include "CommonTools/UtilAlgos/interface/MCMatchSelector.h"
#include "CommonTools/UtilAlgos/interface/MatchByDRDPt.h"
#include "CommonTools/UtilAlgos/interface/MatchLessByDPt.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "TMatrixD.h"
#include "TMath.h"
#include "RecoTauTag/TauTagTools/interface/GeneratorTau.h"
#include <vector>
//#include <iostream>

namespace fshelpers {

double xySignficance(const reco::Candidate::Vector& vector,
    const TMatrixD& covariance) {
  // Instead of playing around w/ vector types to get ROOT
  // to do this for us, just do it manually.
  double vx = vector.x();
  double vy = vector.y();
  double mag2 = vx*vx + vy*vy;
  double mag = TMath::Sqrt(mag2);

  if (mag < 1.0e-9)
    return -1;

  // vT dot cov dot v
  double c00 = covariance(0,0);
  double c01 = covariance(0,1);
  double c10 = covariance(1,0);
  double c11 = covariance(1,1);

  double covDotVx = (c00*vx + c01*vy);
  double covDotVy = (c10*vx + c11*vy);

  double vTdotCovDotV = vx*covDotVx + vy*covDotVy;

  if (vTdotCovDotV < 0)
    return -2;

  // compute error pointing along the vector
  double error = TMath::Sqrt(vTdotCovDotV)/mag;

  return mag/error;
}

// By C. Veelken
std::pair<double, double> pZeta( const reco::Candidate::LorentzVector& leg1,
    const reco::Candidate::LorentzVector& leg2, double metPx, double metPy) {
  //std::cout << "<CompositePtrCandidateT1T2MEtAlgorithm::compZeta>:" << std::endl;

  double leg1x = cos(leg1.phi());
  double leg1y = sin(leg1.phi());
  double leg2x = cos(leg2.phi());
  double leg2y = sin(leg2.phi());
  double zetaX = leg1x + leg2x;
  double zetaY = leg1y + leg2y;
  double zetaR = TMath::Sqrt(zetaX*zetaX + zetaY*zetaY);
  if ( zetaR > 0. ) {
    zetaX /= zetaR;
    zetaY /= zetaR;
  }

  //std::cout << " leg1Phi = " << leg1.phi()*180./TMath::Pi() << std::endl;
  //std::cout << " leg2Phi = " << leg2.phi()*180./TMath::Pi() << std::endl;

  //std::cout << " zetaX = " << zetaX << std::endl;
  //std::cout << " zetaY = " << zetaY << std::endl;

  //std::cout << " zetaPhi = " << normalizedPhi(atan2(zetaY, zetaX))*180./TMath::Pi() << std::endl;

  double visPx = leg1.px() + leg2.px();
  double visPy = leg1.py() + leg2.py();
  double pZetaVis = visPx*zetaX + visPy*zetaY;

  //std::cout << " visPx = " << visPx << std::endl;
  //std::cout << " visPy = " << visPy << std::endl;

  double px = visPx + metPx;
  double py = visPy + metPy;
  double pZeta = px*zetaX + py*zetaY;

  //std::cout << " metPhi = " << normalizedPhi(atan2(metPy, metPx))*180./TMath::Pi() << std::endl;

  //assert(pZetaVis >= 0.);

  return std::make_pair(pZeta, pZetaVis);
}

double transverseMass(const reco::Candidate::LorentzVector& p1,
    const reco::Candidate::LorentzVector& p2){
  double totalEt = p1.Et() + p2.Et();
  double totalPt = (p1 + p2).pt();
  double mt2 = totalEt*totalEt - totalPt*totalPt;
  if (mt2 < 0) {
    std::cout << "P1 = " << p1 << " P2 = " << p2 << " " << mt2 << std::endl;
  }
  return std::sqrt(std::abs(mt2));
}

// Taken from CommonTools/CandUtils/AddFourMomenta.h
void addFourMomenta( reco::Candidate & c ) {
  reco::Candidate::LorentzVector p4( 0, 0, 0, 0 );
  reco::Candidate::Charge charge = 0;
  size_t n = c.numberOfDaughters();
  for(size_t i = 0; i < n; ++i) {
    const reco::Candidate * d = (const_cast<const reco::Candidate &>(c)).daughter(i);
    p4 += d->p4();
    charge += d->charge();
  }
  c.setP4( p4 );
  c.setCharge( charge );
}

/// Helper function to get the matched gen particle 
const reco::GenParticleRef getGenParticle(const reco::Candidate* daughter, const reco::GenParticleRefProd genCollectionRef, int pdgIdToMatch, bool checkCharge, double maxDPtRel, double maxDeltaR, double minPt, int statusFlag)
{
  //if no genPaticle no matching
  if(!genCollectionRef){
    return reco::GenParticleRef();
  }
  reco::GenParticleCollection genParticles = *genCollectionRef;

  //builds pset used by various subclasses
  edm::ParameterSet pset;
  pset.addParameter<double>("maxDPtRel", maxDPtRel);
  pset.addParameter<double>("maxDeltaR", maxDeltaR);
  std::vector<int> pdgIdsToMatch;
  pdgIdsToMatch.push_back(pdgIdToMatch);
  pset.addParameter<std::vector<int> >("mcPdgId", pdgIdsToMatch);
  std::vector<int> status;
  pset.addParameter<std::vector<int> >("mcStatus", status);
  pset.addParameter<bool>("resolveByMatchQuality", false);
  pset.addParameter<bool>("checkCharge", checkCharge);
  pset.addParameter<bool>("resolveAmbiguities", true); //does not make any difference since we have no access to multiple candidates to match

  reco::MCMatchSelector<reco::Candidate, reco::GenParticle> slector(pset);
  reco::MatchByDRDPt<reco::Candidate, reco::GenParticle> matcher(pset);

  //copied from CommonTools/ UtilAlgos/ interface/ PhysObjectMatcher.h
  typedef std::pair<size_t, size_t> IndexPair;
  typedef std::vector<IndexPair> MatchContainer;

  // loop over (one in my case) candidates
  int index = -1;
  double minDr = 9999;

//   std::cout<<"tau pt: "<<daughter->pt()<<"  eta: "<<daughter->eta()<<"  phi: "<<daughter->phi()<<std::endl;

  // loop over target collection
  for(size_t m = 0; m != genParticles.size(); ++m) {
    const reco::GenParticle& match = genParticles[m];

    //check if it's final gen particle before decay
    bool final = true;
    if(abs(match.pdgId()) == pdgIdToMatch){
        if(statusFlag == 0){
            size_t nDaughters = match.numberOfDaughters();
            for(size_t iDaughter = 0; iDaughter < nDaughters; iDaughter++){
                if(abs(match.daughter(iDaughter)->pdgId()) == pdgIdToMatch) final = false;
            }
//         if(final) std::cout<<"gen pt: "<<match.pt()<<"  eta: "<<match.eta()<<"  phi: "<<match.phi()<<std::endl;
        }
    }
    else final = false;
    if(!final) continue;

    double curDr = ROOT::Math::VectorUtil::DeltaR(daughter->p4(), match.p4());

    //check status flag
    if(statusFlag == 1 && !match.statusFlags().isPrompt()) continue;
    if(statusFlag == 2 && !match.isPromptFinalState()) continue;
    if(statusFlag == 3 && !match.statusFlags().isDirectPromptTauDecayProduct()) continue;
    if(statusFlag == 4 && !match.isDirectPromptTauDecayProductFinalState()) continue;
    if(statusFlag == 5){
        size_t nDaughters = match.numberOfDaughters();
        bool pass = false;
        for(size_t iDaughter = 0; iDaughter < nDaughters; iDaughter++){
            if(abs(match.daughter(iDaughter)->pdgId()) == pdgIdToMatch) pass = true;
            if(abs(match.daughter(iDaughter)->pdgId()) == 13 or abs(match.daughter(iDaughter)->pdgId()) == 11) pass = true;
        } 
       if(pass) continue;
        GeneratorTau tau(match);
        tau.init();
        if((tau.getVisibleFourVector()).pt() <= minPt) continue;
        else curDr = ROOT::Math::VectorUtil::DeltaR(daughter->p4(), tau.getVisibleFourVector());
    }
    else{//check pt threshold
        if(match.pt() <= minPt) continue;
    }
//     if(checkCharge && (daughter->charge() != match.charge())) continue;
    if(curDr < maxDeltaR){
	    if(curDr < minDr){
	        minDr = curDr;
	        index = m;
	    }
    }


    // check lock and preselection
//     if ( slector(*daughter, match) ) {
//       // matching requirement fulfilled -> store pair of indices
//       if ( matcher(*daughter,match) )  {
// 	    double curDr = reco::deltaR(*daughter,match);
// 	    if(curDr < minDr){
// 	        minDr = curDr;
// 	        index = m;
// 	    }
//       }
//     }
  }

  // if match(es) found and no global ambiguity resolution requested
  if(index != -1){
//     std::cout<<"found match"<<std::endl;
//     std::cout<<"matched tau pt: "<<reco::GenParticleRef(genCollectionRef,index)->pt()<<"  eta: "<<reco::GenParticleRef(genCollectionRef,index)->eta()<<"  phi: "<<reco::GenParticleRef(genCollectionRef,index)->phi()<<std::endl;
//     std::cout<<std::endl;
    return reco::GenParticleRef(genCollectionRef,index);
  }
  //No Match found
  else{
//     std::cout<<"didn't find match"<<std::endl;
//     std::cout<<std::endl;
    return reco::GenParticleRef();
  }


}

/// Helper function to get the matched gen particle 
const int getGenMatchCategory(const reco::Candidate* daughter, const reco::GenParticleRefProd genCollectionRef)
{

    reco::GenParticleRef promptElectron  = getGenParticle(daughter, genCollectionRef, 11, 1, 0, 0.5, 8, 1);
    reco::GenParticleRef promptMuon      = getGenParticle(daughter, genCollectionRef, 13, 1, 0, 0.5, 8, 2);
    reco::GenParticleRef tau2Electron    = getGenParticle(daughter, genCollectionRef, 11, 1, 0, 0.5, 8, 3);
    reco::GenParticleRef tau2Muon        = getGenParticle(daughter, genCollectionRef, 13, 1, 0, 0.5, 8, 4);
    reco::GenParticleRef tauh            = getGenParticle(daughter, genCollectionRef, 15, 1, 0, 0.5, 15, 5);

  double minDR = 0.5;
  int category = 6;
  double curDR = 0.0;
  if(promptElectron.isAvailable() && promptElectron.isNonnull()){
    minDR = ROOT::Math::VectorUtil::DeltaR(daughter->p4(), promptElectron->p4());
    category = 1;
  }
  if(promptMuon.isAvailable() && promptMuon.isNonnull()){
    curDR = ROOT::Math::VectorUtil::DeltaR(daughter->p4(), promptMuon->p4());
    if(curDR < minDR){
        minDR = curDR;
        category = 2;
    }
  }
  if(tau2Electron.isAvailable() && tau2Electron.isNonnull()){
    curDR = ROOT::Math::VectorUtil::DeltaR(daughter->p4(), tau2Electron->p4());
    if(curDR < minDR){
        minDR = curDR;
        category = 3;
    }
  }
  if(tau2Muon.isAvailable() && tau2Muon.isNonnull()){
    curDR = ROOT::Math::VectorUtil::DeltaR(daughter->p4(), tau2Muon->p4());
    if(curDR < minDR){
        minDR = curDR;
        category = 4;
    }
  }
  if(tauh.isAvailable() && tauh.isNonnull()){
    GeneratorTau tau(*tauh);
    tau.init();
    curDR = ROOT::Math::VectorUtil::DeltaR(daughter->p4(), tau.getVisibleFourVector());

    if(curDR < minDR){
        minDR = curDR;
        category = 5;
    }
  }
  return category;
}

/// Helper function to get the matched gen particle 
const reco::Candidate::LorentzVector getGenParticleVisMomentum(const reco::Candidate* daughter, const reco::GenParticleRefProd genCollectionRef, int pdgIdToMatch, bool checkCharge, double maxDPtRel, double maxDeltaR)
{
  reco::Candidate::LorentzVector p4Vis(0,0,0,0);
  reco::GenParticleRef mother = getGenParticle(daughter, genCollectionRef, pdgIdToMatch, checkCharge, maxDPtRel, maxDeltaR);

  if(mother.isAvailable() && mother.isNonnull()){
    while(abs((mother->daughterRef(0).get())->pdgId()) == 15) mother = mother->daughterRef(0);
    GeneratorTau tau(*mother);
    tau.init();
    p4Vis += tau.getVisibleFourVector();
  }
  return p4Vis;
}

const reco::Candidate::LorentzVector getGenParticleNuMomentum(const reco::Candidate*   daughter, const reco::GenParticleRefProd genCollectionRef, int pdgIdToMatch, bool checkCharge, double maxDPtRel, double maxDeltaR)
{
  reco::Candidate::LorentzVector p4Vis(0,0,0,0);
  reco::GenParticleRef mother = getGenParticle(daughter, genCollectionRef, pdgIdToMatch, checkCharge, maxDPtRel, maxDeltaR);

  if(mother.isAvailable() && mother.isNonnull()){
    while(abs((mother->daughterRef(0).get())->pdgId()) == 15) mother = mother->daughterRef(0);
    GeneratorTau tau(*mother);
    tau.init();
    std::vector< const reco::Candidate * > nus = tau.getGenNu();
    for(unsigned int iNu =0; iNu < nus.size(); iNu++) p4Vis += nus[iNu]->p4();
  }
  return p4Vis;
}

const reco::Candidate::LorentzVector getGenNu(const reco::GenParticleRefProd genCollectionRef)
{
  reco::Candidate::LorentzVector p4Vis(0,0,0,0);
  //if no genPaticle no matching
  if(!genCollectionRef){
    return p4Vis;
  }
  reco::GenParticleCollection genParticles = *genCollectionRef;
  for(size_t m = 0; m != genParticles.size(); ++m) {
    const reco::GenParticle& match = genParticles[m];

    if (match.numberOfDaughters() == 0){
        if( abs(match.pdgId())==12 || abs(match.pdgId())==14 || abs(match.pdgId())==16 ) p4Vis += match.p4();
    }
  }
  return p4Vis;
}



/// Helper function to get the first interesting mother particle 
const reco::GenParticleRef getMotherSmart(const reco::GenParticleRef genPart, int idNOTtoMatch)
{
  if( genPart->numberOfMothers() == 0 ) return genPart; // if we've recursed all the way back we need to stop

  const reco::GenParticleRef mother = genPart->motherRef();
  if( !(mother.isAvailable() && mother.isNonnull())  ) return mother;
  if( mother.isAvailable() && mother.isNonnull() && mother->status() == 3 && mother->pdgId() != idNOTtoMatch )
    return mother;
  else
    return getMotherSmart(mother, idNOTtoMatch);
}

const bool comesFromHiggs(const reco::GenParticleRef genPart)
{
  //std::cout << "comesFromHiggs::start" << std::endl;
  if( genPart->numberOfMothers() >= 1 ){
    const reco::GenParticleRef mother = /*dynamic_cast<reco::GenParticleRef>*/ (genPart->motherRef());
    //std::cout << "comesFromHiggs::if statements" << std::endl;
    if( !(mother.isAvailable() && mother.isNonnull()) ){
      //std::cout << "comesFromHiggs::ret false" << std::endl;
      return false;
    }
    if( mother.isAvailable() && mother.isNonnull() && (mother->pdgId() == 25 || mother->pdgId() == 35 ) ){ // h^0 or H^0
      //std::cout << "comesFromHiggs::ret true" << std::endl;
      return true;
    }
    else{
      //std::cout << "comesFromHiggs::ret recursive" << std::endl;
      return comesFromHiggs(mother);
    }
  }
  else{
    //std::cout << "comesFromHiggs::ret false from no mother" << std::endl;
    return false;
  }
}

const reco::Candidate::LorentzVector metPhiCorrection(const reco::Candidate::LorentzVector& vector, int nvertices, bool isMC)
{
  //ReReco data / Summer'12 MC + Summer'13 JEC Type1 PFMET
  const double cx0 = (isMC) ? +1.62861e-01 : +4.83642e-02;  // 0.1166 :  0.2661;
  const double cxS = (isMC) ? -2.38517e-02 : +2.48870e-01;  // 0.0200 :  0.3217;
  const double cy0 = (isMC) ? +3.60860e-01 : -1.50135e-01;  // 0.2764 : -0.2251;
  const double cyS = (isMC) ? -1.30335e-01 : -8.27917e-02;  //-0.1280 : -0.1747;

  double offset_x = cx0 + cxS*nvertices;
  double offset_y = cy0 + cyS*nvertices;

  double newx     = vector.x() - offset_x;
  double newy     = vector.y() - offset_y;
  double mag      = TMath::Sqrt(newx*newx + newy*newy);

  //the vector is made in pt eta phi e coordinates!
  return reco::Candidate::LorentzVector(newx, newy, 0., mag);
}

const bool findDecay(const reco::GenParticleRefProd genCollectionRef, int pdgIdMother, int pdgIdDaughter)
{
  //if no genPaticle no matching
  if(!genCollectionRef){
    return false;
  }
  reco::GenParticleCollection genParticles = *genCollectionRef;
  reco::GenParticleRefVector allMothers;  
  GenParticlesHelper::findParticles( *genCollectionRef, allMothers, std::abs(pdgIdMother), 0);
  int nDecays = 0;
  for ( GenParticlesHelper::IGR iMom = allMothers.begin(); iMom != allMothers.end(); ++iMom ) {
    bool found = false;
    int n = (*iMom)->numberOfDaughters();
    for(int i = 0; i < n; i++){
        if(abs((*iMom)->daughter(i)->pdgId()) == abs(pdgIdDaughter)){
            found = true;
            break;
        }
    }
    if(found) nDecays += 1;
  }
  return nDecays;
}

int findPromptDecay(const reco::GenParticleRefProd genCollectionRef, int pdgId, int status)
{
  int nPromptParticles = 0;
  //if no genPaticle no matching
  if(!genCollectionRef){
    return nPromptParticles;
  }
  reco::GenParticleCollection genParticles = *genCollectionRef;
  for(size_t m = 0; m != genParticles.size(); ++m) {
    const reco::GenParticle& match = genParticles[m];
    if (abs(match.pdgId()) == pdgId && match.statusFlags().isPrompt() && match.status() == status) nPromptParticles += 1;
  }
  return nPromptParticles;
}

int nDirectPromptTauDecayProductFinalState(const reco::GenParticleRefProd genCollectionRef, int pdgId)
{
  int nPromptParticles = 0;
  //if no genPaticle no matching
  if(!genCollectionRef){
    return nPromptParticles;
  }
  reco::GenParticleCollection genParticles = *genCollectionRef;
  for(size_t m = 0; m != genParticles.size(); ++m) {
    const reco::GenParticle& match = genParticles[m];
    if (abs(match.pdgId()) == pdgId && match.isDirectPromptTauDecayProductFinalState()) nPromptParticles += 1;
  }
  return nPromptParticles;
}

float jetQGVariables(const reco::CandidatePtr  jetptr, const std::string& myvar, const std::vector<edm::Ptr<reco::Vertex>>& recoVertices)
{
  //std::map <std::string, float> varMap; 
  const pat::Jet *jet = dynamic_cast<const pat::Jet*> (jetptr.get());
  if (myvar == "eta")
    return jet->eta();
  Bool_t useQC = true;
  // if(fabs(jet->eta()) > 2.5 && type == "MLP") useQC = false;		//In MLP: no QC in forward region

  std::vector<edm::Ptr<reco::Vertex>>::const_iterator vtxLead = recoVertices.begin();

  Float_t sum_weight = 0., sum_deta = 0., sum_dphi = 0., sum_deta2 = 0., sum_dphi2 = 0., sum_detadphi = 0., sum_pt = 0.;
  Int_t nChg_QC = 0, nChg_ptCut = 0, nNeutral_ptCut = 0;

  //Loop over the jet constituents
  std::vector<reco::PFCandidatePtr> constituents = jet->getPFConstituents();
  for(unsigned i = 0; i < constituents.size(); ++i){
    reco::PFCandidatePtr part = jet->getPFConstituent(i);      
    if(!part.isNonnull()) continue;
    
    reco::TrackRef itrk = part->trackRef();
    
    bool trkForAxis = false;
    if(itrk.isNonnull()){						//Track exists --> charged particle
      if(part->pt() > 1.0) nChg_ptCut++;
  	
      //Search for closest vertex to track
      std::vector<edm::Ptr<reco::Vertex>>::const_iterator  vtxClose = recoVertices.begin();
      for( std::vector<edm::Ptr<reco::Vertex>>::const_iterator  vtx = recoVertices.begin(); vtx != recoVertices.end(); ++vtx){
	if(fabs(itrk->dz((*vtx)->position())) < fabs(itrk->dz((*vtxClose)->position()))) vtxClose = vtx;
      }
  	
      if(vtxClose == vtxLead){
	Float_t dz = itrk->dz((*vtxClose)->position());
	Float_t dz_sigma = sqrt(pow(itrk->dzError(),2) + pow((*vtxClose)->zError(),2));
  	
	if(itrk->quality(reco::TrackBase::qualityByName("highPurity")) && fabs(dz/dz_sigma) < 5.){
	  trkForAxis = true;
	  Float_t d0 = itrk->dxy((*vtxClose)->position());
	  Float_t d0_sigma = sqrt(pow(itrk->d0Error(),2) + pow((*vtxClose)->xError(),2) + pow((*vtxClose)->yError(),2));
	  if(fabs(d0/d0_sigma) < 5.) nChg_QC++;
	}
      }
    } else {								//No track --> neutral particle
      if(part->pt() > 1.0) nNeutral_ptCut++;
      trkForAxis = true;
    }
    
    Float_t deta = part->eta() - jet->eta();
    Float_t dphi = 2*atan(tan(((part->phi()- jet->phi()))/2));           
    Float_t partPt = part->pt(); 
    Float_t weight = partPt*partPt;

    if(!useQC || trkForAxis){					//If quality cuts, only use when trkForAxis
      sum_weight += weight;
      sum_pt += partPt;
      sum_deta += deta*weight;                  
      sum_dphi += dphi*weight;                                                                                             
      sum_deta2 += deta*deta*weight;                    
      sum_detadphi += deta*dphi*weight;                               
      sum_dphi2 += dphi*dphi*weight;
    }	
  }

  //Calculate axis and ptD
  Float_t a = 0., b = 0., c = 0.;
  Float_t ave_deta = 0., ave_dphi = 0., ave_deta2 = 0., ave_dphi2 = 0.;
  if(sum_weight > 0){
    if (myvar == "ptD")
      return sqrt(sum_weight)/sum_pt;
    ave_deta = sum_deta/sum_weight;
    ave_dphi = sum_dphi/sum_weight;
    ave_deta2 = sum_deta2/sum_weight;
    ave_dphi2 = sum_dphi2/sum_weight;
    a = ave_deta2 - ave_deta*ave_deta;                          
    b = ave_dphi2 - ave_dphi*ave_dphi;                          
    c = -(sum_detadphi/sum_weight - ave_deta*ave_dphi);                
  } 
  else if(myvar == "ptD")
    return 0;
  Float_t delta = sqrt(fabs((a-b)*(a-b)+4*c*c));
  
  if(myvar == "axis1")
    return (a+b+delta > 0) ? sqrt(0.5*(a+b+delta)) : 0.;
  else if(myvar == "axis2")
    return (a+b-delta > 0) ? sqrt(0.5*(a+b-delta)) : 0.;
  else if(myvar == "mult")
    return (nChg_QC + nNeutral_ptCut);
  else if(myvar == "mult_MLP_QC")
    return (nChg_QC );
  else if(myvar == "mult_MLP")
    return (nChg_ptCut + nNeutral_ptCut );
  
  return -1.;
}

}
