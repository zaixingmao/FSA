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
#include "CondFormats/BTauObjects/interface/BTagCalibration.h"
#include "CondTools/BTau/interface/BTagCalibrationReader.h"

#include "TRandom3.h"
#include <TFile.h>
#include <TH2D.h>


bool applySFL(double eta, bool& isBTagged, float Btag_SF, float Btag_eff){
    TRandom3 rand_;
    rand_ = TRandom3((int)((eta+5)*100000));
    bool newBTag = isBTagged;
    if (Btag_SF == 1) return newBTag; //no correction needed 
    //throw die
    double coin = rand_.Uniform();    
    //std::cout<<"Uniform coin: "<<coin<<std::endl;
    if(Btag_SF > 1){  // use this if SF>1
        if( !isBTagged ) {
            //fraction of jets that need to be upgraded
            float mistagPercent = (1.0 - Btag_SF) / (1.0 - (Btag_SF/Btag_eff) );
            //upgrade to tagged
            if( coin < mistagPercent ) {newBTag = true;}
        }
    }else{  // use this if SF<1
        //downgrade tagged to untagged
        if( isBTagged && coin > Btag_SF ) {newBTag = false;}
    }
    return newBTag;
}

class MiniAODJetBTagSFEmbedder : public edm::EDProducer {
  public:
    MiniAODJetBTagSFEmbedder(const edm::ParameterSet& pset);
    virtual ~MiniAODJetBTagSFEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);

  private:
    edm::InputTag src_;
    bool isData_;
    int isMC_;
    BTagCalibration *calib;
    BTagCalibrationReader *reader;
    BTagCalibrationReader *reader_c;
    BTagCalibrationReader *reader_light;
    TH2D *h2_Denom_b;
    TH2D *h2_Denom_c;
    TH2D *h2_Denom_udsg;
    TH2D *h2_Num_b;
    TH2D *h2_Num_c;
    TH2D *h2_Num_udsg;
};

MiniAODJetBTagSFEmbedder::MiniAODJetBTagSFEmbedder(const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  consumes<edm::View<pat::Jet>  >(src_);

  isMC_ = pset.getParameter<int>("isMC");
  if(isMC_) isData_ = false;
  else isData_ = true;
  produces<pat::JetCollection>();
  std::string base = std::getenv("CMSSW_BASE");
  std::string fEff =   "/src/FinalStateAnalysis/PatTools/data/TT_bEff_Loose.root";
  std::string path= base+fEff;

  TFile *f_EffMap = new TFile(path.c_str(),"READONLY");
  h2_Denom_b    = (TH2D*)f_EffMap->Get("bTaggingEffAnalyzer/h2_BTaggingEff_Denom_b");
  h2_Denom_c    = (TH2D*)f_EffMap->Get("bTaggingEffAnalyzer/h2_BTaggingEff_Denom_c");
  h2_Denom_udsg    = (TH2D*)f_EffMap->Get("bTaggingEffAnalyzer/h2_BTaggingEff_Denom_udsg");
  h2_Num_b    = (TH2D*)f_EffMap->Get("bTaggingEffAnalyzer/h2_BTaggingEff_Num_b");
  h2_Num_c    = (TH2D*)f_EffMap->Get("bTaggingEffAnalyzer/h2_BTaggingEff_Num_c");
  h2_Num_udsg    = (TH2D*)f_EffMap->Get("bTaggingEffAnalyzer/h2_BTaggingEff_Num_udsg");

  calib=new BTagCalibration("CSVv2", base+"/src/FinalStateAnalysis/PatTools/data/CSVv2_ichep.csv");

  reader = new BTagCalibrationReader(BTagEntry::OP_LOOSE, "central", {"up", "down"});
  reader_c = new BTagCalibrationReader(BTagEntry::OP_LOOSE, "central", {"up", "down"});
  reader_light = new BTagCalibrationReader(BTagEntry::OP_LOOSE, "central", {"up", "down"});

  reader->load(*calib, BTagEntry::FLAV_B, "comb");
  reader_c->load(*calib, BTagEntry::FLAV_C, "comb");
  reader_light->load(*calib, BTagEntry::FLAV_UDSG, "incl");

}

void MiniAODJetBTagSFEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::auto_ptr<pat::JetCollection> output(new pat::JetCollection);

  edm::Handle<edm::View<pat::Jet> > input;
  evt.getByLabel(src_, input);

  output->reserve(input->size());

  for (size_t i = 0; i < input->size(); ++i) {
    pat::Jet jet = input->at(i);
    double j_SF = 1.0;
    double j_SF_up = 1.0;
    double j_SF_down = 1.0;
    double bTagEff = 0.0;
    double num = 1.0;
    double denom = 1.0;
    bool bTag = false;
    if (jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")>0.460) bTag =true;
    double jetPt = jet.pt();
    double jetEta = jet.eta();
    if(jetPt > 30 && fabs(jetEta)<2.4 && isMC_){
        if(jetPt >= 670) jetPt = 665.0;
        if (fabs(jet.partonFlavour()) == 5) {//b-jet
            j_SF  = reader->eval_auto_bounds("central", BTagEntry::FLAV_B, jetEta, jetPt); 
            j_SF_up  = reader->eval_auto_bounds("up", BTagEntry::FLAV_B, jetEta, jetPt); 
            j_SF_down  = reader->eval_auto_bounds("down", BTagEntry::FLAV_B, jetEta, jetPt);
            num = h2_Num_b->GetBinContent( h2_Num_b->GetXaxis()->FindBin(jetPt), h2_Num_b->GetYaxis()->FindBin(jetEta) );
            denom = h2_Denom_b->GetBinContent( h2_Denom_b->GetXaxis()->FindBin(jetPt), h2_Denom_b->GetYaxis()->FindBin(jetEta) );
        }
        else if (fabs(jet.partonFlavour()) == 4){//c-jet
            j_SF  = reader_c->eval_auto_bounds("central", BTagEntry::FLAV_C, jetEta, jetPt); 
            j_SF_up  = reader_c->eval_auto_bounds("up", BTagEntry::FLAV_C, jetEta, jetPt); 
            j_SF_down  = reader_c->eval_auto_bounds("down", BTagEntry::FLAV_C, jetEta, jetPt);
            num = h2_Num_c->GetBinContent( h2_Num_c->GetXaxis()->FindBin(jetPt), h2_Num_c->GetYaxis()->FindBin(jetEta) );
            denom = h2_Denom_c->GetBinContent( h2_Denom_c->GetXaxis()->FindBin(jetPt), h2_Denom_c->GetYaxis()->FindBin(jetEta) );
        }
        else{//light-jet
            j_SF  = reader_light->eval_auto_bounds("central", BTagEntry::FLAV_UDSG, jetEta, jetPt); 
            j_SF_up  = reader_light->eval_auto_bounds("up", BTagEntry::FLAV_UDSG, jetEta, jetPt); 
            j_SF_down  = reader_light->eval_auto_bounds("down", BTagEntry::FLAV_UDSG, jetEta, jetPt); 
            num = h2_Num_udsg->GetBinContent( h2_Num_udsg->GetXaxis()->FindBin(jetPt), h2_Num_udsg->GetYaxis()->FindBin(jetEta) );
            denom = h2_Denom_udsg->GetBinContent( h2_Denom_udsg->GetXaxis()->FindBin(jetPt), h2_Denom_udsg->GetYaxis()->FindBin(jetEta) );
        }
     }

    bool btagged =  bTag;
    bool btaggedup =  bTag;
    bool btaggeddown =  bTag;

    if(num!=0 && denom!=0){
        btagged = applySFL(jetEta, bTag, j_SF, num/denom);
        btaggedup = applySFL(jetEta, bTag, j_SF_up, num/denom);
        btaggeddown = applySFL(jetEta, bTag, j_SF_down, num/denom);
        bTagEff = num/denom;
    }

    jet.addUserFloat("CSVL", float(bTag));
    jet.addUserFloat("CSVL_withSF", float(btagged));
    jet.addUserFloat("CSVL_withSF_up", float(btaggedup));
    jet.addUserFloat("CSVL_withSF_down", float(btaggeddown));

    jet.addUserFloat("bTagEff", float(bTagEff));
    jet.addUserFloat("bTagSF", float(j_SF));
    jet.addUserFloat("bTagSF_up", float(j_SF_up));
    jet.addUserFloat("bTagSF_down", float(j_SF_down));
    output->push_back(jet);
  }

  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODJetBTagSFEmbedder);
