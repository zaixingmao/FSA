//////////////////////////////////////////////////////////////////////////////
//									    //
//   MiniAODElectronMVAIDEmbedder.cc    				    //
//									    //
//   Takes MVA ID values from the common ID framework                       //
//       and embeds them as user floats in the electron                     //
//									    //
//   Author: Nate Woods, U. Wisconsin					    //
//									    //
//////////////////////////////////////////////////////////////////////////////


// system includes
#include <memory>
#include <vector>

// CMS includes
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Common/interface/View.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "EgammaAnalysis/ElectronTools/interface/EGammaMvaEleEstimatorCSA14.h"


class MiniAODElectronMVAIDEmbedder : public edm::EDProducer
{
public:
  explicit MiniAODElectronMVAIDEmbedder(const edm::ParameterSet&);
  ~MiniAODElectronMVAIDEmbedder() {}

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  // Methods
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  // Data
  edm::EDGetTokenT<edm::View<pat::Electron> > electronCollectionToken_;
  // ID decisions objects
  edm::EDGetTokenT<edm::ValueMap<bool> > eleMediumIdMapToken_;
  edm::EDGetTokenT<edm::ValueMap<bool> > eleTightIdMapToken_;
  std::vector<Int_t> passMediumId_;
  std::vector<Int_t> passTightId_;

};


// Constructors and destructors

MiniAODElectronMVAIDEmbedder::MiniAODElectronMVAIDEmbedder(const edm::ParameterSet& iConfig):
  electronCollectionToken_(consumes<edm::View<pat::Electron> >(iConfig.exists("src") ?
							       iConfig.getParameter<edm::InputTag>("src") :
							       edm::InputTag("slimmedElectrons"))),
  eleMediumIdMapToken_(consumes<edm::ValueMap<bool> >(iConfig.getParameter<edm::InputTag>("eleMediumIdMap"))),
  eleTightIdMapToken_(consumes<edm::ValueMap<bool> >(iConfig.getParameter<edm::InputTag>("eleTightIdMap")))
{
  produces<std::vector<pat::Electron> >();
}


void MiniAODElectronMVAIDEmbedder::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  out = std:: auto_ptr<std::vector<pat::Electron> >(new std::vector<pat::Electron>);

  //  out->clear();

  edm::Handle<edm::View<pat::Electron> > electrons;
  iEvent.getByToken(electronCollectionToken_, electrons);

  edm::Handle<edm::ValueMap<bool> > medium_id_decisions;
  edm::Handle<edm::ValueMap<bool> > tight_id_decisions; 
  iEvent.getByToken(eleMediumIdMapToken_,medium_id_decisions);
  iEvent.getByToken(eleTightIdMapToken_,tight_id_decisions);

  for(edm::View<pat::Electron>::const_iterator e = electrons->begin();
      e != electrons->end(); e++) // loop over electrons
    {
      out->push_back(*e); // copy electron to save correctly in event
      bool isPassMedium = (*medium_id_decisions)[*e];
      bool isPassTight  = (*tight_id_decisions)[*e];

      
      out->back().addUserFloat("MVAID_Medium", (int) isPassMedium);
      out->back().addUserFloat("MVAID_Tight", (int) isPassTight);
    }

  iEvent.put(out);
}


void MiniAODElectronMVAIDEmbedder::beginJob()
{}


void MiniAODElectronMVAIDEmbedder::endJob()
{}


void
MiniAODElectronMVAIDEmbedder::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(MiniAODElectronMVAIDEmbedder);








