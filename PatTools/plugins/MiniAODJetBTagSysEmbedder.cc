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

class MiniAODJetBTagSysEmbedder : public edm::EDProducer {
  public:
    MiniAODJetBTagSysEmbedder(const edm::ParameterSet& pset);
    virtual ~MiniAODJetBTagSysEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
    void setBTSF(BtagSFV * btsf) {btsf_=  btsf;}

  private:
    edm::InputTag src_;
    bool isData_;
    int isMC_;

    BtagSFV* btsf_;
    bool btaggedL_bTagSysUp;
    bool btaggedL_bTagSysDown;
    bool btaggedL_bTagMisUp;
    bool btaggedL_bTagMisDown;
    bool btaggedL_bTagUp;
    bool btaggedL_bTagDown;

};

MiniAODJetBTagSysEmbedder::MiniAODJetBTagSysEmbedder(const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  isMC_ = pset.getParameter<int>("isMC");
  if(isMC_) isData_ = false;
  else isData_ = true;
  produces<pat::JetCollection>();
}

void MiniAODJetBTagSysEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::auto_ptr<pat::JetCollection> output(new pat::JetCollection);

  edm::Handle<edm::View<pat::Jet> > input;
  evt.getByLabel(src_, input);

  output->reserve(input->size());


  for (size_t i = 0; i < input->size(); ++i) {
    pat::Jet jet = input->at(i);
    btaggedL_bTagSysUp = false;
    btaggedL_bTagSysDown = false;
    btaggedL_bTagMisUp = false;
    btaggedL_bTagMisDown = false;
    btaggedL_bTagUp = false;
    btaggedL_bTagDown = false;

    if(jet.pt() > 30 && fabs(jet.eta())<2.4){
        btaggedL_bTagSysUp = btsf_->isbtagged(jet.pt(), jet.eta(), jet.phi(), jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags"),jet.partonFlavour(), isData_, 2, 0, 0.605);
        btaggedL_bTagSysDown = btsf_->isbtagged(jet.pt(), jet.eta(), jet.phi(),jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags"),jet.partonFlavour(), isData_, 1, 0, 0.605);
        btaggedL_bTagMisUp = btsf_->isbtagged(jet.pt(), jet.eta(), jet.phi(),jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags"),jet.partonFlavour(), isData_, 0, 2, 0.605);
        btaggedL_bTagMisDown = btsf_->isbtagged(jet.pt(), jet.eta(), jet.phi(),jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags"),jet.partonFlavour(), isData_, 0, 1, 0.605);
        btaggedL_bTagUp = btsf_->isbtagged(jet.pt(), jet.eta(), jet.phi(),jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags"),jet.partonFlavour(), isData_, 2, 2, 0.605);
        btaggedL_bTagDown = btsf_->isbtagged(jet.pt(), jet.eta(), jet.phi(),jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags"),jet.partonFlavour(), isData_, 1, 1, 0.605);
     }
    jet.addUserFloat("CSVL_sysUp", float(btaggedL_bTagSysUp));
    jet.addUserFloat("CSVL_sysDown", float(btaggedL_bTagSysDown));
    jet.addUserFloat("CSVL_misUp", float(btaggedL_bTagMisUp));
    jet.addUserFloat("CSVL_misDown", float(btaggedL_bTagMisDown));
    jet.addUserFloat("CSVL_up", float(btaggedL_bTagUp));
    jet.addUserFloat("CSVL_down", float(btaggedL_bTagDown));

    output->push_back(jet);
  }

  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODJetBTagSysEmbedder);
