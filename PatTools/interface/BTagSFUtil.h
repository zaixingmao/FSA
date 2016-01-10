/*************************************************************
 
 Class Usage:
 
 This class should only be used for upgrading and downgrading
 if a single operating point is used in an analysis.
 
 bool isBTagged = b-tag flag for jet
 int pdgIdPart = parton id
 float Btag_SF = MC/data scale factor for b/c-tagging efficiency
 float Btag_eff = b/c-tagging efficiency in data
 float Bmistag_SF = MC/data scale factor for mistag efficiency
 float Bmistag_eff = mistag efficiency in data
 
 Author: Michael Segala
 Contact: michael.segala@gmail.com
 Updated: Ulrich Heintz 12/23/2011
 Updated: Gena Kukartsev 10/30/2012
 
 v 1.2
 
 *************************************************************/


#ifndef BTagSFUtil_lite_h
#define BTagSFUtil_lite_h

#include <Riostream.h>
#include "TRandom3.h"
#include "TMath.h"


class BTagSFUtil{
    
public:
    
    BTagSFUtil();
    BTagSFUtil(int seed);
    ~BTagSFUtil();
    
    void modifyBTagsWithSF( bool& isBTagged,
                           int pdgIdPart,
                           float Btag_SF = 0.98,
                           float Btag_eff = 1.0,
                           float Bmistag_SF = 1.0,
                           float Bmistag_eff = 1.0);
    
    void SetSeed( int seed );
    
    
private:
    
    bool applySF(bool& isBTagged, float Btag_SF = 0.98, float Btag_eff = 1.0);
    
    TRandom3 rand_;
    
};


#endif
