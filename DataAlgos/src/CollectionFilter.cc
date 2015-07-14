#include "FinalStateAnalysis/DataAlgos/interface/CollectionFilter.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

// Function cache
namespace {

typedef StringCutObjectSelector<reco::Candidate, true> CandFunc;
typedef std::map<std::string, CandFunc> CandFuncCache;
static CandFuncCache functions_;

const CandFunc& getFunction(const std::string& function) {
  CandFuncCache::iterator findFunc = functions_.find(function);
  // Build it if we haven't made it
  if (findFunc == functions_.end()) {
    functions_.insert(std::make_pair(function, CandFunc(function)));
    findFunc = functions_.find(function);
  }
  return findFunc->second;
}

}

// Get objects at least [minDeltaR] away from hardScatter objects
std::vector<const reco::Candidate*> getVetoObjects(
    const std::vector<const reco::Candidate*>& hardScatter,
    const std::vector<const reco::Candidate*>& vetoCollection,
    double minDeltaR,
    const std::string& filter) {
  std::vector<const reco::Candidate*> output;

  const CandFunc& filterFunc = getFunction(filter);

  for (size_t i = 0; i < vetoCollection.size(); ++i) {
    const reco::Candidate* ptr = vetoCollection[i];
    bool awayFromEverything = true;
    for (size_t j = 0; j < hardScatter.size(); ++j) {
      double deltaR = reco::deltaR(ptr->p4(), hardScatter[j]->p4());
      if (deltaR < minDeltaR) {
        awayFromEverything = false;
        break;
      }
    }
    if (awayFromEverything && (filterFunc)(*ptr)) {
      output.push_back(ptr);
    }
  }
  return output;
}

int getVetoDiObjects(
    const std::vector<const reco::Candidate*>& vetoCollection,
    double minDeltaR,
    const std::string& filter) {
    int nPairs = 0;
    const CandFunc& filterFunc = getFunction(filter);
    for (size_t i = 0; i < vetoCollection.size()-1; ++i) {
        const reco::Candidate* ptr_i = vetoCollection[i];
        for (size_t j = i; j < vetoCollection.size(); ++j) {
            const reco::Candidate* ptr_j = vetoCollection[j];
            double deltaR = reco::deltaR(ptr_i->p4(), ptr_j->p4());
            if (deltaR > minDeltaR) {
                if ((filterFunc)(*ptr_i) && (filterFunc)(*ptr_j) && (ptr_i->charge() == -ptr_j->charge())) nPairs++;
            }
        }
    }
    return nPairs;
}


// Get objects within [minDeltaR] from [object] passing [filter]
std::vector<const reco::Candidate*> getOverlapObjects(
    const reco::Candidate& candidate,
    const std::vector<const reco::Candidate*>& overlapCollection,
    double minDeltaR,
    const std::string& filter) {
  std::vector<const reco::Candidate*> output;

  const CandFunc& filterFunc = getFunction(filter);

  for (size_t i = 0; i < overlapCollection.size(); ++i) {
    const reco::Candidate* ptr = overlapCollection[i];
    double deltaR = reco::deltaR(ptr->p4(), candidate.p4());
    if (deltaR < minDeltaR) {
      if ((filterFunc)(*ptr)) {
        output.push_back(ptr);
      }
    }
  }
  return output;
}
