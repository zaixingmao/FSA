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


Configurations (Optional)
-----------------
Specify the desired selections in submit_FS.py

Specify the desired global tag in make_ntuples_cfg.py

Specify the desired campaign tag in submit_FS.py for MC

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

--maxEvents X   #when submitting condor jobs, specify the maximum number of events to run over. 
                #Used mainly for debugging.
```



Local Runs
----------
Edit the local file information in localJob_cfg.py (Optional)

Example:
```bash
#Do:
    python submit_FS.py --local --FS tt --atFNAL
#Or:
    python submit_FS.py --local --FS tt,em,mt,et --atFNAL
```
3) The output file should be in your current directory with default name "myTestFile.root"


Submit Jobs
---------------
For MC samples, make sure the samples you plan to run over are defined in MetaData/tuples/MiniAOD-13TeV_RunIIFall15.json

For data samples, make sure the samples you plan to run over are defined in MetaData/tuples/MiniAOD-13TeV_Data.json

Example:
```bash
#Setup grid proxy: https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookStartingGrid#ObtainingCert
voms-proxy-init --voms=cms --valid=48:00

#Do:
    python submit_FS.py --FS tt,em,mt,et --atFNAL -o testProduction --sample ST*
    python submit_FNAL_condor.py
```
By default, this will submit condor jobs with the error and log files stored at: 
/uscms/home/${USERNAME}/nobackup/testProduction/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/

In the end, the final output root files will be transfered to:
/eos/uscms/store/user/${USERNAME}/testProduction/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/

If some jobs fail, one can resubmit the failed jobs automatically by:
```bash
#Do
    python submit_FS.py --FS tt,em,mt,et --atFNAL -o testProduction --sample ST* --resubmit
    python submit_FNAL_condor.py
```