from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection
from CMGTools.NanoProc.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
import numpy as np
import ROOT
import os
import array as ar


class MVAvar:
    def __init__(self, name):
        self.name = name
        self.var = ar.array('f', [0.])

    def set(self, val):
        self.var[0] = val

class lepMVAWZ_run3(Module):
    def __init__(self, inputpath, elxmlpath, muxmlpath, suffix = "run3"):
            
        self.branches = [
            ("LepGood_mvaTTH%s"%suffix, "F", 20, "nLepGood"),
        ]
        modelname = "BDTG"
        
        self.inputpath = inputpath
        self.elxmlpath = elxmlpath
        self.muxmlpath = muxmlpath
        self.suffix = suffix
        
        self.inputVars = {
            "electrons" : { 
                "Electron_pt" : [MVAvar("Electron_pt"), lambda lep, jets: lep.pt],
                "Electron_eta" : [MVAvar("Electron_eta"), lambda lep, jets: lep.eta],
                "Electron_pfRelIso03_all" : [MVAvar("Electron_pfRelIso03_all"), lambda lep, jets: lep.pfRelIso03_all],
                "Electron_miniPFRelIso_chg" :[MVAvar("Electron_miniPFRelIso_chg"), lambda lep, jets: lep.miniPFRelIso_chg ],
                "Electron_miniRelIsoNeutral := Electron_miniPFRelIso_all - Electron_miniPFRelIso_chg" :[MVAvar("Electron_miniRelIsoNeutral := Electron_miniPFRelIso_all - Electron_miniPFRelIso_chg"), lambda lep, jets: lep.miniPFRelIso_all - lep.miniPFRelIso_chg],
                "Electron_jetNDauCharged" :[MVAvar("Electron_jetNDauCharged"), lambda lep, jets: lep.jetNDauCharged],
                "Electron_jetPtRelv2" :[MVAvar("Electron_jetPtRelv2"), lambda lep, jets: lep.jetPtRelv2],
                "Electron_jetBTagDeepFlavB := Electron_jetIdx > -1 ? Jet_btagDeepFlavB[Electron_jetIdx] : 0" :[MVAvar("Electron_jetBTagDeepFlavB := Electron_jetIdx > -1 ? Jet_btagDeepFlavB[Electron_jetIdx] : 0"), lambda lep, jets: jets[lep.jetIdx].btagDeepFlavB if lep.jetIdx > -1 else 0],
                "Electron_jetPtRatio := min(1 / (1 + Electron_jetRelIso), 1.5)" :[MVAvar("Electron_jetPtRatio := min(1 / (1 + Electron_jetRelIso), 1.5)"), lambda lep, jets: min(1. / (1. + lep.jetRelIso), 1.5) ],
                "Electron_sip3d" :[MVAvar("Electron_sip3d"), lambda lep, jets: lep.sip3d],
                "Electron_log_dxy := log(abs(Electron_dxy))" :[MVAvar("Electron_log_dxy := log(abs(Electron_dxy))"), lambda lep, jets: np.log(abs(lep.dxy))],
                "Electron_log_dz  := log(abs(Electron_dz))" :[MVAvar("Electron_log_dz  := log(abs(Electron_dz))"), lambda lep, jets: np.log(abs(lep.dz))],
                "Electron_mvaNoIso" : [MVAvar("Electron_mvaIso"),lambda lep, jets: lep.mvaIso],
            },
            'muons' : {
                "Muon_pt" : [MVAvar("Muon_pt"), lambda lep, jets: lep.pt],
                "Muon_eta" :  [MVAvar("Muon_eta"), lambda lep, jets: lep.eta],
                "Muon_pfRelIso03_all" :  [MVAvar("Muon_pfRelIso03_all"), lambda lep, jets: lep.pfRelIso03_all],
                "Muon_miniPFRelIso_chg" :  [MVAvar("Muon_miniPFRelIso_chg"), lambda lep, jets: lep.miniPFRelIso_chg ],
                "Muon_miniRelIsoNeutral := Muon_miniPFRelIso_all - Muon_miniPFRelIso_chg" :  [MVAvar("Muon_miniRelIsoNeutral := Muon_miniPFRelIso_all - Muon_miniPFRelIso_chg"), lambda lep, jets: lep.miniPFRelIso_all - lep.miniPFRelIso_chg],
                "Muon_jetNDauCharged" : [MVAvar("Muon_jetNDauCharged"), lambda lep, jets: lep.jetNDauCharged],
                "Muon_jetPtRelv2" :  [MVAvar("Muon_jetPtRelv2"), lambda lep, jets: lep.jetPtRelv2],
                "Muon_jetBTagDeepFlavB := Muon_jetIdx > -1 ? Jet_btagDeepFlavB[Muon_jetIdx] : 0" :  [MVAvar("Muon_jetBTagDeepFlavB := Muon_jetIdx > -1 ? Jet_btagDeepFlavB[Muon_jetIdx] : 0"), lambda lep, jets: jets[lep.jetIdx].btagDeepFlavB if lep.jetIdx > -1 else 0],
                "Muon_jetPtRatio := min(1 / (1 + Muon_jetRelIso), 1.5)" :  [MVAvar("Muon_jetPtRatio := min(1 / (1 + Muon_jetRelIso), 1.5)"), lambda lep, jets: min(1. / (1. + lep.jetRelIso), 1.5) ],
	        "Muon_sip3d" :  [MVAvar("Muon_sip3d"), lambda lep, jets: lep.sip3d],
                "Muon_log_dxy := log(abs(Muon_dxy))" :  [MVAvar("Muon_log_dxy := log(abs(Muon_dxy))"), lambda lep, jets: np.log(abs(lep.dxy))],
	        "Muon_log_dz  := log(abs(Muon_dz))" :  [MVAvar("Muon_log_dz  := log(abs(Muon_dz))"), lambda lep, jets: np.log(abs(lep.dz))],
                "Muon_segmentComp" :  [MVAvar("Muon_segmentComp"),lambda lep, jets: lep.segmentComp],
            }
        }
        self.mva_electrons = self.open_model(os.path.join(inputpath, elxmlpath), self.inputVars["electrons"], "electrons")
        self.mva_muons     = self.open_model(os.path.join(inputpath, muxmlpath), self.inputVars["muons"],  "muons")
        return
    
    def open_model(self, xmlpath, vars, modelname):
        """ Method to open a model a load variables """
        print(" >> Opening model: %s"%xmlpath)
        reader = ROOT.TMVA.Reader()
        for vname, v in vars.items():
                print("  + Adding variable: ", v[0].name) 
                reader.AddVariable(v[0].name, v[0].var)
        print(">> Booking MVA")
        reader.BookMVA(modelname, xmlpath)
        return reader

    
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        declareOutput(self, wrappedOutputTree, self.branches)
        return

    def set_vars(self, vars, lep, jets):
        """ Set the values of the variables before evaluating MVA """
        for vname, v in vars.items():
            lambda_func = v[1]
            v[0].set( lambda_func(lep, jets) )
        return
    
    def evaluate(self, mva, name):
        return mva.EvaluateMVA(name)
    
    def analyze(self, event):
        """ All the magic happens here """
        ret = {
            "LepGood_mvaTTH%s"%self.suffix : [],
        }
        
        jets = Collection(event, "Jet", "nJet")

        for ilep, lep in enumerate(Collection(event, "LepGood","nLepGood")):
            if abs(lep.pdgId) == 11: # Electrons                
                # Set the values of the input variables
                self.set_vars(self.inputVars["electrons"], lep, jets)
                
                # Evaluate the MVA
                mva = self.evaluate(self.mva_electrons, "electrons")
                
                # Save it
                ret["LepGood_mvaTTH%s"%self.suffix].append(mva)
                setattr(lep, "mvaTTH%s"%self.suffix, mva)
            elif abs(lep.pdgId) == 13: # Muons         
                # Set the values of the input variables
                self.set_vars(self.inputVars["muons"], lep, jets)
                
                # Evaluate the MVA
                mva = self.evaluate(self.mva_muons, "muons")
                
                # Save it
                ret["LepGood_mvaTTH%s"%self.suffix].append(mva)
                setattr(lep, "mvaTTH%s"%self.suffix, mva)
            else:
                ret["LepGood_mvaTTH%s"%self.suffix].append(-1)
                    
        writeOutput(self, ret)
        return True

if __name__ == '__main__':
    """ Debug the module """
    from sys import argv
    from copy import deepcopy
    from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import eventLoop
    from PhysicsTools.NanoAODTools.postprocessing.framework.output import FriendOutput, FullOutput
    from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import InputTree
    
    mainpath = "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/MC/2022PostEE/WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8/mcRun3_PostEE_oct2023_WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8/231023_150004/0000/"
    process = "tree_12"
    
    nentries = int(argv[1])
    ### Open the main file
    file_ = ROOT.TFile( os.path.join(mainpath, process+".root") )
    tree = file_.Get("Events")

    
    ### Replicate the eventLoop
    tree = InputTree(tree)
    outFile = ROOT.TFile.Open("test_%s.root"%process, "RECREATE")
    #outTree = FriendOutput(file_, tree, outFile)
    outTree = FullOutput(file_, tree, outFile, maxEntries = nentries)
    
    weightspath_2022EE   = os.path.join(os.environ["CMSSW_BASE"], "src/CMGTools/TTHAnalysis/data/WZRun3/lepMVA/2022EE")
    
    from CMGTools.TTHAnalysis.tools.nanoAOD.wzsm_modules import lepMerge_EE
    import CMGTools.TTHAnalysis.tools.nanoAOD.mvaTTH_vars_run3 as mvatth_cfg

    weightspath_2022EE = os.path.join(os.environ["CMSSW_BASE"], "src/CMGTools/TTHAnalysis/data/WZRun3/")

    module_test = lepMVAWZ_run3(
        weightspath_2022EE, 
        elxmlpath = "EGM/Electron-mvaTTH.2022EE.weights_mvaISO.xml", 
        muxmlpath = "MUO/Muon-mvaTTH.2022EE.weights.xml", 
        suffix = "_run3",
        inputVars = {"muons":  mvatth_cfg.muon_df("2022"), "electrons" : mvatth_cfg.electron_df_wIso("2022")}
    )
    
    module_test.beginJob()
    (nall, npass, timeLoop) = eventLoop([lepMerge_EE, module_test], file_, outFile, tree, outTree, maxEvents = nentries)
    print(('Processed %d preselected entries from %s (%s entries). Finally selected %d entries' % (nall, __file__.split("/")[-1].replace(".py", ""), nentries, npass)))
    outTree.write()
    file_.Close()
    outFile.Close()
    print("Test done")
    module_test.endJob()




