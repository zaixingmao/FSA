FinalStateAnalysis Package Description (miniAOD_dev version)
============================================================

The Final State Analysis (FSA) package is a CMSSW analysis framework.  
The package contains a complete implementatation to build a POG-approved 
PAT tuple, and utilities for generating plain ROOT ntuples from the PAT tuple.

**Documentation:** https://github.com/uwcms/FinalStateAnalysis/wiki


Installation
------------

Current CMSSW version: ``7_4_14``.

Get a supported CMSSW release area:

```bash
  cmsrel CMSSW_7_4_14
  cd CMSSW_7_4_14/src
  # Setup your CMSSW environment
  cmsenv
```

Checkout the FinalStateAnalysis repository:

```bash
  git clone -b miniAOD_dev_7_4_14 https://github.com/zaixingmao/FSA.git FinalStateAnalysis
  cd FinalStateAnalysis
  cd recipe/
  ./recipe.sh
  source environment.sh
cd ../..
```


Checkout SVFit, MVAMET stuff:

```bash
git clone https://github.com/veelken/SVfit_standalone.git TauAnalysis/SVfitStandalone
git cms-addpkg RecoMET/METProducers/
git cms-addpkg RecoMET/METPUSubtraction/
```

New ElectronID:
```bash
git cms-merge-topic ikrav:egm_id_7.4.12_v1
```


Build:

```bash
export USER_CXXFLAGS=" -Wno-delete-non-virtual-dtor -Wno-error=unused-but-set-variable -Wno-error=unused-variable -Wno-error=sign-compare -Wno-error=reorder"
scram b -j 8
```