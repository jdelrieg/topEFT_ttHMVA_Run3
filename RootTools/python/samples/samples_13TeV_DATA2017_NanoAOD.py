# COMPONENT CREATOR
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

# ----------------------------- 2017 pp run  ----------------------------------------

json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'



# ----------------------------- Run2017B UL2017 ----------------------------------------

JetHT_Run2017B_UL2017 = kreator.makeDataComponent("JetHT_Run2017B_UL2017", "/JetHT/Run2017B-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
HTMHT_Run2017B_UL2017 = kreator.makeDataComponent("HTMHT_Run2017B_UL2017", "/HTMHT/Run2017B-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2017B_UL2017 = kreator.makeDataComponent("MET_Run2017B_UL2017", "/MET/Run2017B-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleElectron_Run2017B_UL2017 = kreator.makeDataComponent("SingleElectron_Run2017B_UL2017", "/SingleElectron/Run2017B-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017B_UL2017 = kreator.makeDataComponent("SingleMuon_Run2017B_UL2017", "/SingleMuon/Run2017B-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SinglePhoton_Run2017B_UL2017 = kreator.makeDataComponent("SinglePhoton_Run2017B_UL2017", "/SinglePhoton/Run2017B-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
DoubleEG_Run2017B_UL2017 = kreator.makeDataComponent("DoubleEG_Run2017B_UL2017", "/DoubleEG/Run2017B-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2017B_UL2017 = kreator.makeDataComponent("MuonEG_Run2017B_UL2017", "/MuonEG/Run2017B-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2017B_UL2017 = kreator.makeDataComponent("DoubleMuon_Run2017B_UL2017", "/DoubleMuon/Run2017B-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2017B_UL2017 = kreator.makeDataComponent("Tau_Run2017B_UL2017", "/Tau/Run2017B-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2017B_UL2017 = [JetHT_Run2017B_UL2017, HTMHT_Run2017B_UL2017, MET_Run2017B_UL2017, SingleElectron_Run2017B_UL2017, SingleMuon_Run2017B_UL2017, SinglePhoton_Run2017B_UL2017, DoubleEG_Run2017B_UL2017, MuonEG_Run2017B_UL2017, DoubleMuon_Run2017B_UL2017, Tau_Run2017B_UL2017]

# ----------------------------- Run2017C UL2017 ----------------------------------------

JetHT_Run2017C_UL2017 = kreator.makeDataComponent("JetHT_Run2017C_UL2017", "/JetHT/Run2017C-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
HTMHT_Run2017C_UL2017 = kreator.makeDataComponent("HTMHT_Run2017C_UL2017", "/HTMHT/Run2017C-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2017C_UL2017 = kreator.makeDataComponent("MET_Run2017C_UL2017", "/MET/Run2017C-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleElectron_Run2017C_UL2017 = kreator.makeDataComponent("SingleElectron_Run2017C_UL2017", "/SingleElectron/Run2017C-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017C_UL2017 = kreator.makeDataComponent("SingleMuon_Run2017C_UL2017", "/SingleMuon/Run2017C-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SinglePhoton_Run2017C_UL2017 = kreator.makeDataComponent("SinglePhoton_Run2017C_UL2017", "/SinglePhoton/Run2017C-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
DoubleEG_Run2017C_UL2017 = kreator.makeDataComponent("DoubleEG_Run2017C_UL2017", "/DoubleEG/Run2017C-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2017C_UL2017 = kreator.makeDataComponent("MuonEG_Run2017C_UL2017", "/MuonEG/Run2017C-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2017C_UL2017 = kreator.makeDataComponent("DoubleMuon_Run2017C_UL2017", "/DoubleMuon/Run2017C-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2017C_UL2017 = kreator.makeDataComponent("Tau_Run2017C_UL2017", "/Tau/Run2017C-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2017C_UL2017 = [JetHT_Run2017C_UL2017, HTMHT_Run2017C_UL2017, MET_Run2017C_UL2017, SingleElectron_Run2017C_UL2017, SingleMuon_Run2017C_UL2017, SinglePhoton_Run2017C_UL2017, DoubleEG_Run2017C_UL2017, MuonEG_Run2017C_UL2017, DoubleMuon_Run2017C_UL2017, Tau_Run2017C_UL2017]


# ----------------------------- Run2017D UL2017 ----------------------------------------

JetHT_Run2017D_UL2017 = kreator.makeDataComponent("JetHT_Run2017D_UL2017", "/JetHT/Run2017D-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
HTMHT_Run2017D_UL2017 = kreator.makeDataComponent("HTMHT_Run2017D_UL2017", "/HTMHT/Run2017D-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2017D_UL2017 = kreator.makeDataComponent("MET_Run2017D_UL2017", "/MET/Run2017D-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleElectron_Run2017D_UL2017 = kreator.makeDataComponent("SingleElectron_Run2017D_UL2017", "/SingleElectron/Run2017D-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017D_UL2017 = kreator.makeDataComponent("SingleMuon_Run2017D_UL2017", "/SingleMuon/Run2017D-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SinglePhoton_Run2017D_UL2017 = kreator.makeDataComponent("SinglePhoton_Run2017D_UL2017", "/SinglePhoton/Run2017D-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
DoubleEG_Run2017D_UL2017 = kreator.makeDataComponent("DoubleEG_Run2017D_UL2017", "/DoubleEG/Run2017D-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2017D_UL2017 = kreator.makeDataComponent("MuonEG_Run2017D_UL2017", "/MuonEG/Run2017D-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2017D_UL2017 = kreator.makeDataComponent("DoubleMuon_Run2017D_UL2017", "/DoubleMuon/Run2017D-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2017D_UL2017 = kreator.makeDataComponent("Tau_Run2017D_UL2017", "/Tau/Run2017D-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2017D_UL2017 = [JetHT_Run2017D_UL2017, HTMHT_Run2017D_UL2017, MET_Run2017D_UL2017, SingleElectron_Run2017D_UL2017, SingleMuon_Run2017D_UL2017, SinglePhoton_Run2017D_UL2017, DoubleEG_Run2017D_UL2017, MuonEG_Run2017D_UL2017, DoubleMuon_Run2017D_UL2017, Tau_Run2017D_UL2017]

# ----------------------------- Run2017E UL2017 ----------------------------------------

JetHT_Run2017E_UL2017 = kreator.makeDataComponent("JetHT_Run2017E_UL2017", "/JetHT/Run2017E-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
HTMHT_Run2017E_UL2017 = kreator.makeDataComponent("HTMHT_Run2017E_UL2017", "/HTMHT/Run2017E-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2017E_UL2017 = kreator.makeDataComponent("MET_Run2017E_UL2017", "/MET/Run2017E-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleElectron_Run2017E_UL2017 = kreator.makeDataComponent("SingleElectron_Run2017E_UL2017", "/SingleElectron/Run2017E-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017E_UL2017 = kreator.makeDataComponent("SingleMuon_Run2017E_UL2017", "/SingleMuon/Run2017E-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SinglePhoton_Run2017E_UL2017 = kreator.makeDataComponent("SinglePhoton_Run2017E_UL2017", "/SinglePhoton/Run2017E-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
DoubleEG_Run2017E_UL2017 = kreator.makeDataComponent("DoubleEG_Run2017E_UL2017", "/DoubleEG/Run2017E-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2017E_UL2017 = kreator.makeDataComponent("MuonEG_Run2017E_UL2017", "/MuonEG/Run2017E-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2017E_UL2017 = kreator.makeDataComponent("DoubleMuon_Run2017E_UL2017", "/DoubleMuon/Run2017E-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2017E_UL2017 = kreator.makeDataComponent("Tau_Run2017E_UL2017", "/Tau/Run2017E-UL2017_MiniAODv2_NanoAODv9-v2/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2017E_UL2017 = [JetHT_Run2017E_UL2017, HTMHT_Run2017E_UL2017, 
MET_Run2017E_UL2017, SingleElectron_Run2017E_UL2017, SingleMuon_Run2017E_UL2017, SinglePhoton_Run2017E_UL2017, DoubleEG_Run2017E_UL2017, MuonEG_Run2017E_UL2017, DoubleMuon_Run2017E_UL2017, Tau_Run2017E_UL2017]


# ----------------------------- Run2017F UL2017 ----------------------------------------

JetHT_Run2017F_UL2017 = kreator.makeDataComponent("JetHT_Run2017F_UL2017", "/JetHT/Run2017F-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
HTMHT_Run2017F_UL2017 = kreator.makeDataComponent("HTMHT_Run2017F_UL2017", "/HTMHT/Run2017F-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2017F_UL2017 = kreator.makeDataComponent("MET_Run2017F_UL2017", "/MET/Run2017F-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleElectron_Run2017F_UL2017 = kreator.makeDataComponent("SingleElectron_Run2017F_UL2017", "/SingleElectron/Run2017F-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017F_UL2017 = kreator.makeDataComponent("SingleMuon_Run2017F_UL2017", "/SingleMuon/Run2017F-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SinglePhoton_Run2017F_UL2017 = kreator.makeDataComponent("SinglePhoton_Run2017F_UL2017", "/SinglePhoton/Run2017F-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
DoubleEG_Run2017F_UL2017 = kreator.makeDataComponent("DoubleEG_Run2017F_UL2017", "/DoubleEG/Run2017F-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2017F_UL2017 = kreator.makeDataComponent("MuonEG_Run2017F_UL2017", "/MuonEG/Run2017F-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2017F_UL2017 = kreator.makeDataComponent("DoubleMuon_Run2017F_UL2017", "/DoubleMuon/Run2017F-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2017F_UL2017 = kreator.makeDataComponent("Tau_Run2017F_UL2017", "/Tau/Run2017F-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2017F_UL2017 = [JetHT_Run2017F_UL2017, HTMHT_Run2017F_UL2017, MET_Run2017F_UL2017, SingleElectron_Run2017F_UL2017, SingleMuon_Run2017F_UL2017, SinglePhoton_Run2017F_UL2017, DoubleEG_Run2017F_UL2017, MuonEG_Run2017F_UL2017, DoubleMuon_Run2017F_UL2017, Tau_Run2017F_UL2017]

dataSamples_UL2017 = dataSamples_Run2017B_UL2017 + dataSamples_Run2017C_UL2017 + dataSamples_Run2017D_UL2017 + dataSamples_Run2017E_UL2017 + dataSamples_Run2017F_UL2017


dataSamples = dataSamples_UL2017
samples = dataSamples

# ---------------------------------------------------------------------

if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples, localobjs=locals())
