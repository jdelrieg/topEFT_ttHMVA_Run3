from CMGTools.Production.globalOptions import getCMGOption
import copy


def fineSplitComponent(c):
    splitted = []
    for f in c.files:
        for i in range(c.fineSplitFactor):
            idx = len(splitted)
            nc = copy.deepcopy(c)
            nc.name = c.name + '_Chunk%d'%idx
            nc.files = [f]
            nc.fineSplit = (i,c.fineSplitFactor)
            splitted.append(nc)
    return splitted

def coarseSplitComponent(c):
    splitted = []
    n_files = len(c.files)
    chunk_size = int(n_files / c.splitFactor)
    if n_files % c.splitFactor:
        chunk_size += 1
    count_files=0
    for i in range(0, n_files, chunk_size):
        nc = copy.deepcopy(c)
        nc.name = c.name + '_Chunk%d'%len(splitted)
        nc.files = c.files[i:i+chunk_size]
        count_files+=len(nc.files)
        splitted.append(nc)
    if count_files != n_files:
        raise RuntimeError("Error in the component splitting") 
    return splitted

def split(components):
    splitted = []
    for c in components:
        doFineSplit = hasattr( c, 'fineSplitFactor') and c.fineSplitFactor>1
        doSplit = hasattr( c, 'splitFactor') and c.splitFactor>1
        if doFineSplit:
            splitted.extend(fineSplitComponent(c))
        elif doSplit:
            splitted.extend(coarseSplitComponent(c))
        else:
            splitted.append(c)
    return splitted

def redefineRunRange(selectedComponents,run_range):
    from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
    kreator = ComponentCreator()
    from math import ceil
    for comp in selectedComponents:
        if comp.isMC or not hasattr(comp, 'dataset') or comp.dataset.count("/") != 3: continue
        pre = len(comp.files)
        comp.files = kreator.getFiles(comp.dataset,"CMS",".*root",run_range=run_range)
        comp.splitFactor = max(1, int(ceil(comp.splitFactor * len(comp.files)/float(pre))) )
        if hasattr(comp, 'dataset_entries'):
            comp.dataset_entries = int(comp.dataset_entries * len(comp.files)/float(pre))

def printSummary(selectedComponents):
    print("%-55s | %8s %12s | %7s | %8s %11s | %11s" % ("Component", "N(files)", "N(k ev)", "N(jobs)", "file/job", "k ev/job", "lumi eq [1/fb]"))
    print("%-55s | %8s %12s | %7s | %8s %11s | %11s" % (55*"-", 8*"-", 12*"-", 7*"-", 8*"-", 11*"-", 11*"-"))
    totj, totf, tote = (0,0,0);
    for comp in sorted(selectedComponents, key = lambda c:c.name):
        njobs = min(comp.splitFactor,len(comp.files)) if getattr(comp,'fineSplitFactor',1) == 1 else comp.fineSplitFactor*len(comp.files) 
        nev   = getattr(comp, 'dataset_entries', 0)
        lumi  = nev/(1.e3 * comp.xSection) if comp.isMC and getattr(comp,'xSection',0) > 0 else 0
        if comp.isMC and (getattr(comp, 'fracNegWeights', None) != None):
            lumi *= (1 - 2*comp.fracNegWeights)**2
        totj += njobs; totf += len(comp.files); tote += nev     
        print("%-55s | %8d %12.3f | %7d | %8.2f %11.3f | %11.3f " % (comp.name, len(comp.files), nev/1000., njobs, len(comp.files)/float(njobs) if njobs else 0, (nev/njobs if njobs else 0)/1000, lumi))
    print("%-55s | %8s %12s | %7s | %8s %11s | %11s" % (55*"-", 8*"-", 12*"-", 7*"-", 8*"-", 11*"-", 11*"-"))
    print("%-55s | %8d %12.3f | %7d | %8.2f %11.3f |" % ("TOTAL", totf, tote/1000., totj, totf/totj if totj else -1, tote/totj/1000. if totj else -1))

def configureSplittingFromTime(selectedComponents,msPerEvent,jobTimeInHours,minSplit=None,minSplitDoesFineSplit=False,maxFiles=None,penaltyByOrigin=[]):
    from math import ceil, floor
    for comp in selectedComponents:
        nev = getattr(comp, 'dataset_entries', 0)
        if nev == 0: continue
        njobs = (nev * msPerEvent) / (3.6e6 * jobTimeInHours)
        filesPerJob = len(comp.files)/njobs
        for (pattern,penalty) in penaltyByOrigin:
            if any(f for f in comp.files if pattern in f): 
                filesPerJob /= penalty
                if maxFiles: maxFiles /= penalty
        if maxFiles and filesPerJob > maxFiles:
            filesPerJob = maxFiles
        if minSplit and njobs < minSplit:
            if minSplitDoesFineSplit: 
                raise RuntimeError("Not implemented")
            comp.splitFactor = minSplit
            continue
        if filesPerJob < 0.6:
            comp.splitFactor = 1
            comp.fineSplitFactor = ceil(1.0/filesPerJob)
        else:
            filesPerJob = max(floor(filesPerJob),1)
            comp.splitFactor = int(ceil(len(comp.files)/float(filesPerJob)))
        #print "for %s: %d events, %.1f ms/ev --> %.2f jobs" % (comp.name, nev, msPerEvent, njobs)

def cropToLumi(selectedComponents, maxLumi, minFiles=4):
    from math import ceil
    for comp in selectedComponents:
        nev   = getattr(comp, 'dataset_entries', 0)
        lumi  = nev/(1.e3 * comp.xSection) if comp.isMC and getattr(comp,'xSection',0) > 0 else 0
        if not lumi: continue
        if comp.isMC and (getattr(comp, 'fracNegWeights', None) != None):
            lumi *= (1 - 2*comp.fracNegWeights)**2
        if lumi > maxLumi:
            cfiles = int(ceil(len(comp.files) * maxLumi/lumi))
            if cfiles < minFiles: cfiles = min(minFiles, len(comp.files))
            comp.dataset_entries = nev * cfiles / float(len(comp.files))
            comp.files = comp.files[:cfiles]

def mergeExtensions(selectedComponents, verbose=False):
    compMap = {}
    for comp in sorted(selectedComponents, key = lambda c : c.name):
        
        if "_ext" in comp.name:
            basename = comp.name.split("_ext",1)[0]
        else:
            basename = comp.name
        if basename in compMap:
            f1, f2 = comp.files[:], compMap[basename].files
            e1, e2 = comp.dataset_entries, compMap[basename].dataset_entries
            if len(f1+f2) != len(set(f1+f2)):
                print("Merge %s into %s (%d+%d=%d files, %.3f+%.3f=%.3f k ev) %d" % (comp.name, basename, len(f1), len(f2), len(set(f1+f2)), 0.001*e1, 0.001*e2, 0.001*(e1+e2), len(f1+f2) != len(set(f1+f2))))
                raise Exception("Attempting to merge overlapping datasets!")
            if verbose: print("Merge %s into %s (%d+%d=%d files, %.3f+%.3f=%.3f k ev)" % (comp.name, basename, len(f1), len(f2), len(f1+f2), 0.001*e1, 0.001*e2, 0.001*(e1+e2)))
            compMap[basename].files = f1+f2
            compMap[basename].dataset_entries = e1+e2
        else:
            if "_ext" in comp.name: 
                if verbose: print("Rename %s to %s" % (comp.name, basename))
                comp.name = basename
            compMap[basename] = comp
    return list(compMap.values()), compMap

def prescaleComponents(selectedComponents, factor):
    from math import ceil
    for comp in selectedComponents:
        comp.dataset_entries = getattr(comp, 'dataset_entries', 0) / factor 
        comp.files = [ f for (i,f) in enumerate(comp.files) if ( (i % factor) == 0 ) ]


def autoConfig(selectedComponents,sequence,services=[],xrd_aggressive=2):
    import CMGTools.RootTools.fwlite.Config as cfg
    from CMGTools.TTHAnalysis.tools.EOSEventsWithDownload import EOSEventsWithDownload
    event_class = EOSEventsWithDownload
    EOSEventsWithDownload.aggressive = xrd_aggressive 
    if getCMGOption("nofetch") or getCMGOption("isCrab") or xrd_aggressive <= -3:
        raise RuntimeError("Not implemented anymore")
    return cfg.Config( components = selectedComponents,
                     sequence = sequence,
                     services = services,  
                     events_class = event_class)

def doTest1(comp, url=None, sequence=None, cache=False):
    from CMGTools.Production.globalOptions import setCMGOption
    comp.files = [ url if url else comp.files[0] ]
    if cache:
        import os
        tmpfil = os.path.expandvars("/tmp/$USER/%s" % os.path.basename(comp.files[0]))
        if not os.path.exists(tmpfil):
            os.system("xrdcp %s %s" % (comp.files[0],tmpfil))
        comp.files = [ tmpfil ]
    comp.splitFactor = 1
    comp.fineSplitFactor = 5 if getCMGOption('multi') else 1
    if getCMGOption('events'): insertEventSelector(sequence)
    if not getCMGOption('fetch'): setCMGOption('nofetch')
    return [ comp ]

def doTestN(test, selectedComponents):
    if test == '2':
        for comp in selectedComponents:
            comp.files = comp.files[:1]
            comp.splitFactor = 1
            comp.fineSplitFactor = 1
    elif test in ('3','3s'):
        for comp in selectedComponents:
            comp.files = comp.files[:3]
            if test == '3':
                comp.splitFactor = 1
                comp.fineSplitFactor = 3
            else:
                comp.splitFactor = len(comp.files)
 

