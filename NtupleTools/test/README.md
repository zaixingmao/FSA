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


Local Runs
----------
Edit the local file information in localJob_cfg.py

```bash
    python submit_FS.py --local --FS tt
```

Submit One Jobs
---------------

```bash
    python submit_FS.py --singleJob --FS tt -o test
    bash < do.sh

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