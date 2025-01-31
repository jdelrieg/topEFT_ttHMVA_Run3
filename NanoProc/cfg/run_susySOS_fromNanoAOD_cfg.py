import re, os, sys
from CMGTools.RootTools.samples.configTools import printSummary, mergeExtensions, doTestN, configureSplittingFromTime, cropToLumi
from CMGTools.RootTools.samples.autoAAAconfig import autoAAA
from CMGTools.Production.globalOptions import getCMGOption

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()
def byCompName(components, regexps):
    return [ c for c in components if any(re.match(r, c.name) for r in regexps) ]

year = int(getCMGOption("year", "2018"))
analysis = getCMGOption("analysis", "main")
preprocessor = getCMGOption("nanoPreProcessor")

if getCMGOption("nanoPreProcessor"):
    if year == 2018:
        from CMGTools.RootTools.samples.samples_13TeV_RunIIAutumn18MiniAOD import samples as mcSamples_
        from CMGTools.RootTools.samples.samples_13TeV_DATA2018_MiniAOD import samples as allData
    elif year == 2017:
        from CMGTools.RootTools.samples.samples_13TeV_RunIIFall17MiniAOD import samples as mcSamples_
        from CMGTools.RootTools.samples.samples_13TeV_DATA2017 import dataSamples_31Mar2018 as allData
    elif year == 2016:
        from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv3 import samples as mcSamples_
        from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import dataSamples_17Jul2018 as allData
else:
    if year == 2018:
        from CMGTools.RootTools.samples.samples_13TeV_RunIIAutumn18NanoAODv6 import samples as mcSamples_
        from CMGTools.RootTools.samples.samples_13TeV_DATA2018_NanoAOD import dataSamples_25Oct2019 as allData
    elif year == 2017:
        from CMGTools.RootTools.samples.samples_13TeV_RunIIFall17NanoAODv6 import samples as mcSamples_
        from CMGTools.RootTools.samples.samples_13TeV_DATA2017_NanoAOD import dataSamples_25Oct2019 as allData
    elif year == 2016:
        from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16NanoAODv6 import samples as mcSamples_
        from CMGTools.RootTools.samples.samples_13TeV_DATA2016_NanoAOD import dataSamples_25Oct2019 as allData

DatasetsAndTriggers = []
if year == 2018:
#    from CMGTools.RootTools.samples.triggers_13TeV_DATA2018 import all_triggers as triggers
    if analysis == "main":
        mcSamples = byCompName(mcSamples_, [

            ## low Mll Samples
            "ZZTo4L_M1toInf",
            "VVTo2L2Nu_M1toInf",
            "DYJetsToLL_M1to4_HT70to100",
            "DYJetsToLL_M1to4_HT100to200",
            "DYJetsToLL_M1to4_HT200to400",
            "DYJetsToLL_M1to4_HT400to600",
            "DYJetsToLL_M1to4_HT600toInf",

##            "DYJetsToLL_M10to50_LO",
            #"DYJetsToLL_M50_LO", # for Tag and Probe studies
##            "DYJetsToLL_M50_LO_ext",


            "T_tWch_noFullyHad",
            "TBar_tWch_noFullyHad",

            "DYJetsToLL_M4to50_HT70to100",
            "DYJetsToLL_M4to50_HT100to200",
            "DYJetsToLL_M4to50_HT200to400",
            "DYJetsToLL_M4to50_HT400to600",
            "DYJetsToLL_M4to50_HT600toInf",

            "DYJetsToLL_M50_HT100to200",
            "DYJetsToLL_M50_HT200to400",
            "DYJetsToLL_M50_HT400to600",
            "DYJetsToLL_M50_HT600to800",
            "DYJetsToLL_M50_HT800to1200",
            "DYJetsToLL_M50_HT1200to2500",
            "DYJetsToLL_M50_HT2500toInf",

            "TTJets_DiLepton$",

            #check if VVTo2L2Nu is there
            "VVTo2L2Nu",
#            "WWTo2L2Nu$",
#            "ZZTo2L2Nu",
            "TTJets_SingleLeptonFromT$", "TTJets_SingleLeptonFromTbar$", 
            
            "WJetsToLNu_HT100to200",
            "WJetsToLNu_HT200to400",
            "WJetsToLNu_HT400to600",
            "WJetsToLNu_HT600to800",
            "WJetsToLNu_HT800to1200",
            "WJetsToLNu_HT1200to2500",
            "WJetsToLNu_HT2500toInf",

            "WZTo3LNu_fxfx$",
            "WWToLNuQQ",
            #"WZTo1L1Nu2Q",
            "ZZTo4L$",
            "WWW",#_4F
            "WZZ$",
            "WWZ", #FIX! not _4F
            "ZZZ$",
            "T_tch$",
            "TBar_tch$",
            "T_sch_lep$",
            "WW_DPS",
            "TTWToLNu_fxfx$",
            "TTZToLLNuNu_amc$",
            "TTZToLLNuNu_m1to10$",
            "TTGJets$",
            "TGJets_lep", 

            #missing tbc
            "ZZTo2L2Q", 
            "WpWpJJ",
#            "WZTo1L3Nu",
            "WGToLNuG",
            "ZGTo2LG",
            "WZTo2L2Q",
            "TZQToLL",
            "tWll",
            "WZTo3LNu_mllmin01",

            ##signal SUSY
            "SMS_TChiWZ",
            "SMS_TChiWZ_ext",
            "SMS_HiggsinoN2N1",
            "SMS_HiggsinoN2C1", 
            "SMS_T2tt",
            "SMS_T2tt_ext",
            "SMS_T2bW",
            "SMS_T2bW_ext",
            "SMS_HiggsinoPMSSM",
           
###relics from tth             
###            "TT[WZ]_LO$",
###            "TTHnobb_pow$",
###            "TZQToLL$", "tWll$", "TTTT$", "TTWW$",
###            "WpWpJJ$",
###            "GGHZZ4L$", "VHToNonbb_ll$",
###            "WWW_ll$", "WWZ$", "WZG$",  "WW_DPS$", 
            

        ])

    if analysis == "main":
##        DatasetsAndTriggers.append( ("DoubleMuon", triggers["mumu_iso"] + triggers["3mu"]) )
        DatasetsAndTriggers.append( ("MET",         ["%s_v*"%x for x in ['HLT_PFMETNoMu120_PFMHTNoMu120_IDTight','HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60']] ) )
        DatasetsAndTriggers.append( ("DoubleMuon",  ["%s_v*"%x for x in ['HLT_DoubleMu3_DZ_PFMET50_PFMHT60','HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8']]) )
        DatasetsAndTriggers.append( ("SingleMuon",  ["%s_v*"%x for x in ['HLT_Mu3er1p5_PFJet100er2p5_PFMET80_PFMHT80_IDTight',
                                                                         'HLT_Mu3er1p5_PFJet100er2p5_PFMET90_PFMHT90_IDTight',
                                                                         'HLT_Mu3er1p5_PFJet100er2p5_PFMET100_PFMHT100_IDTight']] ) )
#        DatasetsAndTriggers.append( ("EGamma",      triggers["SOS_eleTnP"] ) )
#        DatasetsAndTriggers.append( ("SingleMuon",  triggers["SOS_muTnP"] ) )
##        DatasetsAndTriggers.append( ("SingleMuon", triggers["1mu_iso"]) ) ##which one?? ##PD SingleMuon o MET?
##conf db e cercare stream dato il nome del trigger

elif year == 2017:
#    from CMGTools.RootTools.samples.triggers_13TeV_DATA2017 import all_triggers as triggers
    mcSamples = byCompName(mcSamples_, [

        ## low Mll Samples
        "ZZTo4L_M1toInf",
        "VVTo2L2Nu_M1toInf",
        "DYJetsToLL_M1to4_HT",

#        "DYJetsToLL_M50_LO", # for Tag and Probe studies
#        "DYJetsToLL_M10to50_LO_ext,"
##        "DYJetsToLL_M50$", "TT(Lep|Semi)_pow", "TTHnobb_pow",

        ##main bkgs
        "T_tWch_noFullyHad", "TBar_tWch_noFullyHad",

        #"DYJetsToLL_M4to50_HT70to100," #Sample status = INVALID on DAS
        #"DYJetsToLL_M4to50_HT70to100_ext1", #Sample status = INVALID on DAS
        "DYJetsToLL_M4to50_HT100to200", 
        "DYJetsToLL_M4to50_HT100to200_ext1",
        "DYJetsToLL_M4to50_HT200to400",
        "DYJetsToLL_M4to50_HT200to400_ext1",
        "DYJetsToLL_M4to50_HT400to600",
        "DYJetsToLL_M4to50_HT400to600_ext1",
        "DYJetsToLL_M4to50_HT600toInf",

        "DYJetsToLL_M50_HT100to200", 
        "DYJetsToLL_M50_HT100to200_ext1",
        "DYJetsToLL_M50_HT200to400",
        "DYJetsToLL_M50_HT200to400_ext1",
        "DYJetsToLL_M50_HT400to600",
        "DYJetsToLL_M50_HT400to600_ext1",
        "DYJetsToLL_M50_HT600to800",
        "DYJetsToLL_M50_HT800to1200",
        "DYJetsToLL_M50_HT1200to2500",
        "DYJetsToLL_M50_HT2500toInf",

        "TTJets_DiLepton",

        #main VV
#        "WWTo2L2Nu",
#        "ZZTo2L2Nu",
        "VVTo2L2Nu",

        #fakesbkg
        "TTJets_SingleLeptonFromT",
        "TTJets_SingleLeptonFromTbar",

        "WJetsToLNu_HT100to200",
        "WJetsToLNu_HT200to400",
        "WJetsToLNu_HT400to600",
        "WJetsToLNu_HT600to800",
        "WJetsToLNu_HT800to1200",
        "WJetsToLNu_HT1200to2500",
        "WJetsToLNu_HT2500toInf",

        #rarebkg
        "WZTo3LNu_fxfx",
        "WWToLNuQQ",
        "WZTo1L1Nu2Q",
        "ZZTo4L",
        "WWW_ll", #_4F
        "WZZ",
        "WWZ", #_4F
        "ZZZ",
        "T_tch",
        "TBar_tch",
        "T_sch_lep",
        "T_tWch_noFullyHad",
        "WWTo2L2Nu_DPS_hpp",
        "TTWToLNu_fxfx",
        "TTZToLLNuNu_amc$",
        "TTZToLLNuNu_m1to10",
        "TTGJets",
        "TGJets_lep",

#more to be included
        "ZZTo2L2Q",
        "WpWpJJ",
#            "WZTo1L3Nu",
        "WGToLNuG",
        "ZGTo2LG",
        "WZTo2L2Q",
        "WW_DPS",
        "TZQToLL",
        "tWll",
        "WZTo3LNu_mllmin01",

        ##signal SUSY
        "SMS_TChiWZ",
        "SMS_TChiWZ_ext",
        "SMS_HiggsinoN2N1",
        "SMS_HiggsinoN2C1",
        "SMS_T2tt",
        "SMS_T2tt_ext",
        "SMS_T2bW",
        "SMS_T2bW_ext",
        "SMS_HiggsinoPMSSM",

    ])

    DatasetsAndTriggers.append( ("MET",         ["%s_v*"%x for x in ['HLT_PFMETNoMu120_PFMHTNoMu120_IDTight','HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60']] ) )
    DatasetsAndTriggers.append( ("DoubleMuon",  ["%s_v*"%x for x in ['HLT_DoubleMu3_DZ_PFMET50_PFMHT60','HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8']]) )

#    DatasetsAndTriggers.append( ("DoubleMuon", triggers["SOS_doublemulowMET"] + triggers["mumu_iso"] + triggers["3mu"]) )
#    DatasetsAndTriggers.append( ("MET",     triggers["SOS_highMET"] ) )
#    DatasetsAndTriggers.append( ("SingleElectron",  triggers["SOS_eleTnP"] ) )
#    DatasetsAndTriggers.append( ("SingleMuon",      triggers["SOS_muTnP"] ) )

elif year == 2016:
#    from CMGTools.RootTools.samples.triggers_13TeV_DATA2016 import all_triggers as triggers
    mcSamples = byCompName(mcSamples_, [

        ## low Mll Samples
        "ZZTo4L_M1toInf",
        "VVTo2L2Nu_M1toInf",
        "DYJetsToLL_M1to5_HT",

#        "DYJetsToLL_M50_LO", # for Tag and Probe studies
#        "DYJetsToLL_M10to50_LO$",

        ##main bkgs
        "T_tWch_noFullyHad", #extensions are to be included?
        "TBar_tWch_noFullyHad",

        "DYJetsToLL_M5to50_HT100to200",
        "DYJetsToLL_M5to50_HT100to200_ext",
        "DYJetsToLL_M5to50_HT200to400",
        "DYJetsToLL_M5to50_HT200to400_ext",
        "DYJetsToLL_M5to50_HT400to600",
        "DYJetsToLL_M5to50_HT400to600_ext",
        "DYJetsToLL_M5to50_HT600toInf",
        "DYJetsToLL_M5to50_HT600toInf_ext",


        "DYJetsToLL_M50_HT70to100", 
        "DYJetsToLL_M50_HT100to200",
        "DYJetsToLL_M50_HT100to200_ext",
        "DYJetsToLL_M50_HT200to400",
        "DYJetsToLL_M50_HT200to400_ext",
        "DYJetsToLL_M50_HT400to600",
        "DYJetsToLL_M50_HT400to600_ext",
        "DYJetsToLL_M50_HT600to800",
        "DYJetsToLL_M50_HT800to1200",
        "DYJetsToLL_M50_HT1200to2500",
        "DYJetsToLL_M50_HT2500toInf",

        "TTJets_DiLepton",

        #main VV
#        "WWTo2L2Nu",
#        "ZZTo2L2Nu",
        "VVTo2L2Nu",

        #fakesbkg
        "TTJets_SingleLeptonFromT",
        "TTJets_SingleLeptonFromTbar",

        "WJetsToLNu_HT70to100",
        "WJetsToLNu_HT100to200",
        "WJetsToLNu_HT100to200_ext",
        "WJetsToLNu_HT100to200_ext2",
        "WJetsToLNu_HT200to400",
        "WJetsToLNu_HT200to400_ext",
        "WJetsToLNu_HT200to400_ext2",
        "WJetsToLNu_HT400to600",
        "WJetsToLNu_HT400to600_ext",
        "WJetsToLNu_HT600to800",
        "WJetsToLNu_HT600to800_ext",
        "WJetsToLNu_HT800to1200",
        "WJetsToLNu_HT800to1200_ext",
        "WJetsToLNu_HT1200to2500",
        "WJetsToLNu_HT1200to2500_ext",
        "WJetsToLNu_HT2500toInf",
        "WJetsToLNu_HT2500toInf_ext",

        #rarebkg
        "WZTo3LNu_fxfx",
        "WWToLNuQQ",
        "WZTo1L1Nu2Q",
        "ZZTo4L",
        "WWW_ll", #_4F
        "WZZ",
        "WWZ", #why not _4F?
        "ZZZ",
        "T_tch",
        "TBar_tch",
        "T_sch_lep",
        "WWDoubleTo2L",
        "TTWToLNu",  #_fxfx
        "TTZToLLNuNu", #_amc
        "TTZToLLNuNu_m1to10",
        "TTGJets",
        "TGJets_lep",

#more to be included
        "ZZTo2L2Q", 
        "WpWpJJ",
#        "WZTo1L3Nu",
        "WGToLNuG_amcatnlo",
        "ZGTo2LG",
        "WZTo2L2Q",
        "TZQToLL",
        "tWll",
        "WZTo3LNu_mllmin01",

        ##signal SUSY
        "SMS_TChiWZ",
        "SMS_TChiWZ_ext",
        "SMS_HiggsinoN2N1",
        "SMS_HiggsinoN2C1",
        "SMS_T2tt",
        "SMS_T2tt_ext",
        "SMS_T2bW",
        "SMS_T2bW_ext",
        "SMS_HiggsinoPMSSM",

###        "DYJetsToLL_M50$", "TT(Lep|Semi)_pow" 
    ])
                                
    DatasetsAndTriggers.append( ("MET",         ["%s_v*"%x for x in ['HLT_DoubleMu3_PFMET50','HLT_PFMETNoMu120_PFMHTNoMu120_IDTight']] ) )
    DatasetsAndTriggers.append( ("DoubleMuon",  ["%s_v*"%x for x in ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ']]) )

#    DatasetsAndTriggers.append( ("DoubleMuon",      triggers["mumu_iso"] + triggers["3mu"]) )
#    DatasetsAndTriggers.append( ("MET",             triggers["SOS_doublemulowMET"] + triggers["SOS_highMET"] ) )
#    DatasetsAndTriggers.append( ("SingleElectron",  triggers["SOS_eleTnP"] ) )
#    DatasetsAndTriggers.append( ("SingleMuon",      triggers["SOS_muTnP"] ) )


mcTriggers = sum((trigs for (pd,trigs) in DatasetsAndTriggers), [])
if getCMGOption('applyTriggersInMC'):
    raise RuntimeError('Applying triggers in MC might bias the input PU distribution for the PU reweighting! If really sure comment out this line.')
    for comp in mcSamples:
        comp.triggers = mcTriggers

# make data
dataSamples = []; vetoTriggers = []
for pd, triggers in DatasetsAndTriggers:
    for comp in byCompName(allData, [pd]):
        comp.triggers = triggers[:]
        comp.vetoTriggers = vetoTriggers[:]
        dataSamples.append(comp)
    vetoTriggers += triggers[:]

selectedComponents = mcSamples + dataSamples
if getCMGOption('selectComponents'):
    if getCMGOption('selectComponents')=='MC':
        selectedComponents = mcSamples
    elif getCMGOption('selectComponents')=='DATA':
        selectedComponents = dataSamples
    else:
        selectedComponents = byCompName(selectedComponents, getCMGOption('selectComponents').split(","))
autoAAA(selectedComponents, quiet=not(getCMGOption("verboseAAA",False)), redirectorAAA="xrootd-cms.infn.it") # must be done before mergeExtensions
configureSplittingFromTime(mcSamples,500 if preprocessor else 10,10)
configureSplittingFromTime(dataSamples,160 if preprocessor else 10,10)
selectedComponents, _ = mergeExtensions(selectedComponents, verbose=True)

# create and set preprocessor if requested
if getCMGOption("nanoPreProcessor"):
    from CMGTools.Production.nanoAODPreprocessor import nanoAODPreprocessor
    suffix = ''
    if getCMGOption("FastSim"):
        suffix = 'fast'
    preproc_cfg = {2016: ("mc94X2016%s"%suffix,"data94X2016"),
                   2017: ("mc94Xv2%s"%suffix,"data94Xv2"),
                   2018: ("mc102X%s"%suffix,"data102X_ABC","data102X_D")}
    preproc_cmsswArea = "/afs/cern.ch/user/p/peruzzi/work/cmgtools_sos/CMSSW_10_2_18" #MODIFY ACCORDINGLY
    preproc_mc = nanoAODPreprocessor(cfg='%s/src/PhysicsTools/NanoAOD/test/%s_NANO.py'%(preproc_cmsswArea,preproc_cfg[year][0]),cmsswArea=preproc_cmsswArea,keepOutput=True)
    if year==2018:
        preproc_data_ABC = nanoAODPreprocessor(cfg='%s/src/PhysicsTools/NanoAOD/test/%s_NANO.py'%(preproc_cmsswArea,preproc_cfg[year][1]),cmsswArea=preproc_cmsswArea,keepOutput=True, injectTriggerFilter=True, injectJSON=True)
        preproc_data_D = nanoAODPreprocessor(cfg='%s/src/PhysicsTools/NanoAOD/test/%s_NANO.py'%(preproc_cmsswArea,preproc_cfg[year][2]),cmsswArea=preproc_cmsswArea,keepOutput=True, injectTriggerFilter=True, injectJSON=True)
        for comp in selectedComponents:
            if comp.isData:
                comp.preprocessor = preproc_data_D if '2018D' in comp.name else preproc_data_ABC
            else:
                comp.preprocessor = preproc_mc
    else:
        preproc_data = nanoAODPreprocessor(cfg='%s/src/PhysicsTools/NanoAOD/test/%s_NANO.py'%(preproc_cmsswArea,preproc_cfg[year][1]),cmsswArea=preproc_cmsswArea,keepOutput=True, injectTriggerFilter=True, injectJSON=True)
        for comp in selectedComponents:
            comp.preprocessor = preproc_data if comp.isData else preproc_mc
    if year==2017:
        preproc_mcv1 = nanoAODPreprocessor(cfg='%s/src/PhysicsTools/NanoAOD/test/%s_NANO.py'%(preproc_cmsswArea,"mc94Xv1%s"%suffix),cmsswArea=preproc_cmsswArea,keepOutput=True)
        for comp in selectedComponents:
            if comp.isMC and "Fall17MiniAODv2" not in comp.dataset:
                print("Warning: %s is MiniAOD v1, dataset %s" % (comp.name, comp.dataset))
                comp.preprocessor = preproc_mcv1

    if getCMGOption("fast"):
        for comp in selectedComponents:
            comp.preprocessor._cfgHasFilter = True
            comp.preprocessor._inlineCustomize = ("""
process.selectEl = cms.EDFilter("PATElectronRefSelector",
    src = cms.InputTag("slimmedElectrons"),
    cut = cms.string("pt > 4.5"),
    filter = cms.bool(False),
)
process.selectMu = cms.EDFilter("PATMuonRefSelector",
    src = cms.InputTag("slimmedMuons"),
    cut = cms.string("pt > 3"),
    filter = cms.bool(False),
)
process.skimNLeps = cms.EDFilter("PATLeptonCountFilter",
    electronSource = cms.InputTag("selectEl"),
    muonSource = cms.InputTag("selectMu"),
    tauSource = cms.InputTag(""),
    countElectrons = cms.bool(True),
    countMuons = cms.bool(True),
    countTaus = cms.bool(False),
    minNumber = cms.uint32(2),
    maxNumber = cms.uint32(999),
)
process.nanoAOD_step.insert(0, cms.Sequence(process.selectEl + process.selectMu + process.skimNLeps))
""")

cropToLumi(byCompName(selectedComponents,["T_","TBar_"]),100.)

# print summary of components to process
if getCMGOption("justSummary"): 
    printSummary(selectedComponents)
    sys.exit(0)

from CMGTools.NanoProc.tools.nanoAOD.susySOS_modules import *

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

modules = susySOS_sequence_step1
cut = susySOS_skim_cut
# Switch to Tag and Probe skimming/sequence
if getCMGOption("TnP"):
    collection = getCMGOption("TnPCollection", "None")
    if collection == "None":
        raise RuntimeError("You omitted the TnP collection to run on!")
    if collection != "Muon" and collection != "Electron":
        raise RuntimeError("Invalid TnP collection to run on: Should be either 'Muon' or 'Electron'!")
    modules = susySOS_sequence_TnP(year,collection)
    cut = susySOS_TnP_cut 

branchsel_in = os.environ['CMSSW_BASE']+"/src/CMGTools/NanoProc/python/tools/nanoAOD/branchsel_in.txt"
branchsel_out = None
compression = "ZLIB:3" #"LZ4:4" #"LZMA:9"

POSTPROCESSOR = PostProcessor(None, [], modules = modules,
        cut = cut, prefetch = True, longTermCache = True,
        branchsel = branchsel_in, outputbranchsel = branchsel_out, compression = compression)

test = getCMGOption("test")
if test == "94X-MC":
    TTLep_pow = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_mtop166p5_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )
    TTLep_pow.files = ["/afs/cern.ch/user/g/gpetrucc/cmg/NanoAOD_94X_TTLep.root"]
    lepSkim.requireSameSignPair = False
    lepSkim.minJets = 0
    lepSkim.minMET = 0
    lepSkim.prescaleFactor = 0
    selectedComponents = [TTLep_pow]
elif test == "94X-MC-miniAOD":
    TTLep_pow = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_mtop166p5_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )
    TTLep_pow.files = [ 'root://cms-xrd-global.cern.ch//store/mc/RunIIFall17MiniAOD/TTTo2L2Nu_mtop166p5_TuneCP5_PSweights_13TeV-powheg-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/70000/3CC234EB-44E0-E711-904F-FA163E0DF774.root' ]
    localfile = os.path.expandvars("/tmp/$USER/%s" % os.path.basename(TTLep_pow.files[0]))
    if os.path.exists(localfile): TTLep_pow.files = [ localfile ] 
    from CMGTools.Production.nanoAODPreprocessor import nanoAODPreprocessor
    TTLep_pow.preprocessor = nanoAODPreprocessor("/afs/cern.ch/work/g/gpetrucc/ttH/CMSSW_10_4_0/src/nanov4_NANO_cfg.py")
    selectedComponents = [TTLep_pow]
elif test == "102X-MC":
    TTLep_pow = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2), useAAA=True )
    TTLep_pow.files = TTLep_pow.files[:1]
    selectedComponents = [TTLep_pow]
elif test in ('2','3','3s'):
    doTestN(test, selectedComponents)
