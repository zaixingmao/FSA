FinalStateAnalysis Package Description (miniAOD_dev version)
============================================================

The Final State Analysis (FSA) package is a CMSSW analysis framework.  
The package contains a complete implementatation to build a POG-approved 
PAT tuple, and utilities for generating plain ROOT ntuples from the PAT tuple.

Installation
------------

Current CMSSW version: ``8_0_12``.

Get a supported CMSSW release area:

```bash
  cmsrel CMSSW_8_0_12
  cd CMSSW_8_0_12/src
  # Setup your CMSSW environment
  cmsenv
  # Run this before doing ANYTHING else in src
  git cms-init
  #type N
  git cms-merge-topic -u cms-met:CMSSW_8_0_X-METFilterUpdate
```

Checkout the FinalStateAnalysis repository:

```bash
  git clone -b miniAOD_8_0_12_FNAL https://github.com/zaixingmao/FSA.git FinalStateAnalysis
  cd FinalStateAnalysis
  cd recipe/
  ./recipe.sh
  source environment.sh
cd ../..
```


Checkout MVAMET stuff:

```bash
git cms-addpkg RecoMET/METProducers/
git cms-addpkg RecoMET/METPUSubtraction/
git cms-addpkg RecoMET/METFilters/
```


Build:

```bash
export USER_CXXFLAGS=" -Wno-delete-non-virtual-dtor"
scram b -j 8
```


Running:

```bash
cd NtupleTools/test/
#Read documentation at https://github.com/zaixingmao/FSA/tree/miniAOD_8_0_12_FNAL/NtupleTools/test
```