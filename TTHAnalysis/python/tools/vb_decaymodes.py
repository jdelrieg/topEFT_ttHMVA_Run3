from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection 

from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput

class VB_DecayModes(Module):
    def __init__(self, label=""):
        self.namebranches = [   "Z_decays",
                                "W_decays",
                            ]
        self.label = "" if (label in ["",None]) else ("_"+label)
        # self.inputlabel = '_'+recllabel
        self.branches = []
        for name in self.namebranches: self.branches.extend([name])

    # old interface (CMG)
    def listBranches(self):
        return self.branches[:]

    def __call__(self,event):
        return self.run(event, CMGCollection, "vb_decaymodes")

    # new interface (nanoAOD-tools)
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

        declareOutput(self, wrappedOutputTree, self.branches)
        self.inputTree = inputTree

    def analyze(self, event):
        writeOutput(self, self.run(event, NanoAODCollection, "vb_decaymodes"))
        return True

    # Function to determine what to print
    def Log(self,message,v):
        verbosity = 0 #0:nothing, 1:event info, 2:specific particles, 3:all particles
        if v<=verbosity:
            print(message)

    def Prepare_WZ_decays_returns(self, ret, Z_daughters, W_daughters):

        if (11 in Z_daughters and -11 in Z_daughters):
            ret["Z_decays"]=1111
        elif (13 in Z_daughters and -13 in Z_daughters):
            ret["Z_decays"]=1313
        elif (15 in Z_daughters and -15 in Z_daughters):
            ret["Z_decays"]=1515
        else:
            print("Found unknown Z decay!")
            ret["Z_decays"]=0

        if   ((6 in W_daughters and -5 in W_daughters) or (-6 in W_daughters and 5 in W_daughters)):
            ret["W_decays"]=65
        elif ((6 in W_daughters and -3 in W_daughters) or (-6 in W_daughters and 3 in W_daughters)):
            ret["W_decays"]=63    
        elif ((6 in W_daughters and -1 in W_daughters) or (-6 in W_daughters and 1 in W_daughters)):
            ret["W_decays"]=61
        elif ((4 in W_daughters and -5 in W_daughters) or (-4 in W_daughters and 5 in W_daughters)):
            ret["W_decays"]=45    
        elif ((4 in W_daughters and -3 in W_daughters) or (-4 in W_daughters and 3 in W_daughters)):
            ret["W_decays"]=43        
        elif ((4 in W_daughters and -1 in W_daughters) or (-4 in W_daughters and 1 in W_daughters)):
            ret["W_decays"]=41    
        elif ((2 in W_daughters and -5 in W_daughters) or (-2 in W_daughters and 5 in W_daughters)):
            ret["W_decays"]=25
        elif ((2 in W_daughters and -3 in W_daughters) or (-2 in W_daughters and 3 in W_daughters)):
            ret["W_decays"]=23
        elif ((2 in W_daughters and -1 in W_daughters) or (-2 in W_daughters and 1 in W_daughters)):
            ret["W_decays"]=21
        elif ((15 in W_daughters and -16 in W_daughters) or (-15 in W_daughters and 16 in W_daughters)):
            ret["W_decays"]=1516
        elif ((13 in W_daughters and -14 in W_daughters) or (-13 in W_daughters and 14 in W_daughters)):
            ret["W_decays"]=1314
        elif ((11 in W_daughters and -12 in W_daughters) or (-11 in W_daughters and 12 in W_daughters)):
            ret["W_decays"]=1112            
        else:
            print("Found unknown W decay! ",W_daughters)
            ret["W_decays"]=0

        return ret


    # logic of the algorithm
    def run(self,event,Collection,VB_DM_name):

        # Put the generator particles in a list so we can loop over it
        all_genpart = [gp for gp in Collection(event,"GenPart")]

        # prepare output
        ret = dict([(name,0.0) for name in self.namebranches])
        
        Z_daughters = []
        W_daughters = []

        # Loop over all generator particles
        for index,gp in enumerate(all_genpart):

            # Incoming partons have status 21; We don't care about these particles
            if gp.status==21:
                continue;

            # If we cannot determine the mother, continue;
            if gp.genPartIdxMother==-1:
                continue

            # Z-Boson daughters
            if abs(all_genpart[gp.genPartIdxMother].pdgId)==23:
                self.Log("Daughter of a Z-boson:\t %d \t|\tid: %d   \t|\tstatus: %d" % (index, gp.pdgId, gp.status),2)
                Z_daughters.append(gp.pdgId)

            # W-Boson daughters
            if abs(all_genpart[gp.genPartIdxMother].pdgId)==24:
                self.Log("Daughter of a W-boson:\t %d \t|\tid: %d   \t|\tstatus: %d" % (index, gp.pdgId, gp.status),2)
                W_daughters.append(gp.pdgId)

        # END of for loop over all generator particles
      
        # Prepare the output to fill the branches
        ret = self.Prepare_WZ_decays_returns(ret, Z_daughters, W_daughters)
    
        # Put all ret branches together
        allret = {}
        for br in self.namebranches:
            allret[br+self.label] = ret[br]

	return allret


if __name__ == '__main__':
    import ROOT
    from sys import argv

    # file = ROOT.TFile(argv[1])
    # tree = file.Get("Events")

    # branches=[]

    # for b in tree.GetListOfBranches():
    #     if "GenModel_TChiWZ_ZToLL_" in b.GetName():
    #         # print b.GetName()
    #         branches.append(b.GetName())

    # for iev in xrange(tree.GetEntries()):
    #     print "Event ",iev
    #     tree.GetEntry(iev)

    #     for k in range(len(branches)):
    #         # print getattr(tree, branches[k])
    #         if getattr(tree, branches[k])!=0:
    #             print branches[k]