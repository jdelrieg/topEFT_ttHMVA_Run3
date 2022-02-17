from __future__ import print_function
from ROOT import gROOT,gSystem

def load_libs():
    print('loading FWLite.')
    #load the libaries needed
    gSystem.Load("libFWCoreFWLite")
    gROOT.ProcessLine('FWLiteEnabler::enable();')
    gSystem.Load("libFWCoreFWLite")
        
    #now the RootTools stuff
    gSystem.Load("libCMGToolsHeppy")

load_libs()
