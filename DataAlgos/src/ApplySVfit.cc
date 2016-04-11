///////////
// imp of function getSVfitMass
// based on standalone SVfit instructions
// https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2012#SVFit_Christian_Lorenzo_Aram_Rog
//
// S.Z. Shalhout (sshalhou@CERN.CH) Nov 20, 2012
/////////

#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "DataFormats/Provenance/interface/EventID.h"
#include "FinalStateAnalysis/DataAlgos/interface/ApplySVfit.h"

#include "TLorentzVector.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include "DataFormats/Math/interface/Vector3D.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "FinalStateAnalysis/DataAlgos/interface/Hash.h"
#include <iostream>
#include <iomanip>
#include <map>
#include <stdio.h>
#include <string>


namespace ApplySVfit {

  // Caching and translation layer
  typedef std::map<size_t, double> SVFitCache;
  static SVFitCache theCache;
  static edm::EventID lastSVfitEvent; // last processed event

  TLorentzVector getSVfitMass(std::vector<reco::CandidatePtr>& cands, std::vector<int>& decayModes,
                      const pat::MET& met, const ROOT::Math::SMatrix2D& covMET, unsigned int verbosity,
                      const edm::EventID& evtId) {

//     return -1.;

    // Check if this a new event
    if (evtId != lastSVfitEvent) {
      theCache.clear();
    }
    lastSVfitEvent = evtId;

// Hash our candidates - NB cands will be sorted in place
//     size_t hash = hashCandsByContent(cands);
// 
// Check if we've already computed it
//     SVFitCache::const_iterator lookup = theCache.find(hash);
//     if (lookup != theCache.end()) {
//       return lookup->second;
//     }
    // No pain no gain
    /*
    Vector measuredMET = met.momentum();
    std::vector<MeasuredTauLepton> measuredTauLeptons;

    bool hasHadronicTaus = false;
    
    for (size_t dau = 0; dau < cands.size(); ++dau) {
      int pdgId = std::abs(cands[dau]->pdgId());

      if (pdgId == 11){
        measuredTauLeptons.push_back(
            MeasuredTauLepton(svFitStandalone::kTauToElecDecay,cands[dau]->pt(),cands[dau]->eta(),cands[dau]->phi(), 0.51100e-3));
      }
      else if (pdgId == 13){
        measuredTauLeptons.push_back(
            MeasuredTauLepton(svFitStandalone::kTauToMuDecay,cands[dau]->pt(),cands[dau]->eta(),cands[dau]->phi(),0.10566));
      }
      else if (pdgId == 15){
        double tauMass = cands[dau]->mass();
        if(decayModes[dau] == 0) tauMass = 0.13957;
        measuredTauLeptons.push_back(
            MeasuredTauLepton(svFitStandalone::kTauToHadDecay,cands[dau]->pt(),cands[dau]->eta(),cands[dau]->phi(), tauMass, decayModes[dau]));
        if(decayModes[dau] != 5 and decayModes[dau] != 6) hasHadronicTaus = true;
      }
      else{
        throw cms::Exception("BadPdgId") << "I don't understand PDG id: "
          << pdgId << ", sorry." << std::endl;
      }
    }

    SVfitStandaloneAlgorithm algo(measuredTauLeptons, measuredMET.x(), measuredMET.y(), 
                                  convert_matrix(covMET), verbosity);
    algo.addLogM(false);
    edm::FileInPath inputFileName_visPtResolution("TauAnalysis/SVfitStandalone/data/svFitVisMassAndPtResolutionPDF.root");
    TH1::AddDirectory(false);  
    TFile* inputFile_visPtResolution = new TFile(inputFileName_visPtResolution.fullPath().data());
    algo.shiftVisPt(hasHadronicTaus, inputFile_visPtResolution);
    algo.integrateMarkovChain();
//     algo.integrateVEGAS();

    double mass = algo.getMass(); // mass uncertainty not implemented yet
    double pt = algo.pt();
    double eta = algo.eta();
    double phi = algo.phi();

    delete inputFile_visPtResolution;

     Thecache[hash] = mass;
    */
    TLorentzVector SVFit_results;
    //    SVFit_results.SetPtEtaPhiM(pt, eta, phi, mass);
    return SVFit_results;

  }

  TMatrixD convert_matrix(const ROOT::Math::SMatrix2D& mat)
  {
    const TMatrixD output = TMatrixD(mat.kRows, mat.kCols, mat.Array());
    return output;
  }

  TMatrixD convert_matrix(const TMatrixD& mat) 
  {
    return mat;
  }

} // namespace ApplySVfit
