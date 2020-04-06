#!/bin/bash

#set -x
## Identifying host
#pwd
#hostname
#ifconfig
#netstat -ntapl

cd ${CMSSW_BASE}/src/CMGTools/TTHAnalysis/python/plotter
eval `scramv1 runtime -sh`

DIR=$1
YEAR=$2
LEP=$3
REG=$4
BIN=$5
while ! [ -z "$6" ]; do
    if [ "$6" = "@" ]; then
        break;
    fi
    FLAGS="$FLAGS $6"; shift;
done
while ! [ -z "$7" ]; do
    EXTRAS="$EXTRAS $7"; shift;
done
COMMAND="$( python susy-sos/sos_plots.py $DIR $YEAR --lep $LEP --reg $REG --bin $BIN $FLAGS ) $EXTRAS"

echo "Region:"
echo $YEAR $LEP $REG $BIN
echo ""
echo "Command to run:"
echo $COMMAND

eval "$COMMAND"
