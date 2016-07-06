#include "FinalStateAnalysis/NtupleTools/interface/PATFinalStateAnalysis.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateFwd.h"
#include "FinalStateAnalysis/NtupleTools/interface/PATFinalStateSelection.h"
#include "FinalStateAnalysis/Utilities/interface/CutFlow.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateLS.h"

#include "FWCore/Common/interface/LuminosityBlockBase.h"
#include "CommonTools/Utils/interface/TFileDirectory.h"
#include "DataFormats/Common/interface/MergeableCounter.h"
#include "TH1F.h"
#include "TTree.h"

#include <sstream>

PATFinalStateAnalysis::PATFinalStateAnalysis(const edm::ParameterSet& pset, TFileDirectory& fs, edm::ConsumesCollector&& iC):
  BasicAnalyzer(pset, fs),fs_(fs) {
  src_ = pset.getParameter<edm::InputTag>("src");
  iC.consumes<PATFinalStateCollection>(src_);

  name_ = pset.getParameter<std::string>("@module_label");

  // Setup the code to apply event level weights
  std::vector<std::string> weights =
    pset.getParameter<std::vector<std::string> >("weights");
  for (size_t i = 0; i < weights.size(); ++i) {
    evtWeights_.push_back(EventFunction(weights[i]));
  }
  evtSrc_ = pset.getParameter<edm::InputTag>("evtSrc");
  iC.consumes<PATFinalStateEventCollection>(evtSrc_);

  analysisCfg_ = pset.getParameterSet("analysis");
  filter_ = pset.exists("filter") ? pset.getParameter<bool>("filter") : false;
  // Build the analyzer
  analysis_.reset(new PATFinalStateSelection(analysisCfg_, fs_));
  // Check if we want to make a sub analyzer for each run (use w/ caution!)
  splitRuns_ = pset.exists("splitRuns") ?
    pset.getParameter<bool>("splitRuns") : false;
  if (splitRuns_)
    runDir_.reset(new TFileDirectory(fs.mkdir("runs")));

  skimCounter_ = pset.getParameter<edm::InputTag>("skimCounter");
  iC.consumes<edm::MergeableCounter>(skimCounter_);

  lumiProducer_ = pset.exists("lumiProducer") ?
    pset.getParameter<edm::InputTag>("lumiProducer") :
    edm::InputTag("finalStateLS");
  iC.consumes<PATFinalStateLS>(lumiProducer_);

  generator_ = edm::InputTag("generator");
  iC.consumes<GenEventInfoProduct>(generator_);

  prunedGenParticles_ = edm::InputTag("prunedGenParticles");
  iC.consumes<reco::GenParticleCollection>(prunedGenParticles_);

  // Build the event counter histos.
  eventCounter_ = fs_.make<TH1F>("eventCount", "Events Processed", 1, -0.5, 0.5);
  eventCounterWeighted_ = fs_.make<TH1F>(
      "eventCountWeighted", "Events Processed (weighted)", 1, -0.5, 0.5);
  eventWeights_ = fs_.make<TH1F>(
      "eventWeights", "Events Weights", 100, 0, 5);
  eventCounterPtWeighted_ = fs_.make<TH1F>(
      "eventCountPtWeighted", "Events Processed (weighted)", 1, -0.5, 0.5);
  skimEventCounter_ = fs_.make<TH1F>(
      "skimCounter", "Original Events Processed", 1, -0.5, 0.5);
  integratedLumi_ = fs_.make<TH1F>(
      "intLumi", "Integrated Lumi", 1, -0.5, 0.5);
  metaTree_ = fs_.make<TTree>(
      "metaInfo", "Information about processed runs and lumis");
  for(int iPDF = 0; iPDF < 100; iPDF++){
    TString name = "eventCountWeightedPDF_" + std::to_string(iPDF);
    eventCounterWeightedPDFs_.push_back(fs_.make<TH1F>(name, " ", 1, -0.5, 0.5));
  }
  metaTree_->Branch("run", &treeRunBranch_, "run/I");
  metaTree_->Branch("lumi", &treeLumiBranch_, "lumi/I");
  metaTree_->Branch("nevents", &treeEventsProcessedBranch_, "nevents/I");
}

PATFinalStateAnalysis::~PATFinalStateAnalysis() { }

void PATFinalStateAnalysis::endLuminosityBlock(
    const edm::LuminosityBlockBase& ls) {
  //std::cout << "Analyzing lumisec: " << ls.id() << std::endl;

  edm::Handle<edm::MergeableCounter> skimmedEvents;
  ls.getByLabel(skimCounter_, skimmedEvents);
  skimEventCounter_->Fill(0.0, skimmedEvents->value);

  edm::Handle<PATFinalStateLS> lumiSummary;
  ls.getByLabel(lumiProducer_, lumiSummary);
  integratedLumi_->Fill(0.0, lumiSummary->intLumi());
  treeIntLumi_ = lumiSummary->intLumi();

  // Fill the meta info tree
  treeRunBranch_ = ls.run();
  treeLumiBranch_ = ls.luminosityBlock();
  treeEventsProcessedBranch_ = skimmedEvents->value;
  metaTree_->Fill();
}

bool PATFinalStateAnalysis::filter(const edm::EventBase& evt) {
  // Get the event weight
  double eventWeight = 1.0;
  double genEventWeight = 1.0;

  if (evtWeights_.size()) {
    edm::Handle<PATFinalStateEventCollection> event;
    evt.getByLabel(evtSrc_, event);
    for (size_t i = 0; i < evtWeights_.size(); ++i) {
      eventWeight *= evtWeights_[i]( (*event)[0] );
    }
  }
  //get gen event weight
  if (!evt.isRealData()){ 
    edm::Handle<GenEventInfoProduct> genEvt;
    evt.getByLabel(generator_,genEvt);

    // event weight
    genEventWeight = genEvt->weight();

    //get pdf weights                                                                                                                                                                                                  
    edm::Handle<PATFinalStateEventCollection> event;
    evt.getByLabel(evtSrc_, event);
    std::vector<double> pdf_weights = (*event)[0].getPDFWeight();
    std::vector<int> pdf_ids = (*event)[0].getPDFID();
    for(int i = 1; i < 101; i++){
      for(unsigned int j = 0; j < pdf_ids.size(); j ++){
	if(pdf_ids[j] == 2000+i) eventCounterWeightedPDFs_[i-1]->Fill(0.0, pdf_weights[j]*genEventWeight);
      }
    }

    //pt reweight                                                                                                                                                                                                      
    edm::Handle<reco::GenParticleCollection> genParticles;
    evt.getByLabel(prunedGenParticles_, genParticles);

    int nLeptons = 0;
    double topPt = 0, topBarPt = 0;
    double SF_Top = 1.0, SF_antiTop = 1.0;
    for(size_t i = 0; i < genParticles->size(); ++i) {
      const reco::GenParticle & p = (*genParticles)[i];
      int id = p.pdgId();
      double pt = p.pt();
      int n = p.numberOfDaughters();
      if(abs(id) == 24 && n == 2) {
	for (int j = 0; j < n; ++j) {
	  const reco::Candidate * dau = p.daughter(j);
	  if(abs(dau->pdgId()) == 11 or abs(dau->pdgId()) == 13) ++nLeptons;
	}
      }
      if(abs(id) == 6 && n == 2) {
	if(abs(p.daughter(0)->pdgId()) == 24 and abs(p.daughter(1)->pdgId()) == 5) {
	  if(id > 0) topPt = pt; else topBarPt = pt;
	}
      }
    }
    if(topPt > 400) topPt = 400;
    if(topBarPt > 400) topBarPt = 400;

    if ( nLeptons > 0 ) {
      if ( nLeptons == 1 ) {
        SF_Top = TMath::Exp(0.159+((-0.00141)*topPt));
        SF_antiTop = TMath::Exp(0.159+((-0.00141)*topBarPt));
      } else if ( nLeptons == 2 ) {
        SF_Top = TMath::Exp(0.148+((-0.00129)*topPt));
        SF_antiTop = TMath::Exp(0.148+((-0.00129)*topBarPt));
      }
    }
    eventCounterPtWeighted_->Fill(0.0, sqrt(SF_Top*SF_antiTop)*genEventWeight);
  }

  // Count this event
  eventCounter_->Fill(0.0);
  eventCounterWeighted_->Fill(0.0, genEventWeight);
  eventWeights_->Fill(eventWeight);

  // Get the final states to analyze
  edm::Handle<PATFinalStateCollection> finalStates;
  evt.getByLabel(src_, finalStates);

  std::vector<const PATFinalState*> finalStatePtrs;
  finalStatePtrs.reserve(finalStates->size());

  //Normal running
  bool mustCleanupFinalStates = false;
  for (size_t i = 0; i < finalStates->size(); ++i) {
    finalStatePtrs.push_back( &( (*finalStates)[i] ) );
  }

  // Hack workarounds into ntuple here
  //  bool mustCleanupFinalStates = true;
  //  do something

  // Check if we want to split by runs
  if (splitRuns_) {
    edm::RunNumber_t run = evt.id().run();
    // make a new folder for this run if necessary
    if (!runAnalysis_.count(run)) {
      std::stringstream ss; ss << run;
      TFileDirectory subdir = runDir_->mkdir(ss.str());
      boost::shared_ptr<PATFinalStateSelection> runSelection(
          new PATFinalStateSelection(analysisCfg_, subdir));
      runAnalysis_.insert(std::make_pair(run, runSelection));
    }
    // Analyze this event using the current run folder
    RunMap::iterator theSelectionIter = runAnalysis_.find(run);
    assert(theSelectionIter != runAnalysis_.end());
    PATFinalStateSelection* selection = theSelectionIter->second.get();
    assert(selection);
    (*selection)(finalStatePtrs, eventWeight);
  }

  bool result = (*analysis_)(finalStatePtrs, eventWeight);

  if (mustCleanupFinalStates) {
    for (size_t i = 0; i < finalStatePtrs.size(); ++i) {
      delete finalStatePtrs[i];
    }
  }

  return result;
}

void PATFinalStateAnalysis::analyze(const edm::EventBase& evt) {
  filter(evt);
}

void PATFinalStateAnalysis::endJob() {
  std::cout << "Cut flow for analyzer: " << name_ << std::endl;
  analysis_->cutFlow()->print(std::cout);
  std::cout << std::endl;
}
