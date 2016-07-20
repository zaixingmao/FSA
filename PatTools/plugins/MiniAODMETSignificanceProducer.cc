#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/METReco/interface/METFwd.h"
#include "DataFormats/METReco/interface/PFMET.h"
#include "DataFormats/METReco/interface/PFMETFwd.h"
#include "DataFormats/METReco/interface/CommonMETData.h"

#include "RecoMET/METAlgorithms/interface/METSignificance.h"

#include <string>
#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateFwd.h"

class MiniAODMETSignificanceProducer: public edm::stream::EDProducer<>
{
    public:
      explicit MiniAODMETSignificanceProducer(const edm::ParameterSet&);
      virtual ~MiniAODMETSignificanceProducer() { }
      virtual void produce(edm::Event&, const edm::EventSetup&) override;

    private:

      // ----------member data ---------------------------

      edm::EDGetTokenT<edm::View<reco::Jet> > pfjetsToken_;
      edm::EDGetTokenT<edm::View<reco::MET> > metToken_;
      edm::EDGetTokenT<edm::View<pat::MET> > patmetToken_;

      edm::EDGetTokenT<edm::View<reco::Candidate> > pfCandidatesToken_;
      std::vector<edm::EDGetTokenT<edm::View<reco::Candidate> > > lepTokens_;
      std::auto_ptr<std::vector<pat::MET> > out; // Collection we'll output at the end

      metsig::METSignificance* metSigAlgo_;
      edm::EDGetTokenT<double> rhoToken_;
      std::string jetResPtType_;
      std::string jetResPhiType_;
      std::string jetSFType_;
};



MiniAODMETSignificanceProducer::MiniAODMETSignificanceProducer(const edm::ParameterSet& iConfig)
{
    std::vector<edm::InputTag> srcLeptonsTags = iConfig.getParameter< std::vector<edm::InputTag> >("srcLeptons");
    for(std::vector<edm::InputTag>::const_iterator it=srcLeptonsTags.begin();it!=srcLeptonsTags.end();it++) {
      lepTokens_.push_back( consumes<edm::View<reco::Candidate> >( *it ) );
    }
    pfjetsToken_    = consumes<edm::View<reco::Jet> >(iConfig.getParameter<edm::InputTag>("srcPfJets"));

    metToken_ = consumes<edm::View<reco::MET> >(iConfig.getParameter<edm::InputTag>("srcMet"));
    patmetToken_ = consumes<edm::View<pat::MET> >(iConfig.getParameter<edm::InputTag>("srcMet"));

    pfCandidatesToken_ = consumes<edm::View<reco::Candidate> >(iConfig.getParameter<edm::InputTag>("srcPFCandidates"));

    rhoToken_ = consumes<double>(iConfig.getParameter<edm::InputTag>("srcRho"));
    jetSFType_ = iConfig.getParameter<std::string>("srcJetSF");
    jetResPtType_ = iConfig.getParameter<std::string>("srcJetResPt");
    jetResPhiType_ = iConfig.getParameter<std::string>("srcJetResPhi");

    metSigAlgo_ = new metsig::METSignificance(iConfig);
    produces<pat::METCollection>();
}

void MiniAODMETSignificanceProducer::produce(edm::Event& event, const edm::EventSetup& setup)
{
  out = std::auto_ptr<std::vector<pat::MET> >(new std::vector<pat::MET>);

   //
   // met
   //
    edm::Handle<edm::View<reco::MET> > metHandle;
    event.getByToken(metToken_, metHandle);
    //const reco::MET& met = (*metHandle)[0];
    
    //
    // candidates
    //
    edm::Handle<reco::CandidateView> pfCandidates;
    event.getByToken( pfCandidatesToken_, pfCandidates );
    
    //
    // leptons
    //
   std::vector< edm::Handle<reco::CandidateView> > leptons;
   for ( std::vector<edm::EDGetTokenT<edm::View<reco::Candidate> > >::const_iterator srcLeptons_i = lepTokens_.begin();
         srcLeptons_i != lepTokens_.end(); ++srcLeptons_i ) {

      edm::Handle<reco::CandidateView> leptons_i;
      event.getByToken(*srcLeptons_i, leptons_i);
      leptons.push_back( leptons_i );

   }

   //
   // jets
   //
   edm::Handle<edm::View<reco::Jet> > jets;
   event.getByToken( pfjetsToken_, jets );
   

   //extra stuff for since 7_6_4
   edm::Handle<double> rho;
   event.getByToken(rhoToken_, rho);
 
   JME::JetResolution resPtObj = JME::JetResolution::get(setup, jetResPtType_);
   JME::JetResolution resPhiObj = JME::JetResolution::get(setup, jetResPhiType_);
   JME::JetResolutionScaleFactor resSFObj = JME::JetResolutionScaleFactor::get(setup, jetSFType_);

   //
   // compute the significance
   //
   const reco::METCovMatrix cov = metSigAlgo_->getCovariance( *jets, leptons, *pfCandidates,
							      *rho, resPtObj, resPhiObj, resSFObj, event.isRealData());

   edm::Handle<edm::View<pat::MET> > metIn;
   event.getByToken(patmetToken_, metIn);
   pat::MET metOut = (*metIn)[0];

   metOut.setSignificanceMatrix(cov);
   out->push_back(metOut);
   event.put(out);
  }

DEFINE_FWK_MODULE(MiniAODMETSignificanceProducer);

