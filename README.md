FinalStateAnalysis Package Description (miniAOD_dev version)
============================================================

The Final State Analysis (FSA) package is a CMSSW analysis framework.  
The package contains a complete implementatation to build a POG-approved 
PAT tuple, and utilities for generating plain ROOT ntuples from the PAT tuple.

**Documentation:** https://github.com/uwcms/FinalStateAnalysis/wiki


Installation
------------

Current CMSSW version: ``7_2_X``.

Get a supported CMSSW release area:

```bash
  cmsrel CMSSW_7_2_1
  cd CMSSW_7_2_1/src
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
  git clone -b test https://github.com/zaixingmao/FSA.git FinalStateAnalysis
  cd FinalStateAnalysis
```

Checkout the needed CMSSW tags:

```bash
  cd recipe/
  # Checkout needed packages and apply patches
  # This enables all options.  You can turn off things you don't need.
  PATPROD=1 LUMI=1 LIMITS=0 ./recipe.sh
  # Setup FSA environment
  source environment.sh
  # Compile
  cd ../../
  scram b -j 8
```

You must always set up the CMSSW environment + some extra variables from FinalStateAnalysis:

```bash
  cmsenv
  source $CMSSW_BASE/src/FinalStateAnalysis/environment.sh
```

To test setup
```bash
  cd FinalStateAnalysis/NtupleTools/test
  python test.py
  #compare your results with benchmark
  python diffROOTFiles.py --file1 myTestFile.root --file2 testFile.root
  #check diff.root file
```
