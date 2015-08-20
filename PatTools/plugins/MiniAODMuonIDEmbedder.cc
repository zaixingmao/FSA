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
    edm::InputTag beamSrc_;
    bool isGoodVertex(const reco::Vertex& vtx);
    int Muon_vtx_ndof_min_, Muon_vtx_rho_max_;
    double Muon_vtx_position_z_max_;
};

// class member functions
MiniAODMuonIDEmbedder::MiniAODMuonIDEmbedder(const edm::ParameterSet& pset) {
  muonsCollection_ = consumes<pat::MuonCollection>(pset.getParameter<edm::InputTag>("src"));
  vtxToken_            = consumes<reco::VertexCollection>(pset.getParameter<edm::InputTag>("vertices"));
  beamSrc_ = pset.getParameter<edm::InputTag>("beamSrc");

  Muon_vtx_ndof_min_      = pset.getParameter<int>("Muon_vtx_ndof_min");
  Muon_vtx_rho_max_        = pset.getParameter<int>("Muon_vtx_rho_max");
  Muon_vtx_position_z_max_ = pset.getParameter<double>("Muon_vtx_position_z_max");

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

  reco::VertexCollection::const_iterator firstGoodVertex = vertices->end();
  for (reco::VertexCollection::const_iterator it = vertices->begin(); it != firstGoodVertex; it++)
    {
      if(isGoodVertex(*it)){
        firstGoodVertex = it;
        break;
      }
    }

  reco::BeamSpot beamSpot;
  edm::Handle<reco::BeamSpot> beamSpotHandle;
  evt.getByLabel(beamSrc_, beamSpotHandle);
  if ( beamSpotHandle.isValid() )  beamSpot = *beamSpotHandle;
  math::XYZPoint point(beamSpot.x0(),beamSpot.y0(), beamSpot.z0());

  const std::vector<pat::Muon> * muons = muonsCollection.product();

  unsigned int nbMuon =  muons->size();

  std::auto_ptr<pat::MuonCollection> output(new pat::MuonCollection);
  output->reserve(nbMuon);

  for(unsigned i = 0 ; i < nbMuon; i++){
    pat::Muon muon(muons->at(i));

    // require a good vertex 
    if (firstGoodVertex == vertices->end()){
        muon.addUserInt("_tight", -9999);
        muon.addUserInt("_soft", -9999);
        muon.addUserInt("_isHightPt", -9999);
        if(muon.innerTrack().isNonnull()){
            muon.addUserFloat("_dxy", -9999);
            muon.addUserFloat("_dxy_bs", -9999);
            muon.addUserFloat("_dxy_bs_dz", -9999);
            muon.addUserFloat("_dz", -9999);
        }
    }
    else{
        muon.addUserInt("_tight",muon.isTightMuon(*firstGoodVertex));
        muon.addUserInt("_soft",muon.isSoftMuon(*firstGoodVertex));
        muon.addUserInt("_isHightPt",muon.isHighPtMuon(*firstGoodVertex));
    //     muon.addUserInt("mediumID",mediumMuon(muon));
        if(muon.innerTrack().isNonnull()){
            muon.addUserFloat("_dxy", muon.innerTrack()->dxy(firstGoodVertex->position()));
            muon.addUserFloat("_dxy_bs", (-1.)*muon.innerTrack()->dxy(point));
            muon.addUserFloat("_dxy_bs_dz", muon.innerTrack()->dz(point));
            muon.addUserFloat("_dz", muon.innerTrack()->dz(firstGoodVertex->position()));
        }
    }
    output->push_back(muon);
  }

  evt.put(output);
}

bool MiniAODMuonIDEmbedder::isGoodVertex(const reco::Vertex& vtx)
{
  if (vtx.isFake()) return false;
  if (vtx.ndof() < Muon_vtx_ndof_min_) return false;
  if (vtx.position().Rho() > Muon_vtx_rho_max_) return false;
  if (fabs(vtx.position().Z()) > Muon_vtx_position_z_max_) return false;
  return true;
}

// define plugin
DEFINE_FWK_MODULE(MiniAODMuonIDEmbedder);
