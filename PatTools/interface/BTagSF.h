//#ifndef BtagSFV_hh
//#define BtagSFV_hh

#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "Math/GenVector/VectorUtil.h"
#include <TFormula.h>
#include "Utilities/General/interface/FileInPath.h"
#include "FinalStateAnalysis/PatTools/interface/BtagHardcodedConditions.h"
#include "FinalStateAnalysis/PatTools/interface/BTagSFUtil.h"
#include <math.h>

#include "TRandom3.h"
#include <iostream>

class BtagSFV
{
public:
  
  BtagSFV(const edm::ParameterSet& iConfig)
    {
      
    }

  
  ~BtagSFV() {
    std:: cout << "destructing b-scalefactor" <<std::endl;
  }
  
  enum { kNo, kDown, kUp };                     // systematic variations 

  Bool_t isbtagged(Float_t pt, Float_t eta, Float_t phi, Float_t csv, Int_t jetflavor, Bool_t isdata, UInt_t btagsys, UInt_t mistagsys, Float_t bTagWP)
  {
    bool btagged = false;
    std::string bTagOP = "CSVL";
    if(bTagWP > 0.7) bTagOP = "CSVM";
    if(csv>bTagWP) btagged = true;
    if(isdata || (btagsys == kNo && mistagsys == kNo)) return btagged;

    BTagSFUtil mBtagSfUtil;
    BtagHardcodedConditions mBtagCond;

    double _lightSf = mBtagCond.GetMistagScaleFactor(pt, eta, bTagOP);
    if(mistagsys == kDown) _lightSf -= mBtagCond.GetMistagSFUncertDown(pt, eta, bTagOP);
    if(mistagsys == kUp) _lightSf += mBtagCond.GetMistagSFUncertUp(pt, eta, bTagOP);
    double _lightEff = mBtagCond.GetMistagRate(pt, eta, bTagOP);

    double _btagSf = mBtagCond.GetBtagScaleFactor(pt, eta, bTagOP);
    if (btagsys == kUp){
        _btagSf += mBtagCond.GetBtagSFUncertUp(pt, eta, bTagOP);
        if(jetflavor == 4) _btagSf += mBtagCond.GetBtagSFUncertUp(pt, eta, bTagOP);
    }

    if (btagsys == kDown){
        _btagSf -= mBtagCond.GetBtagSFUncertUp(pt, eta, bTagOP);
        if(jetflavor == 4) _btagSf -= mBtagCond.GetBtagSFUncertDown(pt, eta, bTagOP);
    }
    double _btagEff = mBtagCond.GetBtagEfficiency(pt, eta, bTagOP);

    mBtagSfUtil.SetSeed(abs(static_cast<int>(sin(phi)*1e5)));

    mBtagSfUtil.modifyBTagsWithSF(btagged, jetflavor, _btagSf, _btagEff, _lightSf, _lightEff);

    return btagged;
  }


  //#endif
};
