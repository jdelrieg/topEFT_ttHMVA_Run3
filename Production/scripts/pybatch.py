#!/bin/env python

import sys
import imp
import copy
import os
import shutil
import pickle
import math
from CMGTools.Production.batchmanager import BatchManager

def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]

def split(comps):
    # import pdb; pdb.set_trace()
    splitComps = []
    for comp in comps:
        if hasattr( comp, 'splitFactor') and comp.splitFactor>1:
            chunkSize = len(comp.files) / comp.splitFactor
            if len(comp.files) % comp.splitFactor:
                chunkSize += 1 
            # print 'chunk size',chunkSize, len(comp.files), comp.splitFactor 
            for ichunk, chunk in enumerate( chunks( comp.files, chunkSize)):
                newComp = copy.deepcopy(comp)
                newComp.files = chunk
                newComp.name = '{name}_Chunk{index}'.format(name=newComp.name,
                                                       index=ichunk)
                splitComps.append( newComp )
        else:
            splitComps.append( comp )
    return splitComps


def batchScriptCERN( jobDir, remoteDir=''):
   '''prepare the LSF version of the batch script, to run on LSF'''
   
   dirCopy = """echo 'sending the logs back'  # will send also root files if copy failed
cp -r Loop/* $LS_SUBCWD
if [ $? -ne 0 ]; then
   echo 'ERROR: problem copying job directory back'
else
   echo 'job directory copy succeeded'
fi"""
   if remoteDir=='':
      cpCmd=dirCopy
   elif remoteDir.startswith("/pnfs/psi.ch"):
       cpCmd="""echo 'sending root files to remote dir'
if [ looperExitStatus -ne 0 ]; then
   echo 'Looper failed. Don't attempt to copy corrupted file remotely'
else
   export LD_LIBRARY_PATH=/usr/lib64:$LD_LIBRARY_PATH # Fabio's workaround to fix gfal-tools with CMSSW
   for f in Loop/tree*/*.root
   do
      ff=`basename $f | cut -d . -f 1`
      d=`echo $f | cut -d / -f 2`
      gfal-mkdir {srm}
      echo "gfal-copy file://`pwd`/Loop/$d/$ff.root {srm}/${{ff}}_{idx}.root"
      gfal-copy file://`pwd`/Loop/$d/$ff.root {srm}/${{ff}}_{idx}.root
      if [ $? -ne 0 ]; then
         echo "ERROR: remote copy failed for file $ff"
      else
         echo "remote copy succeeded"
         rm Loop/$d/$ff.root
      fi
   done
fi
""".format(idx=jobDir[jobDir.find("_Chunk")+6:].strip("/"), srm='srm://t3se01.psi.ch'+remoteDir+jobDir[jobDir.rfind("/"):jobDir.find("_Chunk")]) + dirCopy
   elif remoteDir.startswith("/eos/cms/store"):
       cpCmd="""echo 'sending root files to remote dir'
if [ looperExitStatus -ne 0 ]; then
   echo 'Looper failed. Don't attempt to copy corrupted file remotely'
else
   for f in Loop/*ree*/*.root
   do
      ff=`basename $f | cut -d . -f 1`
      d=`echo $f | cut -d / -f 2`
      eos mkdir {srm}
      echo "cmsStage /`pwd`/Loop/$d/$ff.root {srm}/${{ff}}_{idx}.root"
      cmsStage /`pwd`/Loop/$d/$ff.root {srm}/${{ff}}_{idx}.root
      if [ $? -ne 0 ]; then
         echo "ERROR: remote copy failed for file $ff"
      else
         echo "remote copy succeeded"
         rm Loop/$d/$ff.root
      fi
   done
fi
""".format(idx=jobDir[jobDir.find("_Chunk")+6:].strip("/"), srm=(remoteDir+jobDir[jobDir.rfind("/"):jobDir.find("_Chunk")]).split("/eos/cms",1)[1]) + dirCopy
   else:
       print("choose location not supported yet: ", remoteDir)
       print('path must start with "/pnfs/psi.ch" or "/eos/cms/store"')
       sys.exit(1)

   script = """#!/bin/bash
#BSUB -q 8nm
echo 'environment:'
echo
env | sort
# ulimit -v 3000000 # NO
echo 'copying job dir to worker'
cd $CMSSW_BASE/src
eval `scramv1 ru -sh`
# cd $LS_SUBCWD
# eval `scramv1 ru -sh`
cd -
cp -rf $LS_SUBCWD .
ls
cd `find . -type d | grep /`
echo 'running'
python $CMSSW_BASE/src/CMGTools/RootTools/python/fwlite/Looper.py config.pck
looperExitStatus=$?
echo
{copy}
""".format(copy=cpCmd)

   return script


def batchScriptPSI( jobDir, remoteDir=''):
   '''prepare the SGE version of the batch script, to run on the PSI tier3 batch system'''

   cmssw_release = os.environ['CMSSW_BASE']
   VO_CMS_SW_DIR = "/swshare/cms"  # $VO_CMS_SW_DIR doesn't seem to work in the new SL6 t3wn


   dirCopy = """echo 'sending the logs back'  # will send also root files if copy failed
cp -r Loop/* $SUBMISIONDIR
if [ $? -ne 0 ]; then
   echo 'ERROR: problem copying job directory back'
else
   echo 'job directory copy succeeded'
fi"""
   if remoteDir=='':
       cpCmd=dirCopy
   elif remoteDir.startswith("/pnfs/psi.ch"):
       cpCmd="""echo 'sending root files to remote dir'
if [ looperExitStatus -ne 0 ]; then
   echo 'Looper failed. Don't attempt to copy corrupted file remotely'
else
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib64/dcap/ # Fabio's workaround to fix gfal-tools
   for f in Loop/tree*/*.root
   do
      ff=`basename $f | cut -d . -f 1`
      d=`echo $f | cut -d / -f 2`
      gfal-mkdir {srm}
      echo "gfal-copy file://`pwd`/Loop/$d/$ff.root {srm}/${{ff}}_{idx}.root"
      gfal-copy file://`pwd`/Loop/$d/$ff.root {srm}/${{ff}}_{idx}.root
      if [ $? -ne 0 ]; then
         echo "ERROR: remote copy failed for file $ff"
      else
         echo "remote copy succeeded"
         rm Loop/$d/$ff.root
      fi
   done
fi
""".format(idx=jobDir[jobDir.find("_Chunk")+6:].strip("/"), srm='srm://t3se01.psi.ch'+remoteDir+jobDir[jobDir.rfind("/"):jobDir.find("_Chunk")]) + dirCopy
   else:
       print("remote directory not supported yet: ", remoteDir)
       print('path must start with "/pnfs/psi.ch"')
       sys.exit(1)


   script = """#!/bin/bash
shopt expand_aliases
##### MONITORING/DEBUG INFORMATION ###############################
DATE_START=`date +%s`
echo "Job started at " `date`
cat <<EOF
################################################################
## QUEUEING SYSTEM SETTINGS:
HOME=$HOME
USER=$USER
JOB_ID=$JOB_ID
JOB_NAME=$JOB_NAME
HOSTNAME=$HOSTNAME
TASK_ID=$TASK_ID
QUEUE=$QUEUE

EOF
echo "######## Environment Variables ##########"
env | sort
echo "################################################################"
TOPWORKDIR=/scratch/`whoami`
JOBDIR=sgejob-$JOB_ID
WORKDIR=$TOPWORKDIR/$JOBDIR
SUBMISIONDIR={jdir}
if test -e "$WORKDIR"; then
   echo "ERROR: WORKDIR ($WORKDIR) already exists! Aborting..." >&2
   exit 1
fi
mkdir -p $WORKDIR
if test ! -d "$WORKDIR"; then
   echo "ERROR: Failed to create workdir ($WORKDIR)! Aborting..." >&2
   exit 1
fi

#source $VO_CMS_SW_DIR/cmsset_default.sh
source {vo}/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc481
#cd $CMSSW_BASE/src
cd {cmssw}/src
shopt -s expand_aliases
cmsenv
cd $WORKDIR
cp -rf $SUBMISIONDIR .
ls
cd `find . -type d | grep /`
echo 'running'
#python $CMSSW_BASE/src/CMGTools/RootTools/python/fwlite/Looper.py config.pck
python {cmssw}/src/CMGTools/RootTools/python/fwlite/Looper.py config.pck
looperExitStatus=$?
echo
{copy}
###########################################################################
DATE_END=`date +%s`
RUNTIME=$((DATE_END-DATE_START))
echo "################################################################"
echo "Job finished at " `date`
echo "Wallclock running time: $RUNTIME s"
exit 0
""".format(jdir=jobDir, vo=VO_CMS_SW_DIR,cmssw=cmssw_release, copy=cpCmd)

   return script


def batchScriptLocal(  remoteDir, index ):
   '''prepare a local version of the batch script, to run using nohup'''

   script = """#!/bin/bash
echo 'running'
python $CMSSW_BASE/src/CMGTools/RootTools/python/fwlite/Looper.py config.pck
echo
echo 'sending the job directory back'
mv Loop/* ./
""" 
   return script



class MyBatchManager( BatchManager ):
   '''Batch manager specific to cmsRun processes.''' 
         
   def PrepareJobUser(self, jobDir, value ):
       '''Prepare one job. This function is called by the base class.'''
       print(value)
       print(components[value])

       #prepare the batch script
       scriptFileName = jobDir+'/batchScript.sh'
       scriptFile = open(scriptFileName,'w')
       storeDir = self.remoteOutputDir_.replace('/castor/cern.ch/cms','')
       mode = self.RunningMode(options.batch)
       if mode == 'LXPLUS':
           scriptFile.write( batchScriptCERN (jobDir, storeDir) )
       elif mode == 'PSI':
           scriptFile.write( batchScriptPSI  (jobDir, storeDir) )
       elif mode == 'LOCAL':
           scriptFile.write( batchScriptLocal( storeDir, value) )  # watch out arguments are swapped (although not used)
       scriptFile.close()
       os.system('chmod +x %s' % scriptFileName)
       
       shutil.copyfile(cfgFileName, jobDir+'/pycfg.py')
       jobConfig = copy.deepcopy(config)
       jobConfig.components = [ components[value] ]
       cfgFile = open(jobDir+'/config.pck','w')
       pickle.dump( jobConfig, cfgFile )
       # pickle.dump( cfo, cfgFile )
       cfgFile.close()

      
if __name__ == '__main__':
    batchManager = MyBatchManager()
    batchManager.parser_.usage="""
    %prog [options] <cfgFile>

    Run Colin's python analysis system on the batch.
    Job splitting is determined by your configuration file.
    """

    options, args = batchManager.ParseOptions()

    cfgFileName = args[0]

    handle = open(cfgFileName, 'r')
    cfo = imp.load_source("pycfg", cfgFileName, handle)
    config = cfo.config
    handle.close()

    components = split( [comp for comp in config.components if len(comp.files)>0] )
    listOfValues = list(range(0, len(components)))
    listOfNames = [comp.name for comp in components]

    batchManager.PrepareJobs( listOfValues, listOfNames )
    waitingTime = 0.1
    batchManager.SubmitJobs( waitingTime )

