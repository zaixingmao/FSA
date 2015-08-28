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

#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "RecoVertex/KinematicFitPrimitives/interface/KinematicParticleFactoryFromTransientTrack.h"


#include <vector>

class MiniAODTauIpEmbedder : public edm::EDProducer {
  public:
    MiniAODTauIpEmbedder(const edm::ParameterSet& pset);
    virtual ~MiniAODTauIpEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    edm::InputTag vtxSrc_;
    bool isGoodVertex(const reco::Vertex& vtxxx);
    int tau_vtx_ndof_min_, tau_vtx_rho_max_;
    double tau_vtx_position_z_max_;
    edm::InputTag beamSpot_;
    bool TNT;
};

MiniAODTauIpEmbedder::MiniAODTauIpEmbedder(const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  vtxSrc_ = pset.getParameter<edm::InputTag>("vtxSrc");
  beamSpot_                = pset.getParameter<edm::InputTag>("beamSpot");
  tau_vtx_ndof_min_       = pset.getParameter<int>("Tau_vtx_ndof_min");
  tau_vtx_rho_max_        = pset.getParameter<int>("Tau_vtx_rho_max");
  tau_vtx_position_z_max_ = pset.getParameter<double>("Tau_vtx_position_z_max");
  TNT = pset.getParameter<bool>("TNT");
  produces<std::vector<pat::Tau> >();
}

void MiniAODTauIpEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {

  std::auto_ptr<std::vector<pat::Tau> > output(new std::vector<pat::Tau>());

  edm::Handle<edm::View<pat::Tau> > handle;
  evt.getByLabel(src_, handle);

  edm::Handle<reco::VertexCollection> vertices;
  evt.getByLabel(vtxSrc_, vertices);


  reco::VertexCollection::const_iterator firstGoodVertex = vertices->end();
  for (reco::VertexCollection::const_iterator it = vertices->begin(); it != vertices->end(); it++) {
    if (isGoodVertex(*it)) {
        firstGoodVertex = it;
        break;
    }
  }
  reco::BeamSpot beamSpot;
  edm::Handle<reco::BeamSpot> beamSpotHandle;
  math::XYZPoint point;
  GlobalPoint thebs, thepv;
  edm::ESHandle<TransientTrackBuilder> theB;
  if(TNT){
      es.get<TransientTrackRecord>().get("TransientTrackBuilder",theB);
      GlobalPoint thepv(firstGoodVertex->position().x(),firstGoodVertex->position().y(),firstGoodVertex->position().z());

     // Get BeamSpot Information
      reco::BeamSpot beamSpot;
      edm::Handle<reco::BeamSpot> beamSpotHandle;
      evt.getByLabel(beamSpot_, beamSpotHandle);
      if ( beamSpotHandle.isValid() )  beamSpot = *beamSpotHandle;
      math::XYZPoint point(beamSpot.x0(),beamSpot.y0(), beamSpot.z0());
      GlobalPoint thebs(beamSpot.x0(),beamSpot.y0(),beamSpot.z0());
  }

  const reco::Vertex& thePV = *vertices->begin();

  const float pionMass = 0.139570;
  float pionSigma = pionMass*1e-6;
  float chi2 = 0.0;
  float ndf = 0.0;

  for (size_t iObject = 0; iObject < handle->size(); ++iObject) {
    const pat::Tau& tau = handle->at(iObject);
    double ip = -1;
    double dz = -1;
    double vz = -999;

    if(!tau.leadChargedHadrCand().isNull()){
        pat::PackedCandidate const* packedLeadTauCand = dynamic_cast<pat::PackedCandidate const*>(tau.leadChargedHadrCand().get());
        ip = packedLeadTauCand->dxy();
        dz = packedLeadTauCand->dz();
        vz = packedLeadTauCand->vz();
    }

    pat::Tau newObject = tau;
    newObject.addUserFloat("ipDXY", ip);
    newObject.addUserFloat("dz", dz);
    newObject.addUserFloat("vz", vz);

    if(!tau.leadTrack().isNull() && TNT){
        newObject.addUserFloat("_leadChargedCandDxy_pv", tau.leadTrack()->dxy(firstGoodVertex->position()));
        newObject.addUserFloat("_leadChargedCandDxy_bs", -1.*(tau.leadTrack()->dxy(point)));
        newObject.addUserFloat("_leadChargedCandDz_pv", tau.leadTrack()->dz(firstGoodVertex->position()));
        newObject.addUserFloat("_leadChargedCandDz_bs", tau.leadTrack()->dz(point));

        // tau lead track point of closest approach (PCA) to the beamspot and primary vertex
        reco::TransientTrack tauTransTkPtr = theB->build(*(tau.leadTrack()));
        GlobalPoint tauLeadTrack_pca_bs = tauTransTkPtr.trajectoryStateClosestToPoint(thebs).position();
        GlobalPoint tauLeadTrack_pca_pv = tauTransTkPtr.trajectoryStateClosestToPoint(thepv).position();
        newObject.addUserFloat("_leadChargedCandTrack_PCAx_bs", tauLeadTrack_pca_bs.x());
        newObject.addUserFloat("_leadChargedCandTrack_PCAy_bs", tauLeadTrack_pca_bs.y());
        newObject.addUserFloat("_leadChargedCandTrack_PCAz_bs", tauLeadTrack_pca_bs.z());
        newObject.addUserFloat("_leadChargedCandTrack_PCAx_pv", tauLeadTrack_pca_pv.x());
        newObject.addUserFloat("_leadChargedCandTrack_PCAy_pv", tauLeadTrack_pca_pv.y());
        newObject.addUserFloat("_leadChargedCandTrack_PCAz_pv", tauLeadTrack_pca_pv.z());

        // extract track fit errors
        KinematicParticleFactoryFromTransientTrack pFactory;
        RefCountedKinematicParticle tauParticle = pFactory.particle(tauTransTkPtr, pionMass, chi2, ndf, pionSigma);
        newObject.addUserFloat("_leadChargedCandTrackFitErrorMatrix_00", tauParticle->stateAtPoint(tauLeadTrack_pca_bs).kinematicParametersError().matrix()(0,0));
        newObject.addUserFloat("_leadChargedCandTrackFitErrorMatrix_01", tauParticle->stateAtPoint(tauLeadTrack_pca_bs).kinematicParametersError().matrix()(0,1));
        newObject.addUserFloat("_leadChargedCandTrackFitErrorMatrix_02", tauParticle->stateAtPoint(tauLeadTrack_pca_bs).kinematicParametersError().matrix()(0,2));
        newObject.addUserFloat("_leadChargedCandTrackFitErrorMatrix_11", tauParticle->stateAtPoint(tauLeadTrack_pca_bs).kinematicParametersError().matrix()(1,1));
        newObject.addUserFloat("_leadChargedCandTrackFitErrorMatrix_12", tauParticle->stateAtPoint(tauLeadTrack_pca_bs).kinematicParametersError().matrix()(1,2));
        newObject.addUserFloat("_leadChargedCandTrackFitErrorMatrix_22", tauParticle->stateAtPoint(tauLeadTrack_pca_bs).kinematicParametersError().matrix()(2,2));
    }
    else{
        newObject.addUserFloat("_leadChargedCandDxy_pv", -9999);
        newObject.addUserFloat("_leadChargedCandDxy_bs", -9999);
        newObject.addUserFloat("_leadChargedCandDz_pv", -9999);
        newObject.addUserFloat("_leadChargedCandDz_bs", -9999);

        newObject.addUserFloat("_leadChargedCandTrack_PCAx_bs", -9999);
        newObject.addUserFloat("_leadChargedCandTrack_PCAy_bs", -9999);
        newObject.addUserFloat("_leadChargedCandTrack_PCAz_bs", -9999);
        newObject.addUserFloat("_leadChargedCandTrack_PCAx_pv", -9999);
        newObject.addUserFloat("_leadChargedCandTrack_PCAy_pv", -9999);
        newObject.addUserFloat("_leadChargedCandTrack_PCAz_pv", -9999);

        // extract track fit errors
        newObject.addUserFloat("_leadChargedCandTrackFitErrorMatrix_00", -9999);
        newObject.addUserFloat("_leadChargedCandTrackFitErrorMatrix_01", -9999);
        newObject.addUserFloat("_leadChargedCandTrackFitErrorMatrix_02", -9999);
        newObject.addUserFloat("_leadChargedCandTrackFitErrorMatrix_11", -9999);
        newObject.addUserFloat("_leadChargedCandTrackFitErrorMatrix_12", -9999);
        newObject.addUserFloat("_leadChargedCandTrackFitErrorMatrix_22", -9999);
    }
    output->push_back(newObject);
  }

  evt.put(output);
}

bool MiniAODTauIpEmbedder::isGoodVertex(const reco::Vertex& vtxxx) {
  if (vtxxx.isFake()) return false;
  if (vtxxx.ndof() < tau_vtx_ndof_min_) return false;
  if (vtxxx.position().Rho() > tau_vtx_rho_max_) return false;
  if (fabs(vtxxx.position().Z()) > tau_vtx_position_z_max_) return false;
  return true;
}

DEFINE_FWK_MODULE(MiniAODTauIpEmbedder);
