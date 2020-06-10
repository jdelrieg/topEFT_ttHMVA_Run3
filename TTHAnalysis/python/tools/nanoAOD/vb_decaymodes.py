from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection 

from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput

class VB_DecayModes(Module):
    def __init__(self, label=""):
        self.namebranches = [   "Z_decays",
                                "W_decays",
                                "TopP_decays",
                                "TopM_decays",
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

    def Prepare_decays_returns(self, ret, Z_daughters, W_daughters, TopP_daughters, TopM_daughters):

        # Block to handle events with one Z that is from N2 decay
        if (11 in Z_daughters and -11 in Z_daughters):
            ret["Z_decays"]=1111
        elif (13 in Z_daughters and -13 in Z_daughters):
            ret["Z_decays"]=1313
        elif (15 in Z_daughters and -15 in Z_daughters):
            ret["Z_decays"]=1515
        elif len(Z_daughters):
            raise RuntimeError("Did not find expected Z decays!")
            # Reweighting is based on TChiWZ sample that only has leptonic Z-decays. If hadronic Z-decays are found, we cannot use this!
        else: ret["Z_decays"]=0

        # Block to handle events with:
        # one W that is from C1 decay,
        # one top that is from stop decay, or
        # one anti-top that is from anti-stop decay
        for part, dlist in [['W',W_daughters],['TopP',TopP_daughters],['TopM',TopM_daughters]]:
            part_str = part + "_decays"
            if   ((6 in dlist and -5 in dlist) or (-6 in dlist and 5 in dlist)):
                ret[part_str]=65
            elif ((6 in dlist and -3 in dlist) or (-6 in dlist and 3 in dlist)):
                ret[part_str]=63    
            elif ((6 in dlist and -1 in dlist) or (-6 in dlist and 1 in dlist)):
                ret[part_str]=61
            elif ((4 in dlist and -5 in dlist) or (-4 in dlist and 5 in dlist)):
                ret[part_str]=45    
            elif ((4 in dlist and -3 in dlist) or (-4 in dlist and 3 in dlist)):
                ret[part_str]=43        
            elif ((4 in dlist and -1 in dlist) or (-4 in dlist and 1 in dlist)):
                ret[part_str]=41    
            elif ((2 in dlist and -5 in dlist) or (-2 in dlist and 5 in dlist)):
                ret[part_str]=25
            elif ((2 in dlist and -3 in dlist) or (-2 in dlist and 3 in dlist)):
                ret[part_str]=23
            elif ((2 in dlist and -1 in dlist) or (-2 in dlist and 1 in dlist)):
                ret[part_str]=21
            elif ((15 in dlist and -16 in dlist) or (-15 in dlist and 16 in dlist)):
                ret[part_str]=1516
            elif ((13 in dlist and -14 in dlist) or (-13 in dlist and 14 in dlist)):
                ret[part_str]=1314
            elif ((11 in dlist and -12 in dlist) or (-11 in dlist and 12 in dlist)):
                ret[part_str]=1112            
            elif len(dlist):
                raise RuntimeError("Did not find expected {} decays!".format(part))
            else: ret[part_str]=0


        return ret

    # Function to determine the indices of all particles in the family tree of particle i, so that the returned list will be:
    # [i, mother, grand-mother, ..., ancestor]
    def BuildFamilyTree(self, i, allgenpart):
        MotherIndex = i
        AncestorFound=0
        family_tree = []

        # Continue as long as the ultimate mother is not yet found.
        while not AncestorFound:
            # Build the family tree
            if allgenpart[MotherIndex].pdgId not in family_tree:
                family_tree.append(allgenpart[MotherIndex].pdgId)
                self.Log("Particle in family-tree:\t %d \t|\tid: %d   \t|\tpt: %f" % (MotherIndex, allgenpart[MotherIndex].pdgId, allgenpart[MotherIndex].pt), 3)

            # Cycle back through the family tree
            MotherIndex = allgenpart[MotherIndex].genPartIdxMother

            # Check if the mother has a mother
            AncestorFound = MotherIndex==-1         

        return family_tree

    # Logic of the algorithm
    def run(self,event,Collection,VB_DM_name):

        # Put the generator particles in a list so we can loop over it
        all_genpart = [gp for gp in Collection(event,"GenPart")]

        # prepare output
        ret = dict([(name,0.0) for name in self.namebranches])
        
        Z_daughters = []
        W_daughters = []
        TopP_daughters = []
        TopM_daughters = []

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
                FamilyTree = self.BuildFamilyTree(index,all_genpart)
                self.Log("Daughter of a Z-boson:\t %d \t|\tid: %d   \t|\tstatus: %d" % (index, gp.pdgId, gp.status),2)
                
                # If the grandmother is N2, we found the N2->N1+Z (->ll) decay
                if len(FamilyTree)>2 and FamilyTree[2]==1000023:
                    Z_daughters.append(gp.pdgId)

            # W-Boson daughters
            if abs(all_genpart[gp.genPartIdxMother].pdgId)==24:
                FamilyTree = self.BuildFamilyTree(index,all_genpart)
                self.Log("Daughter of a W-boson:\t %d \t|\tid: %d   \t|\tstatus: %d" % (index, gp.pdgId, gp.status),2)

                # If the grandmother is C1, we found the C1->N1+W (->ff) decay
                # Note that this decay also happens in T2bW (Stop->N1+C1(->N1+W (->ff)))
                if len(FamilyTree)>2 and abs(FamilyTree[2])==1000024:
                    if 1000006 in FamilyTree:
                        TopP_daughters.append(gp.pdgId)
                    elif -1000006 in FamilyTree:
                        TopM_daughters.append(gp.pdgId)
                    else:
                        W_daughters.append(gp.pdgId)

                # If the grandmother is Top+/-, we found the (anti-)Stop->N1+Top->N1+b+W(->ff) decay
                # Used for T2tt
                if len(FamilyTree)>2 and FamilyTree[2]==1000006:
                    TopP_daughters.append(gp.pdgId)
                if len(FamilyTree)>2 and FamilyTree[2]==-1000006:
                    TopM_daughters.append(gp.pdgId)

        # print TopP_daughters,TopM_daughters
        # Prepare the output to fill the branches
        ret = self.Prepare_decays_returns(ret, Z_daughters, W_daughters, TopP_daughters, TopM_daughters)
    
        # Put all ret branches together
        allret = {}
        for br in self.namebranches:
            allret[br+self.label] = ret[br]

    return allret


if __name__ == '__main__':
    import ROOT
    from sys import argv
