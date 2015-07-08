#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

#include <vector>
#include <cmath>

template<typename T>
class MiniAODLeptonRelIsoEmbedder : public edm::EDProducer {
  public:
    MiniAODLeptonRelIsoEmbedder(const edm::ParameterSet& pset);
    float getRelIso(const pat::Muon& muon);
    float getRelIso(const pat::Electron& electron);
    virtual ~MiniAODLeptonRelIsoEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
};

template<typename T>
MiniAODLeptonRelIsoEmbedder<T>::MiniAODLeptonRelIsoEmbedder(const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  produces<std::vector<T> >();
}

template<typename T>
void MiniAODLeptonRelIsoEmbedder<T>::produce(edm::Event& evt, const edm::EventSetup& es) {

  std::auto_ptr<std::vector<T> > output(new std::vector<T>());

  edm::Handle<edm::View<T> > handle;
  evt.getByLabel(src_, handle);



  for (size_t iObject = 0; iObject < handle->size(); ++iObject) {
    const T& object = handle->at(iObject);
    T newObject = object;
    newObject.addUserFloat("relIso", getRelIso(object));
    output->push_back(newObject);
  }
  evt.put(output);
}
template<typename T>
float MiniAODLeptonRelIsoEmbedder<T>::getRelIso(const pat::Muon& muon) {
    float iso = (muon.pfIsolationR03().sumChargedHadronPt + 
                 std::max(0.0, muon.pfIsolationR03().sumNeutralHadronEt +
                 muon.pfIsolationR03().sumPhotonEt -
                 0.5*muon.pfIsolationR03().sumPUPt))/muon.pt();
    return iso;
}
template<typename T>
float MiniAODLeptonRelIsoEmbedder<T>::getRelIso(const pat::Electron& electron) {
    float iso = (electron.pfIsolationVariables().sumChargedHadronPt + 
                 std::max(0.0, electron.pfIsolationVariables().sumNeutralHadronEt +
                 electron.pfIsolationVariables().sumPhotonEt -
                 0.5*electron.pfIsolationVariables().sumPUPt))/electron.pt();
    return iso;
}


typedef MiniAODLeptonRelIsoEmbedder<pat::Muon> MiniAODMuonRelIsoEmbedder;
typedef MiniAODLeptonRelIsoEmbedder<pat::Electron> MiniAODElectronRelIsoEmbedder;

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODMuonRelIsoEmbedder);
DEFINE_FWK_MODULE(MiniAODElectronRelIsoEmbedder);
