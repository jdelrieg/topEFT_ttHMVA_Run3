# COMPONENT CREATOR
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()
import os 

# # QCD_Pt
# QCD_Pt80to120 = kreator.makeMCComponent("QCD_Pt80to120", "/QCD_Pt_80to120_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 2.345e+06*1.17805)
# QCD_Pt120to170 = kreator.makeMCComponent("QCD_Pt120to170", "/QCD_Pt_120to170_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 407800*1.15522)
# QCD_Pt170to300 = kreator.makeMCComponent("QCD_Pt170to300", "/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 103400*1.1342)
# QCD_Pt300to470 = kreator.makeMCComponent("QCD_Pt300to470",  "/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 6838*1.14405)
# QCD_Pt470to600 = kreator.makeMCComponent("QCD_Pt470to600",  "/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 551.1*1.17619)
# QCD_Pt470to600_ext1 = kreator.makeMCComponent("QCD_Pt470to600_ext1",  "/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext1-v1/NANOAODSIM", "CMS", ".*root", 551.1*1.17619)
# QCD_Pt600to800 = kreator.makeMCComponent("QCD_Pt600to800", "/QCD_Pt_600to800_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 156.4*1.19501)
# QCD_Pt800to1000 = kreator.makeMCComponent("QCD_Pt800to1000", "/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext1-v1/NANOAODSIM", "CMS", ".*root", 32.293)
# QCD_Pt1000to1400 = kreator.makeMCComponent("QCD_Pt1000to1400", "/QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 7.466*1.26149)
# QCD_Pt1400to1800 = kreator.makeMCComponent("QCD_Pt1400to1800", "/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 0.6481*1.30019)
# QCD_Pt1400to1800_ext1 = kreator.makeMCComponent("QCD_Pt1400to1800_ext1", "/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext1-v1/NANOAODSIM", "CMS", ".*root", 0.6481*1.30019)
# QCD_Pt1800to2400 = kreator.makeMCComponent("QCD_Pt1800to2400", "/QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 0.08741*1.31499)
# QCD_Pt1800to2400_ext1 = kreator.makeMCComponent("QCD_Pt1800to2400_ext1", "/QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext1-v1/NANOAODSIM", "CMS", ".*root", 0.08741*1.31499)
# QCD_Pt2400to3200 = kreator.makeMCComponent("QCD_Pt2400to3200", "/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 0.00522*1.30839)
# QCD_Pt2400to3200_ext1 = kreator.makeMCComponent("QCD_Pt2400to3200_ext1", "/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext1-v1/NANOAODSIM", "CMS", ".*root", 0.00522*1.30839)
# QCD_Pt3200toInf = kreator.makeMCComponent("QCD_Pt3200toInf", "/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 0.0001349*1.22643)
# QCD_Pt3200toInf_ext2 = kreator.makeMCComponent("QCD_Pt3200toInf_ext2", "/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext2-v1/NANOAODSIM", "CMS", ".*root", 0.0001349*1.22643)

# QCDPt = [
#     QCD_Pt80to120,
#     QCD_Pt120to170,
#     QCD_Pt170to300,
#     QCD_Pt300to470,
#     QCD_Pt470to600,
#     QCD_Pt470to600_ext1,
#     QCD_Pt600to800,
#     QCD_Pt800to1000,
#     QCD_Pt1000to1400,
#     QCD_Pt1400to1800,
#     QCD_Pt1400to1800_ext1,
#     QCD_Pt1800to2400,
#     QCD_Pt1800to2400_ext1,
#     QCD_Pt2400to3200,
#     QCD_Pt2400to3200_ext1,
#     QCD_Pt3200toInf,
#     QCD_Pt3200toInf_ext2
# ]


# # QCD HT bins (cross sections from McM)
# QCD_HT100to200 = kreator.makeMCComponent("QCD_HT100to200", "/QCD_HT100to200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 2.463e+07*1.13073)
# QCD_HT200to300 = kreator.makeMCComponent("QCD_HT200to300", "/QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 1.553e+06*1.1056)
# QCD_HT300to500 = kreator.makeMCComponent("QCD_HT300to500", "/QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 347500*1.01094)
# QCD_HT500to700 = kreator.makeMCComponent("QCD_HT500to700", "/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 29930*1.0568)
# QCD_HT700to1000 = kreator.makeMCComponent("QCD_HT700to1000", "/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 6370*1.06782)
# QCD_HT1000to1500 = kreator.makeMCComponent("QCD_HT1000to1500", "/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 1100*1.09636)
# QCD_HT1500to2000 = kreator.makeMCComponent("QCD_HT1500to2000", "/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 98.71)
# QCD_HT2000toInf = kreator.makeMCComponent("QCD_HT2000toInf", "/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 20.2)

# QCDHT = [
#     QCD_HT100to200,
#     QCD_HT200to300,
#     QCD_HT300to500,
#     QCD_HT500to700,
#     QCD_HT700to1000,
#     QCD_HT1000to1500,
#     QCD_HT1500to2000,
#     QCD_HT2000toInf,
# ]

# # QCD enriched (cross sections form genXSecAna)
#QCD_Mu15 = kreator.makeMyPrivateMCComponent("QCD_Mu15", "/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/sesanche-QCD_Mu15_UL17-c18b9e6b5256da8f58acfdd6c3d6d61d/USER", "PRIVATE", ".*root", 'phys03', 237800)
# QCD_Pt15to20_Mu5    = kreator.makeMCComponent("QCD_Pt15to20_Mu5"    , "/QCD_Pt-15to20_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS" , ".*root", 2.785e+06)
#QCD_Pt20to30_Mu5    = kreator.makeMyPrivateMCComponent("QCD_Pt20to30_Mu5"    , "/QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8/sesanche-QCD_Pt20to30_Mu5_UL17-c18b9e6b5256da8f58acfdd6c3d6d61d/USER", "PRIVATE" , ".*root", 'phys03', 2.49e+06)
#QCD_Pt30to50_Mu5    = kreator.makeMyPrivateMCComponent("QCD_Pt30to50_Mu5", "/QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8/sesanche-QCD_Pt30to50_Mu5_UL17-c18b9e6b5256da8f58acfdd6c3d6d61d/USER", "PRIVATE", ".*root", 'phys03', 1.364e+06)
QCD_Pt50to80_Mu5    = kreator.makeMCComponent("QCD_Pt50to80_Mu5"    , "/QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM" , "CMS" , ".*root", 377400)
QCD_Pt80to120_Mu5   = kreator.makeMCComponent("QCD_Pt80to120_Mu5"   , "/QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS" , ".*root", 88350)
QCD_Pt120to170_Mu5  = kreator.makeMCComponent("QCD_Pt120to170_Mu5"  , "/QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS" , ".*root", 21250)
QCD_Pt170to300_Mu5  = kreator.makeMCComponent("QCD_Pt170to300_Mu5", "/QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root", 6969)

# QCD_Pt300to470_Mu5  = kreator.makeMCComponent("QCD_Pt300to470_Mu5"  , "/QCD_Pt-300to470_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS" , ".*root", 619.5)
# QCD_Pt300to470_Mu5_ext3  = kreator.makeMCComponent("QCD_Pt300to470_Mu5_ext3"  , "/QCD_Pt-300to470_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext3-v1/NANOAODSIM", "CMS" , ".*root", 619.5)
# QCD_Pt470to600_Mu5  = kreator.makeMCComponent("QCD_Pt470to600_Mu5"  , "/QCD_Pt-470to600_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS" , ".*root", 58.9)
# QCD_Pt470to600_Mu5_ext1  = kreator.makeMCComponent("QCD_Pt470to600_Mu5_ext1"  , "/QCD_Pt-470to600_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext1-v1/NANOAODSIM", "CMS" , ".*root", 58.9)
# QCD_Pt600to800_Mu5  = kreator.makeMCComponent("QCD_Pt600to800_Mu5", "/QCD_Pt-600to800_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 18.36)
# QCD_Pt800to1000_Mu5 = kreator.makeMCComponent("QCD_Pt800to1000_Mu5" , "/QCD_Pt-800to1000_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext3-v1/NANOAODSIM", "CMS" , ".*root", 3.253)
# QCD_Pt1000toInf_Mu5 = kreator.makeMCComponent("QCD_Pt1000toInf_Mu5" , "/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS" , ".*root", 1.075)

QCD_Mu5s = [
#    QCD_Pt20to30_Mu5,
#    QCD_Pt30to50_Mu5,
#    QCD_Pt50to80_Mu5,
#    QCD_Pt80to120_Mu5,
#    QCD_Pt120to170_Mu5,
#    QCD_Pt170to300_Mu5,
# ]
    ]
QCD_Mus =[]# [ QCD_Mu15 ] + QCD_Mu5s

# # QCD EMEnr  (cross sections form genXSecAna)
# QCD_Pt15to20_EMEnriched   = kreator.makeMCComponent("QCD_Pt15to20_EMEnriched"  ,"/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext1-v1/NANOAODSIM"  , "CMS", ".*root",  1.33e+06)
#QCD_Pt20to30_EMEnriched   = kreator.makeMyPrivateMCComponent("QCD_Pt20to30_EMEnriched"  ,"/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/sesanche-Summer20UL17-3f0b140a720de1c801ff414923884f7b/USER"  , "PRIVATE", ".*root",  "phys03", 4.928e+06)

from CMGTools.Production.nanoAODPreprocessor import nanoAODPreprocessor
#QCD_Pt20to30_EMEnriched.preprocessor = nanoAODPreprocessor(cfg='/work/sesanche/FRs/CMSSW_10_6_27/src/NANO_Summer20UL17_Nanov2_MC_NANO.py',cmsswArea='/work/sesanche/FRs/CMSSW_10_6_27/src',keepOutput=True)



QCD_Pt30to50_EMEnriched   = kreator.makeMCComponent("QCD_Pt30to50_EMEnriched"  ,"/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM"  , "CMS", ".*root",  6.41e+06)
QCD_Pt50to80_EMEnriched   = kreator.makeMCComponent("QCD_Pt50to80_EMEnriched", "/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root",  1.986e+06)
QCD_Pt80to120_EMEnriched  = kreator.makeMCComponent("QCD_Pt80to120_EMEnriched" ,"/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM" , "CMS", ".*root",  370900)
QCD_Pt120to170_EMEnriched = kreator.makeMCComponent("QCD_Pt120to170_EMEnriched","/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root",  66760)
QCD_Pt170to300_EMEnriched = kreator.makeMCComponent("QCD_Pt170to300_EMEnriched","/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root",  16430)
QCD_Pt300toInf_EMEnriched = kreator.makeMCComponent("QCD_Pt300toInf_EMEnriched","/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root",  1101)

QCD_EMs = [
#     QCD_Pt15to20_EMEnriched,
    #QCD_Pt20to30_EMEnriched,
     QCD_Pt30to50_EMEnriched,
     QCD_Pt50to80_EMEnriched,
     QCD_Pt80to120_EMEnriched,
     QCD_Pt120to170_EMEnriched,
     QCD_Pt170to300_EMEnriched,
     QCD_Pt300toInf_EMEnriched
 ]

# #QCD_Pt15to20_bcToE   = kreator.makeMCComponent("QCD_Pt15to20_bcToE",   "/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v11-v1/MINIAODSIM"  , "CMS", ".*root", 187000)
#QCD_Pt20to30_bcToE   = kreator.makeMyPrivateMCComponent("QCD_Pt20to30_bcToE",   "/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/sesanche-QCD_Pt20to30_bcToE_UL17-c18b9e6b5256da8f58acfdd6c3d6d61d/USER"  , "PRIVATE", ".*root", 'phys03',313500)
QCD_Pt30to80_bcToE   = kreator.makeMCComponent("QCD_Pt30to80_bcToE",   "/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"  , "CMS", ".*root", 361500)
QCD_Pt80to170_bcToE  = kreator.makeMCComponent("QCD_Pt80to170_bcToE",  "/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM" , "CMS", ".*root", 33770)
QCD_Pt170to250_bcToE = kreator.makeMCComponent("QCD_Pt170to250_bcToE", "/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 2126)
# #QCD_Pt250toInf_bcToE = kreator.makeMCComponent("QCD_Pt250toInf_bcToE", "/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v11-v1/MINIAODSIM", "CMS", ".*root", 563.1)

QCD_bcToE = [
    # #   QCD_Pt15to20_bcToE,
    #QCD_Pt20to30_bcToE,
    QCD_Pt30to80_bcToE,
    QCD_Pt80to170_bcToE,
    QCD_Pt170to250_bcToE,
# #   QCD_Pt250toInf_bcToE,
]

# # ====== W + Jets ======
WJetsToLNu_LO = kreator.makeMCComponent("WJetsToLNu_LO","/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 3* 20508.9)
                                                          
# ## LO XSec from genXSecAna times NNLO/LO XSec for inclusive W+jets
W1JetsToLNu_LO = kreator.makeMCComponent("W1JetsToLNu_LO","/W1JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 8123*1.17)
W2JetsToLNu_LO = kreator.makeMCComponent("W2JetsToLNu_LO","/W2JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 2785*1.17)
W3JetsToLNu_LO = kreator.makeMCComponent("W3JetsToLNu_LO","/W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 993.4*1.17)
W4JetsToLNu_LO = kreator.makeMCComponent("W4JetsToLNu_LO","/W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root", 542.4*1.17)

# XSec from genXSecAna
WJetsToLNu_012JetsNLO_34JetsLO = kreator.makeMCComponent("WJetsToLNu_012JetsNLO_34JetsLO","/WJetsToLNu_012JetsNLO_34JetsLO_EWNLOcorr_13TeV-sherpa/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM",  "CMS", ".*root", 6.228e+04)

# ### W+jets HT-binned
WJetsToLNu_HT100to200 = kreator.makeMCComponent("WJetsToLNu_HT100to200", "/WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root",1395*1.17) 
WJetsToLNu_HT200to400 = kreator.makeMCComponent("WJetsToLNu_HT200to400", "/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root",408.7*1.17) 
WJetsToLNu_HT400to600      = kreator.makeMCComponent("WJetsToLNu_HT400to600", "/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root",57.52*1.17) 
WJetsToLNu_HT600to800      = kreator.makeMCComponent("WJetsToLNu_HT600to800",     "/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root",12.78*1.17) 
#WJetsToLNu_HT800to1200     = kreator.makeMCComponent("WJetsToLNu_HT800to1200",    "/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root",5.246*1.17) 
WJetsToLNu_HT1200to2500    = kreator.makeMCComponent("WJetsToLNu_HT1200to2500",   "/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root",1.071*1.17) 
WJetsToLNu_HT2500toInf = kreator.makeMCComponent("WJetsToLNu_HT2500toInf", "/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root",0.00819*1.17) 

WJetsToLNuHT = [
    WJetsToLNu_HT100to200,
    WJetsToLNu_HT200to400,
    WJetsToLNu_HT400to600,
    WJetsToLNu_HT600to800,
    #WJetsToLNu_HT800to1200,
    WJetsToLNu_HT1200to2500,
    WJetsToLNu_HT2500toInf,
]

Ws = [ 
    WJetsToLNu_LO,
    W1JetsToLNu_LO,
    W2JetsToLNu_LO,
    W3JetsToLNu_LO,
    W4JetsToLNu_LO,
    WJetsToLNu_012JetsNLO_34JetsLO,
]+WJetsToLNuHT



# # ====== Z + Jets ======
# ## New FEWZ cross section 1921.8 from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
DYJetsToLL_M50 = kreator.makeMCComponent("DYJetsToLL_M50", "/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root", 1921.8*3, fracNegWeights=0.16)
DYJetsToLL_M50_LO =  kreator.makeMCComponent("DYJetsToLL_M50_LO", "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 1921.8*3)
DYJetsToLL_M50_LO_ext =  kreator.makeMCComponent("DYJetsToLL_M50_LO_ext", "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9_ext1-v1/NANOAODSIM", "CMS", ".*root", 1921.8*3)

DYJetsToLL_M10to50_LO =  kreator.makeMCComponent("DYJetsToLL_M10to50_LO", "/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 15810)

DYJets = [
    DYJetsToLL_M50,
    #DYJetsToLL_M50_LO,DYJetsToLL_M50_LO_ext,
    DYJetsToLL_M10to50_LO,
]



# ## cross sections from genXS analyzer
# DY1JetsToLL_M50_LO     = kreator.makeMCComponent("DY1JetsToLL_M50_LO",     "/DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM",      "CMS", ".*root", 878)
# DY2JetsToLL_M50_LO     = kreator.makeMCComponent("DY2JetsToLL_M50_LO",     "/DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM",      "CMS", ".*root", 307)
# DY3JetsToLL_M50_LO     = kreator.makeMCComponent("DY3JetsToLL_M50_LO",     "/DY3JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM",      "CMS", ".*root", 112)
# DY4JetsToLL_M50_LO     = kreator.makeMCComponent("DY4JetsToLL_M50_LO",     "/DY4JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM",      "CMS", ".*root", 44.2)
# DYNJetsToLL = [ 
#     DY1JetsToLL_M50_LO,
#     DY2JetsToLL_M50_LO,
#     DY3JetsToLL_M50_LO,
#     DY4JetsToLL_M50_LO,
# ]

# ## Cross sections from getXSecAnalyzer
# DYJetsToLL_M4to50_HT70to100  = kreator.makeMCComponent("DYJetsToLL_M4to50_HT70to100",      "/DYJetsToLL_M-4to50_HT-70to100_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM",        "CMS", ".*root", 145.4)
# DYJetsToLL_M4to50_HT100to200 = kreator.makeMCComponent("DYJetsToLL_M4to50_HT100to200",      "/DYJetsToLL_M-4to50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM",      "CMS", ".*root", 202.8)
# DYJetsToLL_M4to50_HT200to400 = kreator.makeMCComponent("DYJetsToLL_M4to50_HT200to400",      "/DYJetsToLL_M-4to50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM",      "CMS", ".*root", 53.7)
# DYJetsToLL_M4to50_HT400to600 = kreator.makeMCComponent("DYJetsToLL_M4to50_HT400to600",      "/DYJetsToLL_M-4to50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM",      "CMS", ".*root", 5.66)
# DYJetsToLL_M4to50_HT600toInf = kreator.makeMCComponent("DYJetsToLL_M4to50_HT600toInf",      "/DYJetsToLL_M-4to50_HT-600toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM",      "CMS", ".*root", 1.852)
# DYJetsToLLM4to50HT = [
#     DYJetsToLL_M4to50_HT70to100,
#     DYJetsToLL_M4to50_HT100to200,
#     DYJetsToLL_M4to50_HT200to400,
#     DYJetsToLL_M4to50_HT400to600,
#     DYJetsToLL_M4to50_HT600toInf,
# ]

# ## Cross sections from getXSecAnalyzer times k-factor 1.08 from ratio of FEWZ to inclusive DYJetsToLL_M50_LO
# DYJetsToLL_M50_HT100to200      = kreator.makeMCComponent("DYJetsToLL_M50_HT100to200",      "/DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM",       "CMS", ".*root", 161.1*1.08)
# DYJetsToLL_M50_HT200to400      = kreator.makeMCComponent("DYJetsToLL_M50_HT200to400",      "/DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM",       "CMS", ".*root", 49.32*1.08)
# DYJetsToLL_M50_HT400to600      = kreator.makeMCComponent("DYJetsToLL_M50_HT400to600",      "/DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM",       "CMS", ".*root", 7.021*1.08)
# DYJetsToLL_M50_HT400to600_ext2 = kreator.makeMCComponent("DYJetsToLL_M50_HT400to600_ext2", "/DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext2-v1/NANOAODSIM",  "CMS", ".*root", 7.021*1.08)
# DYJetsToLL_M50_HT600to800      = kreator.makeMCComponent("DYJetsToLL_M50_HT600to800",      "/DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM",       "CMS", ".*root", 1.743*1.08 )
# DYJetsToLL_M50_HT800to1200     = kreator.makeMCComponent("DYJetsToLL_M50_HT800to1200",     "/DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM",      "CMS", ".*root", 0.8082*1.08 )
# #DYJetsToLL_M50_HT1200to2500    = kreator.makeMCComponent("DYJetsToLL_M50_HT1200to2500",    "/DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v11-v1/MINIAODSIM",     "CMS", ".*root", 0.1925*1.08 )
# DYJetsToLL_M50_HT2500toInf     = kreator.makeMCComponent("DYJetsToLL_M50_HT2500toInf",     "/DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM",      "CMS", ".*root", 0.003486*1.08 )

# DYJetsToLLM50HT = [
#     DYJetsToLL_M50_HT100to200,
#     DYJetsToLL_M50_HT200to400,
#     DYJetsToLL_M50_HT400to600,     DYJetsToLL_M50_HT400to600_ext2,
#     DYJetsToLL_M50_HT600to800,
#     DYJetsToLL_M50_HT800to1200,
#     #DYJetsToLL_M50_HT1200to2500,
#     DYJetsToLL_M50_HT2500toInf,
# ]

DYs = DYJets # + DYNJetsToLL + DYJetsToLLM4to50HT + DYJetsToLLM50HT


# # VJetsQQ HT-binned. Cross sections form genXSAnalyzer (on the corresponding miniAOD)
# WJetsToQQ_HT400to600 = kreator.makeMCComponent("WJetsToQQ_HT400to600", "/WJetsToQQ_HT400to600_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 315.)  
 # WJetsToQQ_HT600to800 = kreator.makeMCComponent("WJetsToQQ_HT600to800", "/WJetsToQQ_HT600to800_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 61.6) 
# WJetsToQQ_HT800toInf = kreator.makeMCComponent("WJetsToQQ_HT800toInf", "/WJetsToQQ_HT-800toInf_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM","CMS", ".*root", 34.97)
# ZJetsToQQ_HT400to600 = kreator.makeMCComponent("ZJetsToQQ_HT400to600", "/ZJetsToQQ_HT400to600_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 145.5)
# ZJetsToQQ_HT600to800 = kreator.makeMCComponent("ZJetsToQQ_HT600to800", "/ZJetsToQQ_HT600to800_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 34.15) 
# ZJetsToQQ_HT800toInf = kreator.makeMCComponent("ZJetsToQQ_HT800toInf", "/ZJetsToQQ_HT-800toInf_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM","CMS", ".*root", 18.6) 

# VJetsQQHT = [
#     WJetsToQQ_HT400to600,
#     WJetsToQQ_HT600to800,
#     WJetsToQQ_HT800toInf,
#     ZJetsToQQ_HT400to600,
#     ZJetsToQQ_HT600to800,
#     ZJetsToQQ_HT800toInf
# ]


# # ====== TT INCLUSIVE =====

# # TTbar cross section: NNLO, https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO (172.5)
# TTJets = kreator.makeMCComponent("TTJets", "/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext1-v1/NANOAODSIM", "CMS", ".*root", 831.76, fracNegWeights=0.319)

TTLep_pow  = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )
# TTHad_pow  = kreator.makeMCComponent("TTHad_pow", "/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 831.76*((1-3*0.108)**2) )
TTSemi_pow = kreator.makeMCComponent("TTSemi_pow", "/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 831.76*2*(3*0.108)*(1-3*0.108) )

# TTJets_SingleLeptonFromT = kreator.makeMCComponent("TTJets_SingleLeptonFromT", "/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 831.76*(3*0.108)*(1-3*0.108))
# TTJets_SingleLeptonFromTbar = kreator.makeMCComponent("TTJets_SingleLeptonFromTbar", "/TTJets_SingleLeptFromTbar_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 831.76*(3*0.108)*(1-3*0.108) )
# TTJets_DiLepton = kreator.makeMCComponent("TTJets_DiLepton", "/TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )


TTs = [ #TTJets, 
        TTLep_pow,
        #TTHad_pow,
        TTSemi_pow,
        #TTJets_SingleLeptonFromT, TTJets_SingleLeptonFromTbar,
        #TTJets_DiLepton
]

# # ====== SINGLE TOP ======
# # Single top cross sections: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
# T_sch_lep = kreator.makeMCComponent("T_sch_lep", "/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext1-v2/NANOAODSIM", "CMS", ".*root", (7.20+4.16)*0.108*3, fracNegWeights=0.188)

T_tch = kreator.makeMCComponent("T_tch", "/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM",           "CMS", ".*root", 136.02) # inclusive sample
TBar_tch = kreator.makeMCComponent("TBar_tch", "/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 80.95) # inclusive sample

T_tWch_noFullyHad    = kreator.makeMCComponent("T_tWch_noFullyHad",    "/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM",     "CMS", ".*root",19.55)
TBar_tWch_noFullyHad = kreator.makeMCComponent("TBar_tWch_noFullyHad", "/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root",19.55)

Ts = [
#     T_sch_lep,
     T_tch, TBar_tch,
     T_tWch_noFullyHad, TBar_tWch_noFullyHad
]

# # ====== T(T) + BOSON =====

TTGJets = kreator.makeMCComponent("TTGJets", "/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 4.09, fracNegWeights=0.306)

TGJets_lep = kreator.makeMCComponent("TGJets_lep", "/TGJets_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 1.018, fracNegWeights=0.411)

TTWToLNu_fxfx = kreator.makeMCComponent("TTWToLNu_fxfx", "/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 0.2043, fracNegWeights=0.227)
TTW_LO = kreator.makeMCComponent("TTW_LO", "/ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root",  0.6105 )
TTWJetsToLNu_EWK_5f_NLO = kreator.makeMCComponent("TTWJetsToLNu_EWK_5f_NLO","/ttWJetsToLNu_5f_EWK_TuneCP5_13TeV_amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 0.0162562 )

TTZToLLNuNu_amc = kreator.makeMCComponent("TTZToLLNuNu_amc", "/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 0.281, fracNegWeights=0.264)
TTZ_LO = kreator.makeMCComponent("TTZ_LO", "/ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root",  0.5297/0.692)
TTLL_CPV  = kreator.makeMCComponent("TTLL_CPV", "/TTLL-AtLeastOneTtoL-CPV_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root", 0.113559537782*(1-0.7*0.7))
TZQ_CPV   = kreator.makeMCComponent("TZQ_CPV", "/TZQB-ZtoLL-TtoL-CPV_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root", 0.07358*0.3)

TTZToLLNuNu_m1to10  = kreator.makeMCComponent("TTZToLLNuNu_m1to10","/TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 0.082, fracNegWeights=0.236)

TTHnobb_pow = kreator.makeMCComponent("TTHnobb_pow", "/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root", 0.5071*(1-0.582))
TTHnobb_fxfx = kreator.makeMCComponent("TTHnobb_fxfx", "/ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 0.5071*(1-0.582), fracNegWeights=0.344)

THQ_ctcvcp = kreator.makeMCComponent("THQ_ctcvcp", "/THQ_ctcvcp_4f_Hincl_TuneCP5_13TeV_madgraph_pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root",  0.7927)
THW_ctcvcp = kreator.makeMCComponent("THW_ctcvcp", "/THW_ctcvcp_5f_Hincl_TuneCP5_13TeV_madgraph_pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root",  0.1472)
TTH_ctcvcp = kreator.makeMCComponent("TTH_ctcvcp", "/TTH_ctcvcp_4f_Hincl_TuneCP5_13TeV_madgraph_pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 0.5071)

TZQToLL  = kreator.makeMCComponent("TZQToLL","/tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 0.07358, fracNegWeights=0.367)

tWll_thad_wlep  = kreator.makeMCComponent("tWll_thad_wlep","/TWZToLL_thad_Wlept_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 0.003004) 
tWll_tlep_whad  = kreator.makeMCComponent("tWll_tlep_whad","/TWZToLL_tlept_Whad_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 0.003004) 
tWll_tlep_wlep  = kreator.makeMCComponent("tWll_tlep_wlep","/TWZToLL_tlept_Wlept_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 0.0015) 


TTXs = [ TTGJets, TGJets_lep,
         TTWToLNu_fxfx, TTW_LO, 
         TTZToLLNuNu_amc, TTZ_LO, TTZToLLNuNu_m1to10,
         TZQToLL,THQ_ctcvcp, THW_ctcvcp, TTH_ctcvcp, # tWll, 
         TTHnobb_pow, TTHnobb_fxfx,
         TTWJetsToLNu_EWK_5f_NLO,
         tWll_thad_wlep, tWll_tlep_whad, tWll_tlep_wlep,
]

# # ====== TT + DIBOSON, 4-top =====

TTTT = kreator.makeMCComponent("TTTT", "/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root", 0.009103, fracNegWeights=0.311)
TTWH = kreator.makeMCComponent("TTWH", "/TTWH_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root", 0.00114)
TTZH = kreator.makeMCComponent("TTZH", "/TTZH_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root", 0.001138)
TTWW = kreator.makeMCComponent("TTWW", "/TTWW_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 0.011500) # NLO xsec from YR4
TTHH = kreator.makeMCComponent("TTHH", "/TTHH_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root", 0.0006666)

TTTJ = kreator.makeMCComponent("TTTJ", "/TTTJ_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root", 0.0003987)
TTTW = kreator.makeMCComponent("TTTW", "/TTTW_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root", 0.0007273)

TTXXs = [ TTTT, TTWH, TTZH, TTWW, TTHH, TTTJ, TTTW ]

# # ===  DI-BOSONS

# # cross section from https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns#Diboson
WW = kreator.makeMCComponent("WW", "/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 63.21 * 1.82)
WZ = kreator.makeMCComponent("WZ", "/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 47.13)
ZZ = kreator.makeMCComponent("ZZ", "/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 16.523)

WWTo2L2Nu = kreator.makeMCComponent("WWTo2L2Nu", "/WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root", 10.481 )
# WWToLNuQQ = kreator.makeMCComponent("WWToLNuQQ", "/WWToLNuQQ_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 43.53 )
# WW_DPS = kreator.makeMCComponent("WW_DPS", "/WW_DoubleScattering_13TeV-pythia8_TuneCP5/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext1-v1/NANOAODSIM", "CMS", ".*root", 1.921)
# WpWpJJ = kreator.makeMCComponent("WpWpJJ", "/WpWpJJ_EWK-QCD_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 0.04914) # XS from genXSecAna 

WZTo3LNu_fxfx = kreator.makeMCComponent("WZTo3LNu_fxfx", "/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root", 5.28, fracNegWeights=0.189 )
WZTo3LNu_pow = kreator.makeMCComponent("WZTo3LNu_pow", "/WZTo3LNu_mllmin4p0_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root", 4.664*1.19 ) # powheg times k-factor
# WZTo1L1Nu2Q = kreator.makeMCComponent("WZTo1L1Nu2Q", "/WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root",  10.71, fracNegWeights=0.204 )

ZZTo4L = kreator.makeMCComponent("ZZTo4L", "/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root", 1.256)
ZZTo2L2Nu = kreator.makeMCComponent("ZZTo2L2Nu", "/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 0.564)

WGToLNuG = kreator.makeMCComponent("WGToLNuG", "/WGToLNuG_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 466.1)
ZGTo2LG =  kreator.makeMCComponent("ZGTo2LG", "/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 55.78)

GluGluToContinToZZTo4e      =  kreator.makeMCComponent("GluGluToContinToZZTo4e", "/GluGluToContinToZZTo4e_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM",  "CMS", ".*root", 0.00159*1.7) # generator cross section times 1.7 k-factor (SMP-19-001, AN-2019/004)
GluGluToContinToZZTo4mu     =  kreator.makeMCComponent("GluGluToContinToZZTo4mu", "/GluGluToContinToZZTo4mu_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM",  "CMS", ".*root", 0.00159*1.7) # generator cross section times 1.7 k-factor (SMP-19-001, AN-2019/004)
GluGluToContinToZZTo4tau    =  kreator.makeMCComponent("GluGluToContinToZZTo4tau", "/GluGluToContinToZZTo4tau_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM",  "CMS", ".*root", 0.00159*1.7) # generator cross section times 1.7 k-factor (SMP-19-001, AN-2019/004)
GluGluToContinToZZTo2e2mu   =  kreator.makeMCComponent("GluGluToContinToZZTo2e2mu", "/GluGluToContinToZZTo2e2mu_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM",  "CMS", ".*root", 0.00319*1.7) # generator cross section times 1.7 k-factor (SMP-19-001, AN-2019/004)
GluGluToContinToZZTo2e2tau  =  kreator.makeMCComponent("GluGluToContinToZZTo2e2tau", "/GluGluToContinToZZTo2e2tau_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM",  "CMS", ".*root", 0.00319*1.7) # generator cross section times 1.7 k-factor (SMP-19-001, AN-2019/004)
GluGluToContinToZZTo2mu2tau =  kreator.makeMCComponent("GluGluToContinToZZTo2mu2tau", "/GluGluToContinToZZTo2mu2tau_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM",  "CMS", ".*root", 0.00319*1.7) # generator cross section times 1.7 k-factor (SMP-19-001, AN-2019/004)
WLLJJ_WToLNu_EWK = kreator.makeMCComponent("WLLJJ_WToLNu_EWK","/WLLJJ_WToLNu_EWK_TuneCP5_13TeV_madgraph-madspin-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM",  "CMS", ".*root", 0.01628) # AN-19-156



DiBosons = [
     WW,
     WZ,
     ZZ,
     WWTo2L2Nu,
    WZTo3LNu_pow,
#     WWToLNuQQ,
#     WW_DPS,
#     WpWpJJ,
#     WZ,
     WZTo3LNu_fxfx,
#     WZTo1L1Nu2Q,
#     ZZ,
     ZZTo4L,
     ZZTo2L2Nu,
    WGToLNuG,
    ZGTo2LG ,
    GluGluToContinToZZTo4e      ,
    GluGluToContinToZZTo4mu     ,
    GluGluToContinToZZTo4tau    ,
    GluGluToContinToZZTo2e2mu   ,
    GluGluToContinToZZTo2e2tau  ,
    GluGluToContinToZZTo2mu2tau ,
    WLLJJ_WToLNu_EWK,
]

# # ===  TRI-BOSONS

# # xsec from GenXSecAnalyzer
WWW        = kreator.makeMCComponent("WWW",        "/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 0.2086, fracNegWeights=0.063)
# WWW_ll = kreator.makeMCComponent("WWW_ll", "/WWW_4F_DiLeptonFilter_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 0.007201, fracNegWeights=0.063) # xs from genXSecAna
WWZ        = kreator.makeMCComponent("WWZ",        "/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root",  0.1651, fracNegWeights=0.06 ) 
WZG        = kreator.makeMCComponent("WZG",        "/WZG_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 0.04345, fracNegWeights=0.078)
WZZ        = kreator.makeMCComponent("WZZ",        "/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 0.05565, fracNegWeights=0.060)
WZZ_ext    = kreator.makeMCComponent("WZZ_ext",    "/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9_ext1-v2/NANOAODSIM", "CMS", ".*root", 0.05565, fracNegWeights=0.060)
ZZZ        = kreator.makeMCComponent("ZZZ",        "/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 0.01398, fracNegWeights=0.060)
ZZZ_ext    = kreator.makeMCComponent("ZZZ_ext",    "/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9_ext1-v2/NANOAODSIM", "CMS", ".*root", 0.01398, fracNegWeights=0.060)



TriBosons = [
    WWW,
#     WWW_ll,
    WWZ,
    WZG,
    WZZ, WZZ_ext,
    ZZZ, ZZZ_ext,

]

# # other Higgs processes

GGHZZ4L = kreator.makeMCComponent("GGHZZ4L", "/GluGluHToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root", 0.01212)
# # note: genXSecAna is incorrect because it doesn't know of the forced decay in pythia8. for the DiLeptonFilter sample, we take the filter efficiency from the ratio of the genXSecAna reports for the two samples
VHToNonbb = kreator.makeMCComponent("VHToNonbb", "/VHToNonbb_M125_TuneCP5_13TeV-amcatnloFXFX_madspin_pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root", 0.9561, fracNegWeights=0.26) 
# #VHToNonbb_ll = kreator.makeMCComponent("VHToNonbb_ll", "/VHToNonbb_M125_DiLeptonFilter_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/-FIXME-MISSING-/NANOAODSIM", "CMS", ".*root", 0.9561*0.08878/2.509, fracNegWeights=0.26) 

ZHToTauTau = kreator.makeMCComponent("ZHToTauTau", "/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 0.05544)
Higgs = [
    # GGHZZ4L,
    VHToNonbb,
    #VHToNonbb_ll,
]


# # ----------------------------- summary ----------------------------------------


mcSamples =  Ws + DYs +  TTs + Ts + TTXs + TTXXs + DiBosons + TriBosons + Higgs + QCD_bcToE + QCD_EMs + QCD_Mus 



samples = mcSamples

# ---------------------------------------------------------------------

if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples, localobjs=locals())
