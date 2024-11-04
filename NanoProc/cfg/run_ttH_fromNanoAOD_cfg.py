import re, os, sys
from CMGTools.RootTools.samples.configTools import printSummary, mergeExtensions, doTestN, configureSplittingFromTime, cropToLumi
from CMGTools.RootTools.samples.autoAAAconfig import autoAAA
from CMGTools.Production.globalOptions import getCMGOption
from copy import deepcopy
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()
def byCompName(components, regexps):
    return [ c for c in components if any(re.match(r, c.name) for r in regexps) ]

year = getCMGOption("year", "2018")
analysis = getCMGOption("analysis", "main")
preprocessor = getCMGOption("nanoPreProcessor")
# Samples
if year == '2018':
    from CMGTools.RootTools.samples.samples_13TeV_RunIISummer20UL18NanoAODv9 import samples as mcSamplesImp
    from CMGTools.RootTools.samples.samples_13TeV_DATA2018_NanoAOD import dataSamples_UL18_GT36 as allData
elif year == '2017':
    from CMGTools.RootTools.samples.samples_13TeV_RunIISummer20UL17NanoAODv9 import samples as mcSamplesImp
    from CMGTools.RootTools.samples.samples_13TeV_DATA2017_NanoAOD import dataSamples_UL2017 as allData
elif year == '2016':
    from CMGTools.RootTools.samples.samples_13TeV_RunIISummer20UL16NanoAODv9 import samples as mcSamplesImp
    from CMGTools.RootTools.samples.samples_13TeV_DATA2016_NanoAOD import dataSamples_UL16 as allData
elif year == '2016APV':
    from CMGTools.RootTools.samples.samples_13TeV_RunIISummer20UL16APVNanoAODv9 import samples as mcSamplesImp
    from CMGTools.RootTools.samples.samples_13TeV_DATA2016APV_NanoAOD import dataSamples_UL16APV as allData
elif year == '2022':
    from CMGTools.RootTools.samples.samples_13p6TeV_mcRun3Summer22_nanoAODv12 import samples as mcSamplesImp
    from CMGTools.RootTools.samples.samples_13p6TeV_dataRun3Summer22_nanoAODv12 import dataSamples_22 as allData
elif year == '2022EE':
    from CMGTools.RootTools.samples.samples_13p6TeV_mcRun3Summer22EE_nanoAODv12 import samples as mcSamplesImp
    from CMGTools.RootTools.samples.samples_13p6TeV_dataRun3Summer22EE_nanoAODv12 import dataSamples_22EE as allData


mcSamples_=deepcopy(mcSamplesImp)
autoAAA(mcSamples_+allData, quiet=not(getCMGOption("verboseAAA",False)), redirectorAAA="xrootd-cms.infn.it") # must be done before mergeExtensions
mcSamples_, _ = mergeExtensions(mcSamples_)

from CMGTools.NanoProc.tools.nanoAOD.nano_postprocessing import triggerGroups_dict


DatasetsAndTriggers = []
if analysis == "main":
    if year in [ '2016', '2016APV', '2017', '2018']:
        mcSamples = byCompName(mcSamples_, ["%s(|_PS)$"%dset for dset in [
            # single boson
            #"WJetsToLNu_LO", "DYJetsToLL_M10to50_LO", "DYJetsToLL_M50",
            ## ttbar + single top + tW
            #"TTSemi_pow", "TTLep_pow",
            #"T_sch_lep", "T_tch", "TBar_tch", "T_tWch_noFullyHad", "TBar_tWch_noFullyHad",
            ## conversions
            #"TTGJets", "TGJets_lep", "WGToLNuG", "ZGTo2LG",
            ## ttV
            #"TTWToLNu_fxfx", "TTZToLLNuNu_amc", "TTZToLLNuNu_m1to10",
            #"TTWJetsToLNu_EWK_5f_NLO", 
            ## ttH + tHq/tHW
            #"TTHnobb_fxfx", "THQ_ctcvcp", "THW_ctcvcp", "TTH_ctcvcp",
            ## top + V rare processes
            #"TZQToLL", "TTTT", "TTWW",
            #"tWll_tlep_wlep","tWll_tlep_whad","tWll_thad_wlep", 
            ## diboson + DPS + WWss
            #"WWTo2L2Nu", "WZTo3LNu_pow", "WZTo3LNu_fxfx", "ZZTo4L", "WW_DPS", "WWTo2L2Nu_DPS", "WpWpJJ",
            ## triboson
            "WZZ",
            #"WWW", "WWW_ll", "WWZ", "WZG",  "ZZZ",
            # other Higgs processes
            #"GGHZZ4L", "VHToNonbb", "VHToNonbb_ll", "ZHTobb_ll", "ZHToTauTau", "TTWH", "TTZH",
        ]])
    else: # i hope they don't change dataset names again
        mcSamples = byCompName(mcSamples_, ["%s(|_PS)$"%dset for dset in [
            #single boson
            "DYto2L_2Jets_MLL_50","DYto2L_2Jets_MLL_50_ext",
            "DYto2L_2Jets_MLL_10to50","DYto2L_2Jets_MLL_10to50_ext","WtoLNu_2Jets",
            # ttbar + tW, not adding t- or s-channel
            "TTto2L2Nu", "TTto2L2Nu_ext",
            "TTtoLNu2Q", "TTtoLNu2Q_ext",
            "TbarWplusto2L2Nu", "TbarWplusto2L2Nu_ext", "TWminusto2L2Nu", "TWminusto2L2Nu_ext",
            # conversions
            "TTG_1Jets_PTG_200","TTG_1Jets_PTG_100to200","TTG_1Jets_PTG_10to100",
            "WGtoLNuG_PTG_10to100","WGtoLNuG_PTG_100to200","WZGtoLNuZG",
            "DYGto2LG_MLL_4to50_PTG_10to100","DYGto2LG_MLL_4to50_PTG_100to200","DYGto2LG_MLL_4to50_PTG_200",
            "DYGto2LG_MLL_50_PTG_10to50","DYGto2LG_MLL_50_PTG_50to100","DYGto2LG_MLL_50_PTG_100to200","DYGto2LG_MLL_50_PTG_200to400","DYGto2LG_MLL_50_PTG_400to600","DYGto2LG_MLL_50_PTG_600", 
            # ttV
            "TTLL_MLL_50", "TTLL_MLL_4to50", "TTLNu_1Jets",
            # ttH + tHq/tHW
            "TTHtoNon2B", "THQ_ctcvcp_sm", "THW_ctcvcp_sm",
            # top + V rare processes
            "TZQB",
            "TTTT",
            "TWZ_Tto2Q_WtoLNu_Zto2L_DR1", "TWZ_Tto2Q_WtoLNu_Zto2L_DR2",
            "TWZ_TtoLNu_Wto2Q_Zto2L_DR1", "TWZ_TtoLNu_Wto2Q_Zto2L_DR2",
            "TWZ_TtoLNu_WtoLNu_Zto2L_DR1", "TWZ_TtoLNu_WtoLNu_Zto2L_DR2", 
            "TTWW",
            # diboson + DPS + WWss
            "ZZto4L", "ZZto4L_ext",
            "WWto2L2Nu", "WWto2L2Nu_ext",  "WZto3LNu", 
            # missing "WWTo2L2Nu_DPS", "WpWpJJ",
            # triboson
            "WWW_4F", "WWZ_4F", 
            "WZG", "WZZ", "ZZZ",
            # other Higgs processes
            "GGHZZ4L", "VHToNonbb", "VHToNonbb_ll", "ZHTobb_ll", "ZHToTauTau", "TTWH", "TTZH",
        ]])


    DatasetsAndTriggers = dict([
        ("DoubleMuon"    , triggerGroups_dict["Trigger_2m"][year] + triggerGroups_dict["Trigger_3m"][year]),
        ("DoubleEG"      , triggerGroups_dict["Trigger_2e"][year] + triggerGroups_dict["Trigger_3e"][year]),
        ("MuonEG"        , triggerGroups_dict["Trigger_em"][year] + triggerGroups_dict["Trigger_mee"][year] + triggerGroups_dict["Trigger_mme"][year]),
        ("SingleMuon"    , triggerGroups_dict["Trigger_1m"][year]),
        ("SingleElectron", triggerGroups_dict["Trigger_1e"][year]),
        ("EGamma"        , triggerGroups_dict["Trigger_2e"][year] + triggerGroups_dict["Trigger_3e"][year] + triggerGroups_dict["Trigger_1e"][year]),
        ("Muon"          , triggerGroups_dict["Trigger_1m"][year] + triggerGroups_dict["Trigger_3m"][year]), # replaces double and single muon from era D 
    ])
    
    if year in [ '2016', '2016APV', '2017']:
        Datasets=["DoubleMuon", "DoubleEG", "MuonEG", "SingleElectron", "SingleMuon"]
    elif year == '2018': 
        Datasets=["DoubleMuon", "MuonEG", "EGamma", "SingleMuon"]
    elif year in [ '2022', '2022EE', '2023']: 
        Datasets=["DoubleMuon", "MuonEG", "EGamma", "SingleMuon", "Muon"]

    vetoMatrix = { 'DoubleMuon'	: [],
                   'SingleMuon' : ['DoubleMuon'],
                   'Muon'       : [], # replaces the two above

                   'DoubleEG'       : ['DoubleMuon', 'SingleMuon', 'Muon'],
                   'SingleElectron' : ['DoubleMuon', 'SingleMuon', 'Muon', 'DoubleEG'],
                   'EGamma'         : ['DoubleMuon', 'SingleMuon', 'Muon'], # replaces the two above

		   'MuonEG' : ['DoubleMuon', 'SingleMuon', 'Muon', 'DoubleEG', 'SingleElectron', 'EGamma'],
                  }
elif analysis == "met":
    if year in [ '2016', '2016APV', '2017', '2018']:
        mcSamples = byCompName(mcSamples_, ["%s(|_PS)$"%dset for dset in [
        ]])
    else: # i hope they don't change dataset names again
        mcSamples = byCompName(mcSamples_, ["%s(|_PS)$"%dset for dset in [
        ]])

    DatasetsAndTriggers = dict([
        ("JetMET"    , []),
    ])
    
    if year in [ '2016', '2016APV', '2017']:
        Datasets=[]
    elif year == '2018': 
        Datasets=[]
    elif year in [ '2022', '2022EE', '2023']: 
        Datasets=["JetMET"]

    vetoMatrix = { 'JetMET'	: [],
                  }

elif analysis == "frqcd":
    raise NotImplementedError 
    mcSamples = byCompName(mcSamples_, [
        "QCD_Mu15", "QCD_Pt(20|30|50|80|120|170)to.*_Mu5", 
        "QCD_Pt(20|30|50|80|120|170)to.*_EMEn.*", 
      (r"QCD_Pt(20|30|50|80|120|170)to\d+$"       if year == 2018 else  
        "QCD_Pt(20|30|50|80|120|170)to.*_bcToE.*" ),        
        "WJetsToLNu_LO", "DYJetsToLL_M50_LO", "DYJetsToLL_M10to50_LO", "TT(Lep|Semi)_pow"
    ])
    egfrpd = {2016:"DoubleEG", 2017:"SingleElectron", 2018:"EGamma"}[year]
    DatasetsAndTriggers.append( ("DoubleMuon", triggers["FR_1mu_noiso"] + triggers["FR_1mu_iso"]) )
    DatasetsAndTriggers.append( (egfrpd,       triggers["FR_1e_noiso"] + triggers["FR_1e_iso"]) )
    DatasetsAndTriggers.append( ("SingleMuon", triggers["FR_1mu_noiso_smpd"]) )

# make MC
mcTriggers = sum([DatasetsAndTriggers[pd] for pd in Datasets], [])
if getCMGOption('applyTriggersInMC'):
    for comp in mcSamples:
        comp.triggers = mcTriggers

# make data
dataSamples = [];
for pd in Datasets:
    for comp in byCompName(allData, [pd+"_"]):
        comp.triggers = DatasetsAndTriggers[pd]
        comp.vetoTriggers = []
        for vetoDataset in vetoMatrix[pd]:
            comp.vetoTriggers.extend( DatasetsAndTriggers[vetoDataset][:] )
        dataSamples.append(comp)

selectedComponents = mcSamples + dataSamples
if getCMGOption('selectComponents'):
    if getCMGOption('selectComponents')=='MC':
        selectedComponents = mcSamples
    elif getCMGOption('selectComponents')=='DATA':
        selectedComponents = dataSamples
    else:
        selectedComponents = byCompName(selectedComponents, getCMGOption('selectComponents').split(","))
#autoAAA(selectedComponents, quiet=not(getCMGOption("verboseAAA",False)), redirectorAAA="xrootd-cms.infn.it")

configureSplittingFromTime(dataSamples, 5,12)
configureSplittingFromTime(mcSamples, 100,12)
    
selectedComponents, _ = mergeExtensions(selectedComponents)




# print summary of components to process
if getCMGOption("justSummary"): 
    printSummary(selectedComponents)
    sys.exit(0)

from CMGTools.NanoProc.tools.nanoAOD.nano_postprocessing import *

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

# in the cut string, keep only the main cuts to have it simpler
modules = ttH_sequence_step1
if analysis == "met":
    modules = ttH_met_sequence_step1

cut = ttH_skim_cut

compression = "ZLIB:3" #"LZ4:4" #"LZMA:9"
branchsel_in = os.environ['CMSSW_BASE']+"/src/CMGTools/NanoProc/python/tools/nanoAOD/branchsel_in.txt"
branchsel_out = None

if analysis == "frqcd":
    modules = ttH_sequence_step1_FR
    cut = ttH_skim_cut_FR
    compression = "LZMA:9"
    branchsel_out = os.environ['CMSSW_BASE']+"/src/CMGTools/NanoProc/python/plotter/ttH-multilepton/qcd1l-skim-ec.txt"

POSTPROCESSOR = PostProcessor(None, [], modules = modules,
        cut = cut, prefetch = True, longTermCache = False,
        branchsel = branchsel_in, outputbranchsel = branchsel_out, compression = compression)



