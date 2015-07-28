FinalStateAnalysis Package Description (miniAOD_dev version)
============================================================

The Final State Analysis (FSA) package is a CMSSW analysis framework.  
The package contains a complete implementatation to build a POG-approved 
PAT tuple, and utilities for generating plain ROOT ntuples from the PAT tuple.

**Documentation:** https://github.com/uwcms/FinalStateAnalysis/wiki


Installation
------------

Current CMSSW version: ``7_4_5``.

Get a supported CMSSW release area:

```bash
  cmsrel CMSSW_7_4_5
  cd CMSSW_7_4_5/src
  # Setup your CMSSW environment
  cmsenv
  # SSH agent is optional, but will save you from typing your password many times
  eval `ssh-agent -s`
  ssh-add
  # Run this before doing ANYTHING else in src
  git cms-init
```

Checkout the FinalStateAnalysis repository:

```bash
  git clone -b miniAOD_dev_74X https://github.com/zaixingmao/FSA.git FinalStateAnalysis
  cd FinalStateAnalysis
```

Checkout the needed CMSSW tags:

```bash
  cd recipe/
  # Checkout needed packages and apply patches
  # do >> HZZ=1 ./recipe.sh  instead if you want H->ZZ MELA stuff.
  ./recipe.sh
  cd ..
  # Setup FSA environment
  source environment.sh
  # Compile
  pushd ..
  scram b -j 8
  popd
```

Checkout METProducers to produce MEt CovMatrix
```bash
git cms-addpkg RecoMET/METProducers/
```

Checkout MVAMet (https://twiki.cern.ch/twiki/bin/view/CMS/MVAMet#CMSSW_7_2_X_requires_slc6_MiniAO)

```bash
git cms-addpkg RecoMET/METPUSubtraction/
cd RecoMET/METPUSubtraction/
git clone https://github.com/rfriese/RecoMET-METPUSubtraction data -b 72X-13TeV-Phys14_25_V4-26Mar15
cp ../../FinalStateAnalysis/recipe/PFMETAlgorithmMVA.cc src/PFMETAlgorithmMVA.cc
```


You must always set up the CMSSW environment + some extra variables from FinalStateAnalysis:

```bash
  cmsenv
  source $CMSSW_BASE/src/FinalStateAnalysis/environment.sh
```
