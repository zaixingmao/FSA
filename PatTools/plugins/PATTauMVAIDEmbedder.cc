#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/PATTauDiscriminator.h"

#include "DataFormats/TauReco/interface/PFTau.h"
#include "DataFormats/TauReco/interface/PFTauFwd.h"
#include "DataFormats/TauReco/interface/PFTauDiscriminator.h"
#include "DataFormats/TauReco/interface/PFTauTransverseImpactParameterAssociation.h"

#include "RecoTauTag/RecoTau/interface/PFRecoTauClusterVariables.h"

class PATTauMVAIDEmbedder : public edm::EDProducer {
  public:
    PATTauMVAIDEmbedder(const edm::ParameterSet& pset);
    virtual ~PATTauMVAIDEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    edm::EDGetTokenT<pat::TauCollection> tauToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVLooseToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationTightToken_;
};

PATTauMVAIDEmbedder::PATTauMVAIDEmbedder(
    const edm::ParameterSet& pset)
{
  src_ = pset.getParameter<edm::InputTag>("src");
  tauToken_ = consumes<pat::TauCollection>(src_);
  mvaIsolationToken_ = consumes<pat::PATTauDiscriminator>(edm::InputTag("rerunDiscriminationByIsolationMVA2016v1raw"));
  mvaIsolationVLooseToken_ = consumes<pat::PATTauDiscriminator>(edm::InputTag("rerunDiscriminationByIsolationMVA2016v1VLoose"));
  mvaIsolationTightToken_ = consumes<pat::PATTauDiscriminator>(edm::InputTag("rerunDiscriminationByIsolationMVA2016v1Tight"));
  produces<pat::TauCollection>();
}

void PATTauMVAIDEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {

  edm::Handle<pat::TauCollection> taus;
  evt.getByToken(tauToken_,taus);

  edm::Handle<pat::PATTauDiscriminator> mvaIsoRaw;
  evt.getByToken(mvaIsolationToken_,mvaIsoRaw);

  edm::Handle<pat::PATTauDiscriminator> mvaIsoVLoose;
  evt.getByToken(mvaIsolationVLooseToken_,mvaIsoVLoose);

  edm::Handle<pat::PATTauDiscriminator> mvaIsoTight;
  evt.getByToken(mvaIsolationTightToken_,mvaIsoTight);

  size_t nTaus = taus->size();

  std::auto_ptr<pat::TauCollection> output(new pat::TauCollection);
  output->reserve(nTaus);

  for (size_t i = 0; i < nTaus; ++i) {

    pat::Tau origTau = taus->at(i);
	pat::TauRef tau(taus,i);

    origTau.addUserFloat("newMVAIDraw", (*mvaIsoRaw)[tau]);
    origTau.addUserInt("newMVAIDVLoose", (*mvaIsoVLoose)[tau]);
    origTau.addUserInt("newMVAIDTight", (*mvaIsoTight)[tau]);

    output->push_back(origTau); // make our own copy

  }

  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATTauMVAIDEmbedder);
