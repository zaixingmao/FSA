#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/Candidate/interface/LeafCandidate.h"

#include "JetMETCorrections/Objects/interface/JetCorrector.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"

class PATJetSystematicsEmbedder : public edm::EDProducer {
  public:
    typedef reco::LeafCandidate ShiftedCand;
    typedef std::vector<ShiftedCand> ShiftedCandCollection;
    typedef reco::CandidatePtr CandidatePtr;
    typedef reco::Candidate::LorentzVector LorentzVector;

    PATJetSystematicsEmbedder(const edm::ParameterSet& pset);
    virtual ~PATJetSystematicsEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    std::string label_;
    double unclusteredEnergyScale_;
};

PATJetSystematicsEmbedder::PATJetSystematicsEmbedder(const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  label_ = pset.getParameter<std::string>("corrLabel");
  unclusteredEnergyScale_ = pset.getParameter<double>("unclusteredEnergyScale");
  consumes<edm::View<pat::Jet> >(src_);
  produces<pat::JetCollection>();
//   produces<ShiftedCandCollection>("p4OutJESUpJets");
//   produces<ShiftedCandCollection>("p4OutJESDownJets");
//   produces<ShiftedCandCollection>("p4OutUESUpJets");
//   produces<ShiftedCandCollection>("p4OutUESDownJets");
}
void PATJetSystematicsEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::auto_ptr<pat::JetCollection> output(new pat::JetCollection);

  edm::Handle<edm::View<pat::Jet> > jets;
  evt.getByLabel(src_, jets);
  size_t nJets = jets->size();
// 
  std::auto_ptr<ShiftedCandCollection> p4OutJESUpJets(new ShiftedCandCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutJESDownJets(new ShiftedCandCollection);
//   std::auto_ptr<ShiftedCandCollection> p4OutUESUpJets(new ShiftedCandCollection);
//   std::auto_ptr<ShiftedCandCollection> p4OutUESDownJets(new ShiftedCandCollection);

  p4OutJESUpJets->reserve(nJets);
  p4OutJESDownJets->reserve(nJets);

//   p4OutJESUpJets->reserve(nJets);
//   p4OutJESDownJets->reserve(nJets);
//   p4OutUESUpJets->reserve(nJets);
//   p4OutUESDownJets->reserve(nJets);

  edm::ESHandle<JetCorrectorParametersCollection> JetCorParColl;
  es.get<JetCorrectionsRecord>().get(label_, JetCorParColl);
  JetCorrectorParameters const & JetCorPar = (*JetCorParColl)["Uncertainty"];
  std::auto_ptr<JetCorrectionUncertainty> jecUnc(
      new JetCorrectionUncertainty(JetCorPar));

  for (size_t i = 0; i < nJets; ++i) {
    pat::Jet jet = jets->at(i);

    double unc = 0;
    double pt_up = 0;
    double pt_down = 0;


    if (std::abs(jet.eta()) < 5.2 && jet.pt() > 20) {
      jecUnc->setJetEta(jet.eta());
      jecUnc->setJetPt(jet.pt()); // here you must use the CORRECTED jet pt
      unc = jecUnc->getUncertainty(true);
      // Get uncorrected pt
      assert(jet.jecSetsAvailable());

      LorentzVector uncDown = (1-unc)*jet.p4();
      LorentzVector uncUp = (1+unc)*jet.p4();
      //     LorentzVector uncUESDown = (1-unclusteredEnergyScale_)*jet.p4();
      //     LorentzVector uncUESUp = (1+unclusteredEnergyScale_)*jet.p4();

      ShiftedCand candUncDown = jet;
      candUncDown.setP4(uncDown);
      ShiftedCand candUncUp = jet;
      candUncUp.setP4(uncUp);
      pt_up = candUncUp.pt();
      pt_down = candUncDown.pt();
    }
    jet.addUserFloat("jes+", float(pt_up));
    jet.addUserFloat("jes-", float(pt_down));


    // Get uncorrected pt
    assert(jet.jecSetsAvailable());

    LorentzVector uncDown = (1-unc)*jet.p4();
    LorentzVector uncUp = (1+unc)*jet.p4();

    ShiftedCand candUncDown = jet;
    candUncDown.setP4(uncDown);
    ShiftedCand candUncUp = jet;
    candUncUp.setP4(uncUp);
    jet.addUserFloat("jes+", uncUp.pt());
    jet.addUserFloat("jes-", uncDown.pt());

    output->push_back(jet); // make our own copy


  }

//   typedef edm::OrphanHandle<ShiftedCandCollection> PutHandle;
//   PutHandle p4OutJESUpJetsH = evt.put(p4OutJESUpJets, "p4OutJESUpJets");
//   PutHandle p4OutJESDownJetsH = evt.put(p4OutJESDownJets, "p4OutJESDownJets");
//   PutHandle p4OutUESUpJetsH = evt.put(p4OutUESUpJets, "p4OutUESUpJets");
//   PutHandle p4OutUESDownJetsH = evt.put(p4OutUESDownJets, "p4OutUESDownJets");


  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATJetSystematicsEmbedder);
