from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
import os
json=os.environ['CMSSW_BASE']+"/src/CMGTools/RootTools/data/Cert_Collisions2022_355100_362760_Golden.json"

kreator = ComponentCreator()
JetMET_Run2022C  = kreator.makeDataComponent("JetMET_Run2022C", "/JetMET/Run2022C-22Sep2023-v1/NANOAOD", "CMS", ".*root", json)
EGamma_Run2022C  = kreator.makeDataComponent("EGamma_Run2022C", "/EGamma/Run2022C-22Sep2023-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2022C  = kreator.makeDataComponent("MuonEG_Run2022C", "/MuonEG/Run2022C-22Sep2023-v1/NANOAOD", "CMS", ".*root", json)
Muon_Run2022C    = kreator.makeDataComponent("Muon_Run2022C", "/Muon/Run2022C-22Sep2023-v1/NANOAOD", "CMS", ".*root", json)
JetMET_Run2022D  = kreator.makeDataComponent("JetMET_Run2022D", "/JetMET/Run2022D-22Sep2023-v1/NANOAOD", "CMS", ".*root", json)
EGamma_Run2022D  = kreator.makeDataComponent("EGamma_Run2022D", "/EGamma/Run2022D-22Sep2023-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2022D  = kreator.makeDataComponent("MuonEG_Run2022D", "/MuonEG/Run2022D-22Sep2023-v1/NANOAOD", "CMS", ".*root", json)
Muon_Run2022D    = kreator.makeDataComponent("Muon_Run2022D", "/Muon/Run2022D-22Sep2023-v1/NANOAOD", "CMS", ".*root", json)



dataSamples_22=[JetMET_Run2022C,EGamma_Run2022C,MuonEG_Run2022C,Muon_Run2022C,JetMET_Run2022D,EGamma_Run2022D,MuonEG_Run2022D,Muon_Run2022D]
