from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
import os

json=os.environ['CMSSW_BASE']+"/src/CMGTools/RootTools/data/Cert_Collisions2022_355100_362760_Golden.json"

kreator = ComponentCreator()

JetMET_Run2022E  = kreator.makeDataComponent("JetMET_Run2022E", "/JetMET/Run2022E-22Sep2023-v1/NANOAOD", "CMS", ".*root", json)
EGamma_Run2022E  = kreator.makeDataComponent("EGamma_Run2022E", "/EGamma/Run2022E-22Sep2023-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2022E  = kreator.makeDataComponent("MuonEG_Run2022E", "/MuonEG/Run2022E-22Sep2023-v1/NANOAOD", "CMS", ".*root", json)
Muon_Run2022E    = kreator.makeDataComponent("Muon_Run2022E", "/Muon/Run2022E-22Sep2023-v1/NANOAOD", "CMS", ".*root", json)
JetMET_Run2022F  = kreator.makeDataComponent("JetMET_Run2022F", "/JetMET/Run2022F-22Sep2023-v2/NANOAOD", "CMS", ".*root", json)
EGamma_Run2022F  = kreator.makeDataComponent("EGamma_Run2022F", "/EGamma/Run2022F-22Sep2023-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2022F  = kreator.makeDataComponent("MuonEG_Run2022F", "/MuonEG/Run2022F-22Sep2023-v1/NANOAOD", "CMS", ".*root", json)
Muon_Run2022F    = kreator.makeDataComponent("Muon_Run2022F", "/Muon/Run2022F-22Sep2023-v2/NANOAOD", "CMS", ".*root", json)
JetMET_Run2022G  = kreator.makeDataComponent("JetMET_Run2022G", "/JetMET/Run2022G-22Sep2023-v2/NANOAOD", "CMS", ".*root", json)
EGamma_Run2022G  = kreator.makeDataComponent("EGamma_Run2022G", "/EGamma/Run2022G-22Sep2023-v2/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2022G  = kreator.makeDataComponent("MuonEG_Run2022G", "/MuonEG/Run2022G-22Sep2023-v1/NANOAOD", "CMS", ".*root", json)
Muon_Run2022G    = kreator.makeDataComponent("Muon_Run2022G", "/Muon/Run2022G-22Sep2023-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_22EE=[JetMET_Run2022E,EGamma_Run2022E,MuonEG_Run2022E,Muon_Run2022E,JetMET_Run2022F,EGamma_Run2022F,MuonEG_Run2022F,Muon_Run2022F,JetMET_Run2022G,EGamma_Run2022G,MuonEG_Run2022G,Muon_Run2022G]
