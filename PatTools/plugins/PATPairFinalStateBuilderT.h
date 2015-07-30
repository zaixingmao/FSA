#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"
#include "FinalStateAnalysis/DataFormats/interface/PATPairFinalStateT.h"

template<class FinalStatePair>
class PATPairFinalStateBuilderT : public edm::EDProducer {
  public:
    typedef std::vector<FinalStatePair> FinalStatePairCollection;

    PATPairFinalStateBuilderT(const edm::ParameterSet& pset);
    virtual ~PATPairFinalStateBuilderT(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag leg1Src_;
    edm::InputTag leg2Src_;
    edm::InputTag evtSrc_;
    edm::InputTag tautauMVAMetSrc_;
    StringCutObjectSelector<PATFinalState> cut_;
};

template<class FinalStatePair>
PATPairFinalStateBuilderT<FinalStatePair>::PATPairFinalStateBuilderT(
    const edm::ParameterSet& pset):
  cut_(pset.getParameter<std::string>("cut"), true) {
  leg1Src_ = pset.getParameter<edm::InputTag>("leg1Src");
  leg2Src_ = pset.getParameter<edm::InputTag>("leg2Src");
  evtSrc_ = pset.getParameter<edm::InputTag>("evtSrc");
  tautauMVAMetSrc_ = pset.getParameter<edm::InputTag>("tautauMVAMETSrc");

  produces<FinalStatePairCollection>();
}

template<class FinalStatePair> void
PATPairFinalStateBuilderT<FinalStatePair>::produce(
    edm::Event& evt, const edm::EventSetup& es) {

  edm::Handle<edm::View<PATFinalStateEvent> > fsEvent;
  evt.getByLabel(evtSrc_, fsEvent);
  edm::Ptr<PATFinalStateEvent> evtPtr = fsEvent->ptrAt(0);
  assert(evtPtr.isNonnull());

  std::auto_ptr<FinalStatePairCollection> output(new FinalStatePairCollection);

  edm::Handle<edm::View<typename FinalStatePair::daughter1_type> > leg1s;
  evt.getByLabel(leg1Src_, leg1s);

  edm::Handle<edm::View<typename FinalStatePair::daughter2_type> > leg2s;
  evt.getByLabel(leg2Src_, leg2s);

  edm::Handle<edm::View<pat::MET> > metCands;
  evt.getByLabel(tautauMVAMetSrc_, metCands);

  for (size_t iLeg1 = 0; iLeg1 < leg1s->size(); ++iLeg1) {
    edm::Ptr<typename FinalStatePair::daughter1_type> leg1 = leg1s->ptrAt(iLeg1);
    assert(leg1.isNonnull());
    for (size_t iLeg2 = 0; iLeg2 < leg2s->size(); ++iLeg2) {
      edm::Ptr<typename FinalStatePair::daughter2_type> leg2 = leg2s->ptrAt(iLeg2);
      assert(leg2.isNonnull());

      // Skip if the two objects are the same thing.
      if (reco::CandidatePtr(leg1) == reco::CandidatePtr(leg2))
        continue;

//       edm::Ptr<pat::MET> tautauMVAMET;
//       std::cout<<"leg1_p4: "<<leg1->p4()<<std::endl;
//       std::cout<<"leg2_p4: "<<leg2->p4()<<std::endl;
// 
//       for(size_t iMEt = 0; iMEt < metCands->size(); iMEt++){
//         if(leg1->p4() == (metCands->at(iMEt)).userCand("lepton1").get()->p4() && leg2->p4() == (metCands->at(iMEt)).userCand("lepton2").get()->p4()){
//             tautauMVAMET = metCands->ptrAt(iMEt);
//             break;
//         }
//         else if(leg1->p4() == (metCands->at(iMEt)).userCand("lepton2").get()->p4() && leg2->p4() == (metCands->at(iMEt)).userCand("lepton1").get()->p4()){
//             tautauMVAMET = metCands->ptrAt(iMEt);
//             break;
//         }
//       }
//       std::string outName = "tautauMVAMET";
//       std::cout<<"MET: "<<tautauMVAMET->pt()<<std::endl;
//       evtPtr->addMET(outName, tautauMVAMET);
      FinalStatePair outputCand(leg1, leg2, evtPtr);
      if (cut_(outputCand))
        output->push_back(outputCand);
    }
  }
  evt.put(output);
}
