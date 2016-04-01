#!/usr/bin/env python
import os
import time



def writeCFGFile(dir):
    f = open('tmp_submit_cfg','w')
    f.write("universe = vanilla\n")
    if '\n' in dir:
        dir = dir[:dir.find('\n')]
    f.write("Executable = %s/submit\n" %dir)
    f.write('Requirements   =  OpSys == "LINUX" && (Arch =="INTEL" || Arch =="x86_64")\n')
    f.write("request_memory = 8000\n")
    f.write("Should_Transfer_Files = YES\n")
    f.write("WhenToTransferOutput = ON_EXIT\n")
    f.write("Transfer_Input_Files = %s.tar\n" %os.environ.get ('CMSSW_BASE'))
    f.write("Output = %s/condor.out\n" %dir)
    f.write("Error = %s/condor.err\n" %dir)
    f.write("Log = %s/condor.log\n" %dir)
    f.write("Notification = Never\n")
    f.write("Queue 1\n")





f_submit_jobs = open('submit_files.txt','r')
for line in f_submit_jobs.readlines():
    writeCFGFile(line)
    os.system("condor_submit tmp_submit_cfg")