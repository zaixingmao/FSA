FSA Flat Ntuple Generation
==========================

The file ``make_ntuples_cfg.py`` generates TTrees for most final states of 
interest.  It can be tested in place by::

    cmsRun make_ntuples_cfg.py channels="em,mt" [options] inputFiles=file.root

There are some additional pre-defined groups of channels which are expanded
for your convenience::

    zh = eeem, eeet, eemt, eett, emmm, emmt, mmmt, mmtt,
    zz = eeee, eemm, mmmm,
    zgg = eegg, mmgg
    llt = emt, mmt, eet, mmm, emm
    zg = mmg,eeg
    zgxtra = mgg, emg, egg,


Ntuple Options
--------------

The available command line options (which are enabled/disabled by setting to
zero or one) are::

    skipEvents=0            - events to skip (for debugging)
    maxEvents=-1            - events to run on
    rerunMCMatch=0          - rerun MC matching
    eventView=0             - make a row in the ntuple correspond to an event
                              instead of a final state in an event.
    passThru=0              - turn off any preselection/skim
    verbose=0               - print out timing information
    noPhotons=0             - don't build things which depend on photons.
    isMC=0                  - run over monte carlo
    svFit=0                 - run secondary vertex stuff
    runMVAMET=0             - compute MVA MET (defaults to 1 if svFit is enabled)
    runDQM=0                - run on single objects instead of final states, plotting many quantities to make sure things work
    use25ns=1               - use conditions for 25ns PHYS14 miniAOD samples
    hzz=0                   - run the H->ZZ->4l group's FSR algorithm, don't clean
                              alternate Z pairings out of ntuples, several other small changes
    nExtraJets=0            - (for non-jet final states) add basic info about this many jets in addition to final state branches
    paramFile=''            - custom parameter file for ntuple production

Tests
----------------
```bash
  python test.py
  python diffROOTFiles.py --file1 testFile.root --file2 myTestFile.root
```
check diff.root file


Batch submission
----------------

Edit submit_TT.py
```bash
  python submit_TT.py
  source do.sh
```

