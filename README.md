FinalStateAnalysis Package Description (miniAOD_dev version)
============================================================

The Final State Analysis (FSA) package is a CMSSW analysis framework.  
The package contains a complete implementatation to build a POG-approved 
PAT tuple, and utilities for generating plain ROOT ntuples from the PAT tuple.

Installation
------------

Current CMSSW version: ``8_0_22``.

Get a supported CMSSW release area:

```bash
  cmsrel CMSSW_8_0_22
  cd CMSSW_8_0_22/src
  # Setup your CMSSW environment
  cmsenv
  # Run this before doing ANYTHING else in src
  git cms-init
  #type N
  git cms-merge-topic -u cms-met:fromCMSSW_8_0_20_postICHEPfilter
  git cms-merge-topic ikrav:egm_id_80X_v2
  scram b -j 8
  cd $CMSSW_BASE/external
  cd slc6_amd64_gcc530/
  git clone https://github.com/ikrav/RecoEgamma-ElectronIdentification.git data/RecoEgamma/ElectronIdentification/data
  cd data/RecoEgamma/ElectronIdentification/data
  git checkout egm_id_80X_v1
  cd $CMSSW_BASE/src
```

Checkout the FinalStateAnalysis repository:

```bash
  git clone -b miniAOD_8_0_20_FNAL https://github.com/zaixingmao/FSA.git FinalStateAnalysis
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