from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection
#from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
from CMGTools.NanoProc.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
import numpy as np
import ROOT
import os
import array as ar
import time


class MVAvar:
    def __init__(self, name):
        self.name = name
        self.var = ar.array('f', [0.])

    def set(self, val):
        self.var[0] = val

class lepMVA_run3(Module):
    def __init__(self, inputpath="CMSSW_14_0_6/src/CMGTools/NanoProc/data/leptonMVA/tth/", elxmlpath="Electron-mvaTTH.2022EE.weights_mvaISO.xml", muxmlpath="Muon-mvaTTH.2022EE.weights.xml", suffix = "run3"):
            
        self.branches = [
            ("Electron_mvaTTH%s"%suffix, "F", 20, "nElectron"),
            ("Muon_mvaTTH%s"%suffix, "F", 20, "nMuon"),
        ]
        modelname = "BDTG"
        
        self.inputpath = inputpath
        self.elxmlpath = elxmlpath
        self.muxmlpath = muxmlpath
        self.suffix = suffix
                #self.inputVars = inputVars
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
        print('empieza a leer electrones')
        inicio_e=time.time()
        self.mva_electrons = self.open_model(os.path.join(inputpath, elxmlpath), self.inputVars["electrons"], "electrons")
        print('acaba electrones en: ',time.time()-inicio_e)
        print('empieza muones')
        inicio_m=time.time()
        self.mva_muons     = self.open_model(os.path.join(inputpath, muxmlpath), self.inputVars["muons"],  "muons")
        print('acaba muones en :',time.time()-inicio_m)
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
        print('empieza analyze')
        inicio_anal=time.time()
        ret = {
			"Electron_mvaTTH%s"%self.suffix : [],
			"Muon_mvaTTH%s"%self.suffix : [],
			}
        
        jets = Collection(event, "Jet", "nJet")

        for ilep, lep in enumerate(Collection(event, "Electron","nElectron")):
            self.set_vars(self.inputVars["electrons"], lep, jets)
            mva = self.evaluate(self.mva_electrons, "electrons")
            ret["Electron_mvaTTH%s"%self.suffix].append(mva)
            setattr(lep, "mvaTTH%s"%self.suffix, mva)
           
        for ilep, lep in enumerate(Collection(event, "Muon","nMuon")):
            self.set_vars(self.inputVars["muons"], lep, jets)
            mva = self.evaluate(self.mva_muons, "muons")
            ret["Muon_mvaTTH%s"%self.suffix].append(mva)
            setattr(lep, "mvaTTH%s"%self.suffix, mva)
                    
        writeOutput(self, ret)
        print('acaba analize en:',time.time()-inicio_anal)
        return True

lepMVA=lambda : lepMVA_run3("CMSSW_14_0_6/src/CMGTools/NanoProc/data/leptonMVA/tth/", "Electron-mvaTTH.2022EE.weights_mvaISO.xml","Muon-mvaTTH.2022EE.weights.xml")
