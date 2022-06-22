#!/bin/bash
export XRD_NETWORKSTACK=IPv4
cd $1
eval $(scramv1 runtime -sh); 
cd src/CMGTools/NanoProc/python/plotter
bash ${2} && touch ${2}.good
touch ${2}.done
