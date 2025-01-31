#!/usr/bin/env python

import os
import pprint
import re
import pickle
import sys
import json

from CMGTools.Production.castorBaseDir import castorBaseDir
import CMGTools.Production.eostools as castortools
import fnmatch

class IntegrityCheckError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def _dasPopen(dbs, verbose=True):
    if 'LSB_JOBID' in os.environ:
        raise RuntimeError("Trying to do a DAS query while in a LXBatch job (env variable LSB_JOBID defined)\nquery was: %s" % dbs)
    #--- this below fails also locally, so it's off for the moment; to be improved ---
    #if 'GLOBUS_GRAM_JOB_CONTACT':
    #    raise RuntimeError, "Trying to do a DAS query while in a Grid job (env variable GLOBUS_GRAM_JOB_CONTACT defined)\nquery was: %s" % dbs
    if verbose: print('dbs\t: %s' % dbs)
    return os.popen(dbs)

class BaseDataset( object ):
    
    ### def __init__(self, name, user, pattern='.*root', run_range=None):
    def __init__(self, name, user, pattern='.*root', run_range=None, dbsInstance=None, json=None):
        self.name = name
        self.user = user
        self.pattern = pattern
        self.run_range = run_range
        self.json = json
        ### MM
        self.dbsInstance = dbsInstance
        ### MM
        self.primaryDatasetEntries = -1
        self.report = None
        self.buildListOfFiles( self.pattern )
        self.extractFileSizes()
        self.buildListOfBadFiles()
        self.primaryDatasetEntries = self.getPrimaryDatasetEntries()
     
    def buildListOfFiles( self, pattern ):
        self.files = []

    def extractFileSizes(self):
        '''Get the file size for each file, 
        from the eos ls -l command.'''
        self.filesAndSizes = {}

    def buildListOfBadFiles(self):
        self.good_files = []
        self.bad_files = {}

    def printInfo(self):
        print('sample      :  ' + self.name)
        print('user        :  ' + self.user)

    def getPrimaryDatasetEntries(self):
        return self.primaryDatasetEntries

    def printFiles(self, abspath=True, info=True):
        # import pdb; pdb.set_trace()
        if self.files == None:
            self.buildListOfFiles(self.pattern)
        for file in self.files:
            status = 'OK'
            if file in self.bad_files:
                status = self.bad_files[file]
            elif file not in self.good_files:
                status = 'UNKNOWN'
            fileNameToPrint = file
            if abspath == False:
                fileNameToPrint = os.path.basename(file)
            if info:
                size=self.filesAndSizes.get(file,'UNKNOWN').rjust(10)
                # if size is not None:
                #     size = size.rjust(10)
                print(status.ljust(10), size, \
                      '\t', fileNameToPrint)
            else:
                print(fileNameToPrint)
        print('PrimaryDatasetEntries: %d' % self.primaryDatasetEntries)
                
    def listOfFiles(self):
        '''Returns all files, even the bad ones.'''
        return self.files

    def listOfGoodFiles(self):
        '''Returns all files flagged as good in the integrity 
        check text output, or not present in this file, are 
        considered as good.'''
        self.good_files = []
        for file in self.files:            
            if file not in self.bad_files:
                self.good_files.append( file )
        return self.good_files

    def listOfGoodFilesWithPrescale(self, prescale):
        """Takes the list of good files and selects a random sample 
        from them according to the prescale factor. 
        E.g. a prescale of 10 will select 1 in 10 files."""

        good_files = self.listOfGoodFiles()
        if prescale < 2:
            return self.good_files
        
        #the number of files to select from the dataset
        num_files = int( (len(good_files)/(1.0*prescale)) + 0.5)
        if num_files < 1:
            num_files = 1
        if num_files > len(good_files):
            num_files = len(good_files)
        
        #pick unique good files randomly
        import random
        subset = set()
        while len(subset) < num_files:
            #pick a random file from the list
            choice = random.choice(good_files)
            slen = len(subset)
            #add to the set
            subset.add(choice)
            #if this was a unique file remove so we don't get 
            #very slow corner cases where prescale is small
            if len(subset) > slen:
                good_files.remove(choice)
        assert len(subset)==num_files,'The number of files does not match'

        return [f for f in subset]

class CMSDataset( BaseDataset ):

    def __init__(self, name, run_range = None, json = None, unsafe=False, user='CMS', dbsInstance=None):
        self.unsafe = unsafe
        super(CMSDataset, self).__init__( name, user, run_range=run_range, json=json, dbsInstance=dbsInstance)

    def buildListOfFilesDBS(self, pattern, begin=-1, end=-1, run_range="self"):
        #print 'buildListOfFilesDBS',begin,end
        sampleName = self.name.rstrip('/')
        query, qwhat = sampleName, "dataset"
        if "#" in sampleName: qwhat = "block"
        if run_range == "self": run_range = self.run_range
        if run_range is not None and run_range != (-1,-1):
            if run_range[0] == run_range[1]:
                query += "   run=%s" % run_range[0]
            else:
                print("WARNING: queries with run ranges are slow in DAS")
                query += "   run between [%s,%s]" % ( run_range[0],run_range[1] )
        else:
            query += "  status=VALID" # status doesn't interact well with run range
        if self.dbsInstance != None:
            query += "  instance=prod/%s" % self.dbsInstance
        dbs='dasgoclient --json --query="file %s=%s"'%(qwhat,query) # files must be valid
        if begin >= 0:
            dbs += ' --index %d' % begin
        if end >= 0:
            dbs += ' --limit %d' % (end-begin+1)
        else:
            dbs += ' --limit 0'
        dbsOut = json.load(_dasPopen(dbs))
        files = []
        if dbsOut:
            for dbsEntry in dbsOut:
                if 'file' not in dbsEntry:
                    continue
                dbsFiles = dbsEntry['file']
                for fileDict in dbsFiles:
                    if 'name' not in fileDict:
                        continue
                    files.append(fileDict['name'])
        if not files:
            raise RuntimeError("No files for query \'%s\'" % query)
        return files

    def buildListOfFiles(self, pattern='.*root'):
        runs = (-1,-1)
        if self.run_range is not None:
            runs = self.run_range
        if not hasattr(self,'summaries'):
            self.summaries = self.findPrimaryDatasetSummaries(self.name.rstrip('/'),
                                                  runs[0],runs[1])
        num_files = self.summaries['files']
        if num_files == -1:
            raise RuntimeError("Error querying DAS for dataset %r" % self.name.rstrip('/'))
        
        limit = 10000
        if num_files > limit:
            if self.json is not None:
                print("WARNING: the json file will be ignored for this data set. (to be implemented)")

            num_steps = int(num_files/limit)+1
            self.files = []
            for i in range(num_steps):
                DBSFiles=self.buildListOfFilesDBS(pattern,
                                                  i*limit,
                                                  ((i+1)*limit)-1)
                self.files.extend(DBSFiles)
            if len(self.files) != num_files:
                raise RuntimeError("ERROR: mismatching number of files between dataset summary (%d) and dataset query for files(%d)\n" % (num_files, len(self.files)))
            return

        if self.json is not None:
            import json
            j = json.load(open(os.path.expandvars(self.json)))
            certified_runs = [int(r) for r in sorted(j.keys())]
            if self.run_range is not None:
                certified_runs = [r for r in certified_runs if self.run_range[0] <= r <= self.run_range[1]]
            run_range_list = [ ]
            run_range = None
            for run in certified_runs:
                if run_range is None:
                    run_range = [run, run]
                elif run == run_range[1] + 1:
                    run_range[1] = run
                else:
                    run_range_list.append(run_range)
                    run_range = [run, run]
            else:
                if run_range is not None:
                    run_range_list.append(run_range)

            self.files = []
            for run_range in run_range_list:
                DBSFiles = self.buildListOfFilesDBS(pattern, run_range=run_range)
                DBSFiles = [f for f in DBSFiles if f not in self.files]
                self.files.extend(DBSFiles)

            return

        self.files = self.buildListOfFilesDBS(pattern)
        if len(self.files) != num_files and not self.unsafe:
            raise RuntimeError("ERROR: mismatching number of files between dataset summary (%d) and dataset query for files(%d)\n" % (num_files, len(self.files)))
            
    @staticmethod
    def findPrimaryDatasetSummaries(dataset, runmin, runmax, dbsInstance=None):

        query, qwhat = dataset, "dataset"
        if "#" in dataset: qwhat = "block"
        if runmin >0 or runmax > 0:
            if runmin == runmax:
                query = "%s run=%d" % (query,runmin)
            else:
                print("WARNING: queries with run ranges are slow in DAS")
                query = "%s run between [%d, %d]" % (query,runmin if runmin > 0 else 1, runmax if runmax > 0 else 999999)
        if dbsInstance != None:
            query += "  instance=prod/%s" % dbsInstance
        dbs='dasgoclient --query="summary %s=%s" --format=json'%(qwhat,query)
        try:
            jdata = json.load(_dasPopen(dbs))['data']
        except ValueError as err:
            err=['cannot decode json obtained from das']
            err.append(_dasPopen(dbs).read())
            raise ValueError('\n'.join(err))
        events = []
        files = []
        lumis = []
        for line in jdata:
            data = line['summary'][0]
            events.append(int(data["nevents"]))
            files.append(int(data["nfiles"]))
            lumis.append(int(data["nlumis"]))
        if not events: events = [-1]
        if not files:  files  = [-1]
        if not lumis:  lumis  = [-1]
        return { 'files':sum(files), 'events':sum(events), 'lumis':sum(lumis) }


    @staticmethod
    def findPrimaryDatasetEntries(dataset, runmin, runmax, dbsInstance=None):
        return self.findPrimaryDatasetSummaries(dataset, runmin, runmax, dbsInstance=dbsInstance)['events']

    @staticmethod
    def findPrimaryDatasetNumFiles(dataset, runmin, runmax, dbsInstance=None):
        return self.findPrimaryDatasetSummaries(dataset, runmin, runmax, dbsInstance=dbsInstance)['files']

    def getPrimaryDatasetEntries(self):
        runmin = -1
        runmax = -1
        if self.run_range is not None:
            runmin = self.run_range[0]
            runmax = self.run_range[1]
        if not hasattr(self,'summaries'):
            self.summaries = self.findPrimaryDatasetSummaries(self.name, runmin, runmax, dbsInstance = self.dbsInstance)
        return self.summaries['events']

class LocalDataset( BaseDataset ):

    def __init__(self, name, basedir, pattern):
        self.basedir = basedir 
        super(LocalDataset, self).__init__( name, 'LOCAL', pattern)
        
    def buildListOfFiles(self, pattern='.*root'):
        pat = re.compile( pattern )
        sampleName = self.name.rstrip('/')
        sampleDir = ''.join( [os.path.abspath(self.basedir), 
                              sampleName ] )
        self.files = []
        for file in sorted(os.listdir( sampleDir )):
            if pat.match( file ) is not None:
                self.files.append( '/'.join([sampleDir, file]) )
                # print file
##         dbs = 'dbs search --query="find file where dataset like %s"' % sampleName
##         dbsOut = _dasPopen(dbs)
##         self.files = []
##         for line in dbsOut:
##             if line.find('/store')==-1:
##                 continue
##             line = line.rstrip()
##             # print 'line',line
##             self.files.append(line)

class Dataset( BaseDataset ):
    
    def __init__(self, name, user, pattern='.*root'):
        self.lfnDir = castorBaseDir(user) + name
        self.castorDir = castortools.lfnToCastor( self.lfnDir )
        self.maskExists = False
        self.report = None
        super(Dataset, self).__init__(name, user, pattern)
        #        self.buildListOfFiles( pattern )
        #        self.extractFileSizes()
        #        self.maskExists = False
        #        self.report = None
        #        self.buildListOfBadFiles()
        
    def buildListOfFiles(self, pattern='.*root'):
        '''fills list of files, taking all root files matching the pattern in the castor dir'''
        self.files = castortools.matchingFiles( self.castorDir, pattern )
                             
    def buildListOfBadFiles(self):
        '''fills the list of bad files from the IntegrityCheck log.

        When the integrity check file is not available,
        files are considered as good.'''
        mask = "IntegrityCheck"
           
        self.bad_files = {}
        self.good_files = []

        file_mask = castortools.matchingFiles(self.castorDir, '^%s_.*\.txt$' % mask)
        if file_mask:
            from CMGTools.Production.edmIntegrityCheck import PublishToFileSystem
            p = PublishToFileSystem(mask)
            report = p.get(self.castorDir)
            if report is not None and report:
                self.maskExists = True
                self.report = report
                dup = report.get('ValidDuplicates',{})
                for name, status in report['Files'].items():
                    # print name, status
                    if not status[0]:
                        self.bad_files[name] = 'MarkedBad'
                    elif name in dup:
                        self.bad_files[name] = 'ValidDup'
                    else:
                        self.good_files.append( name )
        else:
            raise IntegrityCheckError( "ERROR: IntegrityCheck log file IntegrityCheck_XXXXXXXXXX.txt not found" )

    def extractFileSizes(self):
        '''Get the file size for each file, from the eos ls -l command.'''
        #lsout = castortools.runEOSCommand(self.castorDir, 'ls','-l')[0]
        #lsout = lsout.split('\n')
        #self.filesAndSizes = {}
        #for entry in lsout:
        #    values = entry.split()
        #    if( len(values) != 9):
        #        continue
        #    # using full abs path as a key.
        #    file = '/'.join([self.lfnDir, values[8]])
        #    size = values[4]
        #    self.filesAndSizes[file] = size 
        # EOS command does not work in tier3
        lsout = castortools.runXRDCommand(self.castorDir,'dirlist')[0]
        lsout = lsout.split('\n')
        self.filesAndSizes = {}
        for entry in lsout:
            values = entry.split()
            if( len(values) != 5):
                continue
            # using full abs path as a key.
            file = '/'.join([self.lfnDir, values[4].split("/")[-1]])
            size = values[1]
            self.filesAndSizes[file] = size 
         
    def printInfo(self):
        print('sample      :  ' + self.name)
        print('LFN         :  ' + self.lfnDir)
        print('Castor path :  ' + self.castorDir)

    def getPrimaryDatasetEntries(self):
        if self.report is not None and self.report:
            return int(self.report.get('PrimaryDatasetEntries',-1))
        return -1


### MM
class PrivateDataset ( BaseDataset ):

    def __init__(self, name, dbsInstance=None):
        super(PrivateDataset, self).__init__(name, 'PRIVATE', dbsInstance=dbsInstance)

    def buildListOfFilesDBS(self, name, dbsInstance):
        entries = self.findPrimaryDatasetNumFiles(name, dbsInstance, -1, -1)
        files = []
        dbs = 'dasgoclient --json --query="file dataset=%s instance=prod/%s" --limit=%s' % (name, dbsInstance, entries)
        dbsOut = json.load(_dasPopen(dbs))
        if dbsOut:
            for dbsEntry in dbsOut:
                if 'file' not in dbsEntry:
                    continue
                dbsFiles = dbsEntry['file']
                for fileDict in dbsFiles:
                    if 'name' not in fileDict:
                        continue
                    files.append(fileDict['name'])
        if not files:
            raise RuntimeError("Dataset %s is empty!" % name)
        return files

    def buildListOfFiles(self, pattern='.*root'):
        self.files = self.buildListOfFilesDBS(self.name, self.dbsInstance)


    @staticmethod
    def findPrimaryDatasetEntries(dataset, dbsInstance, runmin, runmax):

        query, qwhat = dataset, "dataset"
        if "#" in dataset: qwhat = "block"
        if runmin >0 or runmax > 0:
            if runmin == runmax:
                query = "%s run=%d" % (query,runmin)
            else:
                print("WARNING: queries with run ranges are slow in DAS")
                query = "%s run between [%d, %d]" % (query,runmin if runmin > 0 else 1, runmax if runmax > 0 else 999999)
        dbs='dasgoclient --json --query="summary %s=%s instance=prod/%s"'%(qwhat, query, dbsInstance)
        dbsOut = json.load(_dasPopen(dbs))
        entries = []
        if dbsOut:
            dbsSummary = dbsOut[0]['summary']
            for summaryDict in dbsSummary:
                if "nevents" in summaryDict:
                    entries.append(int(summaryDict["nevents"]))
        if entries:
            return sum(entries)
        return -1


    @staticmethod
    def findPrimaryDatasetNumFiles(dataset, dbsInstance, runmin, runmax):

        query, qwhat = dataset, "dataset"
        if "#" in dataset: qwhat = "block"
        if runmin >0 or runmax > 0:
            if runmin == runmax:
                query = "%s run=%d" % (query,runmin)
            else:
                print("WARNING: queries with run ranges are slow in DAS")
                query = "%s run between [%d, %d]" % (query,runmin if runmin > 0 else 1, runmax if runmax > 0 else 999999)
        dbs='dasgoclient --json --query="summary %s=%s instance=prod/%s"'%(qwhat, query, dbsInstance)
        dbsOut = json.load(_dasPopen(dbs))[0]['summary']
        entries = []
        for summaryDict in dbsOut:
            if "nfiles" in summaryDict:
                entries.append(int(summaryDict["nfiles"]))
        if entries:
            return sum(entries)
        return -1

    def getPrimaryDatasetEntries(self):
        runmin = -1
        runmax = -1
        if self.run_range is not None:
            runmin = self.run_range[0]
            runmax = self.run_range[1]
        return self.findPrimaryDatasetEntries(self.name, self.dbsInstance, runmin, runmax)
### MM

def getDatasetFromCache( cachename ) :
    cachedir =  '/'.join( [os.environ['HOME'],'.cmgdataset'])
    pckfile = open( cachedir + "/" + cachename, 'rb' )
    dataset = pickle.load(pckfile)      
    return dataset

def writeDatasetToCache( cachename, dataset ):
    cachedir =  '/'.join( [os.environ['HOME'],'.cmgdataset'])
    if not os.path.exists(cachedir):
        os.mkdir(cachedir)
    pckfile = open( cachedir + "/" + cachename, 'wb')
    pickle.dump(dataset, pckfile)

def createDataset( user, dataset, pattern, readcache=False, 
                   basedir = None, run_range = None, json = None, unsafe = False, dbsInstance = None):
    if user == 'CMS' and pattern != ".*root":
        raise RuntimeError("For 'CMS' datasets, the pattern must be '.*root', while you configured '%s' for %s, %s" % (pattern, dataset.name, dataset))

    def cacheFileName(data, user, pattern, run_range, json):
        rr = "_run%s_%s" % (run_range[0], run_range[1]) if run_range else ""
        jj = ('%' + os.path.splitext(os.path.basename(json))[0]) if json is not None else ""
        return '{user}%{name}{rr}%{pattern}{jj}.pck'.format( user = user, name = data.replace('/','_'), pattern = pattern, rr=rr, jj=jj)

    def writeCache(dataset, data, user, pattern, run_range, json):
        writeDatasetToCache( cacheFileName(data, user, pattern, run_range, json), dataset )

    def readCache(data, user, pattern, run_range, json):
        return getDatasetFromCache( cacheFileName(data, user, pattern, run_range, json) )

    if readcache:
        try:
            data = readCache(dataset, user, pattern, run_range, json)
        except IOError:
            readcache = False
    if not readcache:
        #print "CreateDataset called: '%s', '%s', '%s', run_range %r" % (user, dataset, pattern, run_range) 
        if user == 'CMS':
            data = CMSDataset( dataset, run_range = run_range, json = json, unsafe = unsafe, dbsInstance = dbsInstance)
            info = False
        elif user == 'LOCAL':
            data = LocalDataset( dataset, basedir, pattern)
            info = False
        else:
            data = Dataset( dataset, user, pattern)
        writeCache(data, dataset, user, pattern, run_range, json)
    return data

### MM
def createMyDataset( user, dataset, pattern, dbsInstance, readcache=False):

    cachedir =  '/'.join( [os.environ['HOME'],'.cmgdataset'])

    def cacheFileName(data, user, dbsInstance, pattern):
        cf =  data.replace('/','_')
        name = '{dir}/{user}%{dbsInstance}%{name}%{pattern}.pck'.format(
            dir = cachedir,
            user = user,
            dbsInstance = dbsInstance,
            name = cf,
            pattern = pattern)
        return name

    def writeCache(dataset):
        if not os.path.exists(cachedir):
            os.mkdir(cachedir)
        cachename = cacheFileName(dataset.name,
                                  dataset.user,
                                  dataset.dbsInstance,
                                  dataset.pattern)
        pckfile = open( cachename, 'w')
        pickle.dump(dataset, pckfile)

    def readCache(data, user, dbsInstance, pattern):
        cachename = cacheFileName(data, user, dbsInstance, pattern)
        
        pckfile = open( cachename)
        dataset = pickle.load(pckfile)
        #print 'reading cache'                                                                                                                                                                   
        return dataset

    if readcache:
        try:
            data = readCache(dataset, user, dbsInstance, pattern)    
        except IOError:
            readcache = False
    if not readcache:
        if user == 'PRIVATE':
            data = PrivateDataset( dataset, dbsInstance )
            info = False
        writeCache(data)
    return data
### MM
