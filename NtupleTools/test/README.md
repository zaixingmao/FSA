FinalState Production
=====================

submit_FS.py commands:
----------------------

  --local          run local jobs
  --doSVFit        do SVFit (currently not supported)
  --singleJob      submit 1 job
  -o NAME          name of output dir
  --sample=SAMPLE  sample name VBF, SUSY
  --memory         profile memory usage (igprof mp)
  --cpu            profile CPU usage (igprof pp)
  --FS=FS          final state: tt, et, mt, em


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
```

Submit Jobs
---------------

```bash
    python submit_FS.py --FS tt -o test
```

Submit Multiple Final States
----------------------------

```bash
    python submit_FS.py --FS tt,et,mt,em -o test
```