from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 

from CMGTools.NanoProc.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
import ROOT
from math import sqrt,cos
import os, json

class isrReweight( Module ):
    def __init__(self,
                 label = "isrWeight",
                 isrWfile="",
                 normWfile=""
             ):
        self.label = label
        self.events = 0

        #read isr corrections from file
        ##self.weights = getISRweights(isrWfile)
        self.weights =  {}
        with open(isrWfile) as f:
            self.weights = json.load(f)
        #changing json dict keys from str to tuples
        oldks = list(self.weights.keys())
        for k in oldks:
            self.weights[eval(k)] = self.weights.pop(k)

        inf = open(normWfile,'r')
        lines=inf.readlines()
        self.normWeights={}
        for l in lines:
            self.normWeights[ ( int(l.split()[0].split('_')[0]), int(l.split()[0].split('_')[1]))] =  float(l.split()[1])
        
        #utilities
        self.barcodeN1=1000022
        self.barcodeN2=1000023
        self.max_dm=80.

        # testing only
        self.run_diagnostics = True

    def getNormWeight(self, m1, m2):
        k = (m1, m2)
        if k in list(self.normWeights.keys()):
            return self.normWeights[k]
        else:
            print("WARNING! Normalization constant for ISR reweighting not found for mass combination (%s, %s). Assigning -1. " %(str(m1),str(m2)))
            return -1

    def getISRw(self, pt):
        ret=-1.
        for k in  list(self.weights.keys()):
            if pt >= k[0] and pt < k[1]:
                ret = self.weights[k]
                break
        return ret

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree

        self.wrappedOutputTree.branch(self.label,'F')
        if self.run_diagnostics:
            self.wrappedOutputTree.branch(self.label+"_isrPt",'F')
            self.wrappedOutputTree.branch(self.label+"_m1",'I')
            self.wrappedOutputTree.branch(self.label+"_m2",'I')

            self.wrappedOutputTree.branch(self.label+"_normw",'F')
            self.wrappedOutputTree.branch(self.label+"_ptw",'F')


    def analyze(self, event):
        mN1,pt1,phi1=0,0.,0.
        mN2,pt2,phi2=0,0.,0.
        # find the initial N1, N2 from the truth particles
        genParts = Collection(event, 'GenPart')
        for ip,p in enumerate(genParts):
            # find N1, N2
            if (not mN1 and abs(p.pdgId) == self.barcodeN1 
                and abs(p.genPartIdxMother) != self.barcodeN1):
                mN1 = int(p.mass+1e-5)
                pt1 = p.pt
                phi1 = p.phi
            if (not mN2 and abs(p.pdgId) == self.barcodeN2 
                and abs(p.genPartIdxMother) != self.barcodeN2):
                mN2 = int(p.mass+1e-5) 
                pt2 = p.pt
                phi2 = p.phi
                
        ISRpt=-1.
        if mN1!=0 and mN2!=0:
            ISRpt = sqrt( pt1**2 + pt2**2 + 2*pt1*pt2*cos(phi2-phi1)  ) 
        
        normw = self.getNormWeight(mN2,mN1)
        ptw = self.getISRw(ISRpt)
        corr = normw*ptw
        self.wrappedOutputTree.fillBranch(self.label, corr)
        if self.run_diagnostics:
            self.wrappedOutputTree.fillBranch(self.label+"_isrPt", ISRpt)
            self.wrappedOutputTree.fillBranch(self.label+"_m1", mN1)
            self.wrappedOutputTree.fillBranch(self.label+"_m2", mN2)
            self.wrappedOutputTree.fillBranch(self.label+"_normw", normw)
            self.wrappedOutputTree.fillBranch(self.label+"_ptw", ptw)

        return True
