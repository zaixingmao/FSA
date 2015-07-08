/** \class MiniAODTauIpEmbedder
 *
 * Embed the track IP w.r.t an input PV as a user float in a pat collection
 * Also embeds the 3D & 2D IP and significance
 *
 * \author Konstantinos A. Petridis, Imperial College;
 *  modified by Christian Veelken
 *  modified by Evan Friis
 *  modified by Devin Taylor (for miniAOD)
 *
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"

#include "FWCore/Framework/interface/MakerMacros.h"

#include <vector>

class MiniAODTauIpEmbedder : public edm::EDProducer {
  public:
    MiniAODTauIpEmbedder(const edm::ParameterSet& pset);
    virtual ~MiniAODTauIpEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    edm::InputTag vtxSrc_;
};

MiniAODTauIpEmbedder::MiniAODTauIpEmbedder(const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  vtxSrc_ = pset.getParameter<edm::InputTag>("vtxSrc");
  produces<std::vector<pat::Tau> >();
}

void MiniAODTauIpEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {

  std::auto_ptr<std::vector<pat::Tau> > output(new std::vector<pat::Tau>());

  edm::Handle<edm::View<pat::Tau> > handle;
  evt.getByLabel(src_, handle);

  edm::Handle<reco::VertexCollection> vertices;
  evt.getByLabel(vtxSrc_, vertices);

  const reco::Vertex& thePV = *vertices->begin();

  for (size_t iObject = 0; iObject < handle->size(); ++iObject) {
    const pat::Tau& tau = handle->at(iObject);
    double ip = -1;
    double dz = -1;
    double vz = -999;

    if(!tau.leadChargedHadrCand().isNull()){
        pat::PackedCandidate const* packedLeadTauCand = dynamic_cast<pat::PackedCandidate const*>(tau.leadChargedHadrCand().get());
        ip = packedLeadTauCand->dxy(thePV.position());
        dz = packedLeadTauCand->dz(thePV.position());
        vz = packedLeadTauCand->vz();
    }

    pat::Tau newObject = tau;
    newObject.addUserFloat("ipDXY", ip);
    newObject.addUserFloat("dz", dz);
    newObject.addUserFloat("vz", vz);
    output->push_back(newObject);
  }

  evt.put(output);
}

DEFINE_FWK_MODULE(MiniAODTauIpEmbedder);
