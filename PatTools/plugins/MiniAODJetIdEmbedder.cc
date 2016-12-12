/*
 * Embed PF Jet IDs (see https://twiki.cern.ch/twiki/bin/view/CMS/JetID)
 * into pat::Jets
 *
 * Author: Evan K. Friis, UW Madison
 */


#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FinalStateAnalysis/PatTools/interface/BTagSF.h"

class MiniAODJetIdEmbedder : public edm::EDProducer {
  public:
    MiniAODJetIdEmbedder(const edm::ParameterSet& pset);
    virtual ~MiniAODJetIdEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
    void setBTSF(BtagSFV * btsf) {btsf_=  btsf;}

  private:
    edm::InputTag src_;
    bool isData_;
    int isMC_;

    BtagSFV* btsf_; 

};

MiniAODJetIdEmbedder::MiniAODJetIdEmbedder(const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  consumes<edm::View<pat::Jet>>(src_);
  isMC_ = pset.getParameter<int>("isMC");
  if(isMC_) isData_ = false;
  else isData_ = true;
  produces<pat::JetCollection>();
}

void MiniAODJetIdEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::auto_ptr<pat::JetCollection> output(new pat::JetCollection);

  edm::Handle<edm::View<pat::Jet> > input;
  evt.getByLabel(src_, input);

  output->reserve(input->size());
  //bool btaggedL = false;
//   bool btaggedL_bTagSysUp = false;
//   bool btaggedL_bTagSysDown = false;
//   bool btaggedL_bTagMisUp = false;
//   bool btaggedL_bTagMisDown = false;
//   bool btaggedL_bTagUp = false;
//   bool btaggedL_bTagDown = false;
  for (size_t i = 0; i < input->size(); ++i) {
    pat::Jet jet = input->at(i);
    bool loose = true;
    bool tight = true;
    bool tightLepVeto = true;
//     bool btaggedL = false;


    double NHF = jet.neutralHadronEnergyFraction();
    double NEMF = jet.neutralEmEnergyFraction();
    double CHF = jet.chargedHadronEnergyFraction();
    double MUF = jet.muonEnergyFraction();
    double CEMF = jet.chargedEmEnergyFraction();
    double NumConst = jet.chargedMultiplicity()+jet.neutralMultiplicity();
    double NumNeutralParticles =jet.neutralMultiplicity();
    double CHM = jet.chargedMultiplicity();
    double eta = jet.eta();
    if (std::abs(eta) <= 2.7){
      loose = (NHF<0.99 && NEMF<0.99 && NumConst>1) && ((abs(eta)<=2.4 && CHF>0 && CHM>0 && CEMF<0.99) || std::abs(eta)>2.4) && std::abs(eta)<=2.7;
      tight = (NHF<0.90 && NEMF<0.90 && NumConst>1) && ((std::abs(eta)<=2.4 && CHF>0 && CHM>0 && CEMF<0.99) || std::abs(eta)>2.4) && std::abs(eta)<=2.7;
      tightLepVeto = (NHF<0.90 && NEMF<0.90 && NumConst>1 && MUF<0.8) && ((std::abs(eta)<=2.4 && CHF>0 && CHM>0 && CEMF<0.90) || std::abs(eta)>2.4) && std::abs(eta)<=2.7;
    }
    else if(std::abs(eta) <= 3.0){
      loose = (NEMF<0.90 && NumNeutralParticles>2 && std::abs(eta)>2.7 && std::abs(eta)<=3.0);
      tight = (NEMF<0.90 && NumNeutralParticles>2 && std::abs(eta)>2.7 && std::abs(eta)<=3.0);
    }
    else{
      loose = (NEMF<0.90 && NumNeutralParticles>10 && std::abs(eta)>3.0);
      tight = (NEMF<0.90 && NumNeutralParticles>10 && std::abs(eta)>3.0);
    }
    jet.addUserFloat("idLoose", loose);
    jet.addUserFloat("idTight", tight);
    jet.addUserFloat("idTightLepVeto", tightLepVeto);

    // Pileup discriminant
    bool passPU = true;
    float jpumva = jet.userFloat("pileupJetId:fullDiscriminant");
    if(jet.pt() > 20)
      {
	if(fabs(jet.eta()) > 3.)
	  {
	    if(jpumva <= -0.45) passPU = false;
	  }
	else if(fabs(jet.eta()) > 2.75)
	  {
	    if(jpumva <= -0.55) passPU = false;
	  }
	else if(fabs(jet.eta()) > 2.5)
	  {
	    if(jpumva <= -0.6) passPU = false;
	  }
	else if(jpumva <= -0.63) passPU = false;
      }
    else
      {
	if(fabs(jet.eta()) > 3.)
	  {
	    if(jpumva <= -0.95) passPU = false;
	  }
	else if(fabs(jet.eta()) > 2.75)
	  {
	    if(jpumva <= -0.94) passPU = false;
	  }
	else if(fabs(jet.eta()) > 2.5)
	  {
	    if(jpumva <= -0.96) passPU = false;
	  }
	else if(jpumva <= -0.95) passPU = false;
      }

    jet.addUserFloat("puID", float(passPU));
    output->push_back(jet);
  }

  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODJetIdEmbedder);
