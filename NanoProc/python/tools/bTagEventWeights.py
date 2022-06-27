#!/usr/bin/env python
import os.path, types
from array import array
from math import log, exp

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from CMGTools.NanoProc.treeReAnalyzer import ROOT, EventLoop
from BTagScaleFactors import BTagScaleFactors
from CMGTools.NanoProc.tools.nanoAOD.friendVariableProducerTools import declareOutput

class BTagEventWeightFriend:
    def __init__(self,
                 csvfile,
                 csvfastsim=None,
                 eff_rootfile=None,
                 year=None,
                 algo='csv',
                 wp='M',
                 btag_branch='btagCSV',
                 flavor_branch='hadronFlavour',
                 label='eventBTagSF',
                 recllabel='_Recl',
                 mcOnly=True):

        self.reader = BTagScaleFactors('btagsf',
                                       csvfile=csvfile,
                                       csvfastsim=csvfastsim,
                                       eff_rootfile=eff_rootfile,
                                       year=year,
                                       algo=algo,
                                       verbose=0)

        self.systsJEC = {0:"", 1:"_jecUp", -1:"_jecDown"}
        self.wp = wp
        self.recllabel = recllabel
        self.label = label
        self.btag_branch = btag_branch
        self.flavor_branch = flavor_branch
        self.mcOnly = mcOnly

        self.is_fastsim = (csvfastsim != None)

        # Automatically add the iterative systs from the reader
        self.btag_systs = ["central"]
        self.btag_systs += ["up_%s"  %s for s in self.reader.iterative_systs]
        self.btag_systs += ["down_%s"%s for s in self.reader.iterative_systs]

        # Take only central, up, and down for fastsim
        if self.is_fastsim:
            self.btag_systs = ["central", "up", "down"]


        # JEC to use for each syst:
        # Central one for all btag variations except up_jes and down_jes
        self.jec_syst_to_use = {}
        for btag_syst in self.btag_systs:
            self.jec_syst_to_use[btag_syst] = 0
        self.jec_syst_to_use["up_jes"] = 1
        self.jec_syst_to_use["down_jes"] = -1

        self.branches = self.listBranches()

    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        declareOutput(self, wrappedOutputTree, self.branches)
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def listBranches(self):
        out = []
        for syst in self.btag_systs:
            label = "%s_%s" % (self.label, syst)
            if syst == 'central': label = self.label
            out.append(label)

        return out

    def event_weight_from_discr_shape(self, jets, jetcorr,
                                      syst="central",
                                      flavorAttr=None,
                                      btagAttr=None):
        syst = syst.lower()
        if not flavorAttr: flavorAttr=self.flavor_branch
        if not btagAttr:   btagAttr=self.btag_branch

        weight = 1.0
        for i,jet in enumerate(jets):
            flavor  = getattr(jet, flavorAttr)
            btagval = getattr(jet, btagAttr)
            weight *= self.reader.get_SF(pt=jet.pt*jetcorr[i], eta=jet.eta,
                                  flavor=flavor, val=btagval,
                                  syst=syst, shape_corr=True)
        return weight

    def fastsim_event_weight(self, jets, jetcorr,
                             syst="central",
                             flavorAttr=None,
                             btagAttr=None,
                             wp='M'):
        """
        This would correspond to the event weight when for a selection
        of events with jets of the given WP.
        """
        syst = syst.lower()
        if not flavorAttr: flavorAttr=self.flavor_branch
        if not btagAttr:   btagAttr=self.btag_branch

        pmc = 1.0
        pdata = 1.0
        for i,jet in enumerate(jets):
            flavor  = getattr(jet, flavorAttr)
            btagval = getattr(jet, btagAttr)
            tagged = (btagval >= self.reader.working_points[wp])

            # Get FastSIM efficiency from MC
            efficiency = self.reader.get_tagging_efficiency(jet, wp)

            # Get FastSIM scale factors and multiply
            # Fastsim SF are defined as eff_full / eff_fast
            fastsim_syst = syst
            if 'correlated' in syst:
                fastsim_syst = syst.split('_', 1)[0] # take 'down' or 'up' for fastsim
            sf_fastsim = self.reader.get_SF(pt=jet.pt*jetcorr[i], eta=jet.eta,
                                            flavor=flavor, val=btagval, wp=wp,
                                            syst=fastsim_syst, mtype='fastsim')

            # Get FullSIM scale factors
            sf_fullsim = self.reader.get_SF(pt=jet.pt*jetcorr[i], eta=jet.eta,
                                            flavor=flavor, val=btagval, wp=wp,
                                            syst=syst, mtype='auto')

            # Combine factors for efficiency in data = Eff_FastSIM_MC * (Eff_FullSIM_MC / Eff_FastSIM_MC) * (Eff_Data / Eff_FullSIM_MC)
            eff_data = efficiency * sf_fastsim * sf_fullsim

            # Complimentary efficiencies for not tagged
            if not tagged:
                efficiency = 1.0 - efficiency # MC
                eff_data = 1.0 - eff_data # Data
                if eff_data < 0.0: print "WARNING: Negative efficiency computed!"


            pmc *= efficiency
            pdata *= eff_data
            if pdata < 0.0: print "WARNING: Negative probability computed!"

        try:
            return pdata/pmc
        except ZeroDivisionError:
            print "WARNING: scale factor of 0 found"
            return 1.0



    def analyze(self, event):
        ret = {k:1.0 for k in self.branches}
        #if self.mcOnly and event.isData: return ret

        jetscoll = {}
        for _var in self.systsJEC:
            jets = [j for j in Collection(event,"JetSel"+self.recllabel)]
            jetptcut = 25
            if (_var==0): jets = filter(lambda x : x.pt>jetptcut, jets)
            elif (_var==1): jets = filter(lambda x : x.pt_jesTotalUp>jetptcut, jets)
            elif (_var==-1): jets = filter(lambda x : x.pt_jesTotalDown>jetptcut, jets)
            if (_var==0): jetcorr = [1 for x in jets]
            elif (_var==1): jetcorr = [ x.pt_jesTotalUp/x.pt if x.pt != 0 else 1 for x in jets]
            elif (_var==-1): jetcorr = [ x.pt_jesTotalDown/x.pt  if x.pt != 0 else 1 for x in jets]
            jetscoll[_var]=(jets,jetcorr)

        for syst in self.btag_systs:

            _var=self.jec_syst_to_use[syst]

            label = "%s_%s" % (self.label, syst)
            if syst == 'central': label = self.label

            jets,jetcorr = jetscoll[_var]
            if not self.is_fastsim:
                weight = self.event_weight_from_discr_shape(jets,jetcorr, syst=syst, wp=self.wp)
            else:
                weight = self.fastsim_event_weight(jets,jetcorr, syst=syst, wp=self.wp)
            self.wrappedOutputTree.fillBranch(label,weight)
            ret[label] = weight
        return ret

if __name__ == '__main__':
    from sys import argv
    treefile = ROOT.TFile.Open(argv[1])
    tree = treefile.Get("tree")
    tree.vectorTree = True
    print "... processing %s" % argv[1]

    try:
        friendfile = ROOT.TFile.Open(argv[2])
        friendtree = friendfile.Get("sf/t")
        tree.AddFriend(friendtree)
        print "... adding friend tree from %s" % argv[2]
    except IndexError:
        pass


    btagsf_payload = os.path.join(os.environ['CMSSW_BASE'], "src/CMGTools/NanoProc/data/btag/", "CSVv2_ichep.csv")

#################################################################
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = BTagEventWeightFriend(btagsf_payload, recllabel="Recl", algo='csv')
            print "Adding these branches:", self.sf.listBranches()

        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: jets %d, isdata=%d" % (ev.run, ev.lumi, ev.evt, ev.nJet25, int(ev.isData))
            ret = self.sf(ev)
            jets = Collection(ev,"Jet")
            # leps = Collection(ev,"LepGood")

            for i,j in enumerate(jets):
                print "\tjet %8.2f %+5.2f %1d %.3f" % (j.pt, j.eta, getattr(j, "hadronFlavour", -1), min(max(0, j.btagCSV), 1))

            for label in self.sf.listBranches()[:10]:
                print "%8s"%label[-8:],
            print ""

            for label in self.sf.listBranches()[:10]:
                print "%8.3f" % ret[label],
            print ""


        def done(self):
            pass

    btagsf_payload_fastsim = os.path.join(os.environ['CMSSW_BASE'], "src/CMGTools/NanoProc/data/btag/", "CSV_13TEV_TTJets_11_7_2016.csv")
    btag_efficiency_file   = os.path.join(os.environ['CMSSW_BASE'], "src/CMGTools/NanoProc/data/btag/", "bTagEffs.root")

    class TesterFastSim(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = BTagEventWeightFriend(csvfile=btagsf_payload,
                                            csvfastsim=btagsf_payload_fastsim,
                                            eff_rootfile=btag_efficiency_file,
                                            recllabel="Recl", algo='csv')
            print "Adding these branches:", self.sf.listBranches()

        def analyze(self,ev):
            # print "\nrun %6d lumi %4d event %d: jets %d, isdata=%d" % (ev.run, ev.lumi, ev.evt, ev.nJet25, int(ev.isData))
            ret = self.sf(ev)
            # jets = Collection(ev,"Jet")
            # leps = Collection(ev,"LepGood")

            # for i,j in enumerate(jets):
            #     print "\tjet %8.2f %+5.2f %1d %.3f" % (j.pt, j.eta, getattr(j, "hadronFlavour", -1), min(max(0, j.btagCSV), 1))

            # for label in self.sf.listBranches()[:10]:
            #     print "%8s"%label[-8:],
            # print ""

            for label in self.sf.listBranches()[:10]:
                print "%8.3f" % ret[label],
            print ""


        def done(self):
            pass

    T = TesterFastSim("tester")
    el = EventLoop([ T ])
    el.loop([tree], maxEvents = 100)
    T.done()
