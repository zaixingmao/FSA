FinalState Production
=====================

MINIAOD -> ntuple
-----------------
Read information from MINIAOD and store pairs of any combiniation of [e:electron, m:muon, t:tau]. 
For example, if an event had an electron and two muons while you requested to store em, there will 
be two entries in the final root file with the two possible electron-muon pairs.

Currently, the supported final states are: 
- et (electron-tau pair)
- mt (muon-tau pair)
- em (electron-muon pair)
- tt (tau-tau pair)


Branches
-----------------
Basic kinimatic variables of the leptons are stored as 'lepton name' + 'variable name'.
For example, the electron pt is stored as 'ePt' and the tau eta is stored as 'tEta'.
For the case of tau-tau pair, the pt leading tau takes the name 't1' and the pt trailing tau takes the name 't2'.


Configurations
-----------------
Specify the desired selections in submit_FS.py

Specify the desired json file in submit_FS.py for data

Add the sample you'd like to run over at MetaData/tuples/MiniAOD-13TeV_RunIIFall15.json or MetaData/tuples/MiniAOD-13TeV_Data.json.


submit_FS.py Options
-----------------
```bash

--local         #run interactively

--nJobs X       #when submitting condor jobs, specify the number of jobs to run. Used mainly for debugging.

-o XXX          #when submitting condor jobs, XXX specifies your desired directory name

--sample XXX    #when submitting condor jobs, specify the samples you'd like to run over. 
                #Defined in MetaData/tuples/MiniAOD-13TeV_RunIIFall15.json 
                #or MetaData/tuples/MiniAOD-13TeV_Data.json

--FS XX         #specify the desired final states to be saved. Currently supports et, mt, tt, em, ee, mm.

--isData        #please use if you're running over data samples

--atFNAL        #please use if you're running at FNAL

--resubmit      #when submitting condor jobs, resubmits failed jobs

--maxEvents     #when submitting condor jobs, specify the maximum number of events to run over. 
                #Used mainly for debugging.
```



Local Runs
----------
Edit the local file information in localJob_cfg.py

```bash
    python submit_FS.py --local --FS tt
```


Submit Jobs
---------------

```bash
    python submit_FS.py --FS tt -o test
    bash < do.sh
```

Submit Multiple Final States
----------------------------

```bash
    python submit_FS.py --FS tt,et,mt,em -o test
    bash < do.sh
```