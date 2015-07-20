/*
 * Embeds the muon ID as recommended by the Muon POG
 * Author: Devin N. Taylor, UW-Madison
 */

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "DataFormats/PatCandidates/interface/Muon.h"

#include <math.h>

// class declaration
class MiniAODMuonIDEmbedder : public edm::EDProducer {
  public:
    explicit MiniAODMuonIDEmbedder(const edm::ParameterSet& pset);
    bool mediumMuon(const pat::Muon & muon);
    virtual ~MiniAODMuonIDEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);

  private:
    edm::EDGetTokenT<pat::MuonCollection> muonsCollection_;
    edm::EDGetTokenT<reco::VertexCollection> vtxToken_;
    reco::Vertex pv_;
};

// class member functions
MiniAODMuonIDEmbedder::MiniAODMuonIDEmbedder(const edm::ParameterSet& pset) {
  muonsCollection_ = consumes<pat::MuonCollection>(pset.getParameter<edm::InputTag>("src"));
  vtxToken_            = consumes<reco::VertexCollection>(pset.getParameter<edm::InputTag>("vertices"));

  produces<pat::MuonCollection>();
}

bool MiniAODMuonIDEmbedder::mediumMuon(const pat::Muon & recoMu) 
   {
      bool goodGlob = recoMu.isGlobalMuon() && 
                      recoMu.globalTrack()->normalizedChi2() < 3 && 
                      recoMu.combinedQuality().chi2LocalPosition < 12 && 
                      recoMu.combinedQuality().trkKink < 20; 
      bool isMedium = muon::isLooseMuon(recoMu) && 
                      recoMu.innerTrack()->validFraction() > 0.8 && 
                      muon::segmentCompatibility(recoMu) > (goodGlob ? 0.303 : 0.451); 
      return isMedium; 
   }


void MiniAODMuonIDEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  edm::Handle<std::vector<pat::Muon>> muonsCollection;
  evt.getByToken(muonsCollection_ , muonsCollection);

  edm::Handle<reco::VertexCollection> vertices;
  evt.getByToken(vtxToken_, vertices);
  if (vertices->empty()) return; // skip the event if no PV found
  pv_ = vertices->front();

  const std::vector<pat::Muon> * muons = muonsCollection.product();

  unsigned int nbMuon =  muons->size();

  std::auto_ptr<pat::MuonCollection> output(new pat::MuonCollection);
  output->reserve(nbMuon);

  for(unsigned i = 0 ; i < nbMuon; i++){
    pat::Muon muon(muons->at(i));

    muon.addUserInt("tightID",muon.isTightMuon(pv_));
//     muon.addUserInt("mediumID",mediumMuon(muon));

    output->push_back(muon);
  }

  evt.put(output);
}

// define plugin
DEFINE_FWK_MODULE(MiniAODMuonIDEmbedder);
