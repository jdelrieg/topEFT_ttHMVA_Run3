from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
import os
kreator = ComponentCreator()
WZto3LNu                        = kreator.makeMCComponent("WZto3LNu", "/WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 5.31)
ZZto4L                          = kreator.makeMCComponent("ZZto4L", "/ZZto4L_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 1.65)
ZZto4L_ext                      = kreator.makeMCComponent("ZZto4L_ext", "/ZZto4L_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6_ext1-v2/NANOAODSIM", "CMS", ".*root", 1.65)
GluGlutoContinto2Zto4E          = kreator.makeMCComponent("GluGlutoContinto2Zto4E", "/GluGlutoContinto2Zto4E_TuneCP5_13p6TeV_mcfm-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 0.00306)
GluGlutoContinto2Zto4Mu         = kreator.makeMCComponent("GluGlutoContinto2Zto4Mu", "/GluGlutoContinto2Zto4Mu_TuneCP5_13p6TeV_mcfm-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 0.00306)
GluGlutoContinto2Zto4Tau        = kreator.makeMCComponent("GluGlutoContinto2Zto4Tau", "/GluGlutoContinto2Zto4Tau_TuneCP5_13p6TeV_mcfm-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 0.00306)
TTG_1Jets_PTG_10to100           = kreator.makeMCComponent("TTG_1Jets_PTG_10to100", "/TTG-1Jets_PTG-10to100_TuneCP5_13p6TeV_amcatnloFXFXold-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v4/NANOAODSIM", "CMS", ".*root", 4.216)
TTG_1Jets_PTG_100to200          = kreator.makeMCComponent("TTG_1Jets_PTG_100to200", "/TTG-1Jets_PTG-100to200_TuneCP5_13p6TeV_amcatnloFXFXold-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v3/NANOAODSIM", "CMS", ".*root", 0.411)
TTG_1Jets_PTG_200               = kreator.makeMCComponent("TTG_1Jets_PTG_200", "/TTG-1Jets_PTG-200_TuneCP5_13p6TeV_amcatnloFXFXold-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v3/NANOAODSIM", "CMS", ".*root", 0.128)
TTHtoNon2B                      = kreator.makeMCComponent("TTHtoNon2B", "/TTHtoNon2B_M-125_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 0.25)
TTLL_MLL_50                     = kreator.makeMCComponent("TTLL_MLL_50", "/TTLL_MLL-50_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 0.08646)
TTLL_CPV                        = kreator.makeMCComponent("TTLL_CPV", "/TTLL-AtLeastOneTtoL-CPV_TuneCP5_13p6TeV_madgraph-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 0.113559537782*(1-0.7*0.7))
TZQ_CPV                         = kreator.makeMCComponent("TZQ_CPV", "/TZQB-ZtoLL-TtoL-CPV_TuneCP5_13p6TeV_madgraph-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v3/NANOAODSIM", "CMS", ".*root", 0.07358*0.3)

TTLL_MLL_4to50                  = kreator.makeMCComponent("TTLL_MLL_4to50", "/TTLL_MLL-4to50_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 0.03949)
TTLNu_1Jets                     = kreator.makeMCComponent("TTLNu_1Jets", "/TTLNu-1Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v4/NANOAODSIM", "CMS", ".*root", 0.25)
TZQB                            = kreator.makeMCComponent("TZQB", "/TZQB-Zto2L-4FS_MLL-30_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 0.07968)
WZZ                             = kreator.makeMCComponent("WZZ", "/WZZ_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 0.06206)
WWW_4F                          = kreator.makeMCComponent("WWW_4F", "/WWW_4F_TuneCP5_13p6TeV_amcatnlo-madspin-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 1)
WWZ_4F                          = kreator.makeMCComponent("WWZ_4F", "/WWZ_4F_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 0.1851)
ZZZ                             = kreator.makeMCComponent("ZZZ", "/ZZZ_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 0.01591)
TTto2L2Nu                       = kreator.makeMCComponent("TTto2L2Nu", "/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 97.4488)
TTto2L2Nu_ext                   = kreator.makeMCComponent("TTto2L2Nu_ext", "/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6_ext1-v2/NANOAODSIM", "CMS", ".*root", 97.4488)
TTtoLNu2Q                       = kreator.makeMCComponent("TTtoLNu2Q", "/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 403.25)
TTtoLNu2Q_ext                   = kreator.makeMCComponent("TTtoLNu2Q_ext", "/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6_ext1-v2/NANOAODSIM", "CMS", ".*root", 403.25)
TbarWplusto2L2Nu                = kreator.makeMCComponent("TbarWplusto2L2Nu", "/TbarWplusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 23.8979)
TbarWplusto2L2Nu_ext            = kreator.makeMCComponent("TbarWplusto2L2Nu_ext", "/TbarWplusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6_ext1-v2/NANOAODSIM", "CMS", ".*root", 23.8979)
TWminusto2L2Nu                  = kreator.makeMCComponent("TWminusto2L2Nu", "/TWminusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 23.8979)
TWminusto2L2Nu_ext              = kreator.makeMCComponent("TWminusto2L2Nu_ext", "/TWminusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6_ext1-v2/NANOAODSIM", "CMS", ".*root", 23.8979)
WZto2L2Q                        = kreator.makeMCComponent("WZto2L2Q", "/WZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 1)
WZto2L2Q_ext                    = kreator.makeMCComponent("WZto2L2Q_ext", "/WZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6_ext1-v2/NANOAODSIM", "CMS", ".*root", 1)
WWto2L2Nu                       = kreator.makeMCComponent("WWto2L2Nu", "/WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 12.98)
WWto2L2Nu_ext                   = kreator.makeMCComponent("WWto2L2Nu_ext", "/WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6_ext1-v2/NANOAODSIM", "CMS", ".*root", 12.98)
ZZto2L2Nu                       = kreator.makeMCComponent("ZZto2L2Nu", "/ZZto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 1.19)
ZZto2L2Nu_ext                   = kreator.makeMCComponent("ZZto2L2Nu_ext", "/ZZto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6_ext1-v2/NANOAODSIM", "CMS", ".*root", 1.19)
ZZto2L2Q                        = kreator.makeMCComponent("ZZto2L2Q", "/ZZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 8.08)
ZZto2L2Q_ext                    = kreator.makeMCComponent("ZZto2L2Q_ext", "/ZZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6_ext1-v2/NANOAODSIM", "CMS", ".*root", 8.08)
DYto2L_2Jets_MLL_50             = kreator.makeMCComponent("DYto2L_2Jets_MLL_50", "/DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 6345.99)
DYto2L_2Jets_MLL_50_ext         = kreator.makeMCComponent("DYto2L_2Jets_MLL_50_ext", "/DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6_ext1-v1/NANOAODSIM", "CMS", ".*root", 6345.99)
DYto2L_2Jets_MLL_10to50         = kreator.makeMCComponent("DYto2L_2Jets_MLL_10to50", "/DYto2L-2Jets_MLL-10to50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 19982.5)
DYto2L_2Jets_MLL_10to50_ext     = kreator.makeMCComponent("DYto2L_2Jets_MLL_10to50_ext", "/DYto2L-2Jets_MLL-10to50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6_ext1-v3/NANOAODSIM", "CMS", ".*root", 19982.5)
WtoLNu_2Jets                    = kreator.makeMCComponent("WtoLNu_2Jets", "/WtoLNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 64481.58)
VH_HtoNonbb                     = kreator.makeMCComponent("VH_HtoNonbb", "/VH_HtoNonbb_M-125_TuneCP5_13p6TeV_amcatnloFXFX-madspin-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v1/NANOAODSIM", "CMS", ".*root", 1.01)
WGtoLNuG_PTG_10to100            = kreator.makeMCComponent("WGtoLNuG_PTG_10to100", "/WGtoLNuG-1Jets_PTG-10to100_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 662.2)
WGtoLNuG_PTG_100to200           = kreator.makeMCComponent("WGtoLNuG_PTG_100to200", "/WGtoLNuG-1Jets_PTG-100to200_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 2.214)
WZGtoLNuZG                      = kreator.makeMCComponent("WZGtoLNuZG", "/WZGtoLNuZG_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 0.08425)
DYGto2LG_MLL_4to50_PTG_10to100  = kreator.makeMCComponent("DYGto2LG_MLL-4to50_PTG-10to100", "/DYGto2LG-1Jets_MLL-4to50_PTG-10to100_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 87.94)
DYGto2LG_MLL_4to50_PTG_100to200 = kreator.makeMCComponent("DYGto2LG_MLL-4to50_PTG-100to200", "/DYGto2LG-1Jets_MLL-4to50_PTG-100to200_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 0.2423)
DYGto2LG_MLL_4to50_PTG_200      = kreator.makeMCComponent("DYGto2LG_MLL-4to50_PTG-200", "/DYGto2LG-1Jets_MLL-4to50_PTG-200_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 0.04002)
DYGto2LG_MLL_50_PTG_10to50      = kreator.makeMCComponent("DYGto2LG_MLL-50_PTG-10to50", "/DYGto2LG-1Jets_MLL-50_PTG-10to50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 124.2)
DYGto2LG_MLL_50_PTG_50to100     = kreator.makeMCComponent("DYGto2LG_MLL-50_PTG-50to100", "/DYGto2LG-1Jets_MLL-50_PTG-50to100_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v1/NANOAODSIM", "CMS", ".*root", 2.1)
DYGto2LG_MLL_50_PTG_100to200    = kreator.makeMCComponent("DYGto2LG_MLL-50_PTG-100to200", "/DYGto2LG-1Jets_MLL-50_PTG-100to200_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 0.045)
DYGto2LG_MLL_50_PTG_200to400    = kreator.makeMCComponent("DYGto2LG_MLL-50_PTG-200to400", "/DYGto2LG-1Jets_MLL-50_PTG-200to400_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 0.00329)
DYGto2LG_MLL_50_PTG_400to600    = kreator.makeMCComponent("DYGto2LG_MLL-50_PTG-400to600", "/DYGto2LG-1Jets_MLL-50_PTG-400to600_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 0.00067)
DYGto2LG_MLL_50_PTG_600         = kreator.makeMCComponent("DYGto2LG_MLL-50_PTG-600", "/DYGto2LG-1Jets_MLL-50_PTG-600_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 0.0007773)
QCD_PT_10to30_EMEnriched        = kreator.makeMCComponent("QCD_PT_10to30_EMEnriched", "/QCD_PT-10to30_EMEnriched_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 6896000.0)
QCD_PT_10to30_EMEnriched_ext    = kreator.makeMCComponent("QCD_PT_10to30_EMEnriched_ext", "/QCD_PT-10to30_EMEnriched_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv12-FS22_pilot_130X_mcRun3_2022_realistic_postEE_v6-v3/NANOAODSIM", "CMS", ".*root", 6896000.0)
QCD_PT_30to50_EMEnriched        = kreator.makeMCComponent("QCD_PT_30to50_EMEnriched", "/QCD_PT-30to50_EMEnriched_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 6716000.0)
QCD_PT_50to80_EMEnriched        = kreator.makeMCComponent("QCD_PT_50to80_EMEnriched", "/QCD_PT-50to80_EMEnriched_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 2106000.0)
QCD_PT_80to120_EMEnriched       = kreator.makeMCComponent("QCD_PT_80to120_EMEnriched", "/QCD_PT-80to120_EMEnriched_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 388100.0)
QCD_PT_120to170_EMEnriched      = kreator.makeMCComponent("QCD_PT_120to170_EMEnriched", "/QCD_PT-120to170_EMEnriched_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 71320.0)
QCD_PT_15to20_MuEnrichedPt5     = kreator.makeMCComponent("QCD_PT-15to20_MuEnrichedPt5", "/QCD_PT-15to20_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 2956000.0)
QCD_PT_20to30_MuEnrichedPt5     = kreator.makeMCComponent("QCD_PT-20to30_MuEnrichedPt5", "/QCD_PT-20to30_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 2689000.0)
QCD_PT_30to50_MuEnrichedPt5     = kreator.makeMCComponent("QCD_PT-30to50_MuEnrichedPt5", "/QCD_PT-30to50_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 1442000.0)
QCD_PT_50to80_MuEnrichedPt5     = kreator.makeMCComponent("QCD_PT-50to80_MuEnrichedPt5", "/QCD_PT-50to80_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 405800.0)
QCD_PT_80to120_MuEnrichedPt5    = kreator.makeMCComponent("QCD_PT-80to120_MuEnrichedPt5", "/QCD_PT-80to120_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 96060.0)
QCD_PT_120to170_MuEnrichedPt5   = kreator.makeMCComponent("QCD_PT-120to170_MuEnrichedPt5", "/QCD_PT-120to170_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 23230.0)
QCD_PT_20to30_bcToE             = kreator.makeMCComponent("QCD_PT-20to30_bcToE", "/QCD_PT-20to30_bcToE_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 2028000.0)
QCD_PT_30to80_bcToE             = kreator.makeMCComponent("QCD_PT-30to80_bcToE", "/QCD_PT-30to80_bcToE_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 1308000.0)
QCD_PT_80to170_bcToE            = kreator.makeMCComponent("QCD_PT-80to170_bcToE", "/QCD_PT-80to170_bcToE_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM", "CMS", ".*root", 73560.0)
TTTT                            = kreator.makeMCComponent("TTTT", "/TTTT_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v1/NANOAODSIM",  "CMS", ".*root", 9.652e-03)
TWZ_Tto2Q_WtoLNu_Zto2L_DR1      = kreator.makeMCComponent("TWZ_Tto2Q_WtoLNu_Zto2L_DR1", "/TWZ_Tto2Q_WtoLNu_Zto2L_DR1_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v3/NANOAODSIM" ,  "CMS", ".*root", 3.338e-03)
TWZ_Tto2Q_WtoLNu_Zto2L_DR2      = kreator.makeMCComponent("TWZ_Tto2Q_WtoLNu_Zto2L_DR2", "/TWZ_Tto2Q_WtoLNu_Zto2L_DR2_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v3/NANOAODSIM" ,  "CMS", ".*root", 3.338e-03)
TWZ_TtoLNu_Wto2Q_Zto2L_DR1      = kreator.makeMCComponent("TWZ_TtoLNu_Wto2Q_Zto2L_DR1", "/TWZ_TtoLNu_Wto2Q_Zto2L_DR1_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v4/NANOAODSIM" ,  "CMS", ".*root", 3.338e-03)
TWZ_TtoLNu_Wto2Q_Zto2L_DR2      = kreator.makeMCComponent("TWZ_TtoLNu_Wto2Q_Zto2L_DR2", "/TWZ_TtoLNu_Wto2Q_Zto2L_DR2_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v3/NANOAODSIM" ,  "CMS", ".*root", 3.338e-03)
TWZ_TtoLNu_WtoLNu_Zto2L_DR1     = kreator.makeMCComponent("TWZ_TtoLNu_WtoLNu_Zto2L_DR1", "/TWZ_TtoLNu_WtoLNu_Zto2L_DR1_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v3/NANOAODSIM",  "CMS", ".*root",3.338e-03 )
TWZ_TtoLNu_WtoLNu_Zto2L_DR2     = kreator.makeMCComponent("TWZ_TtoLNu_WtoLNu_Zto2L_DR2", "/TWZ_TtoLNu_WtoLNu_Zto2L_DR2_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v3/NANOAODSIM",  "CMS", ".*root",3.338e-03 )
TTWW                            = kreator.makeMCComponent("TTWW",                        "/TTWW_TuneCP5_13p6TeV_madgraph-madspin-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM",  "CMS", ".*root", 8.178e-03)
THQ_ctcvcp_sm                   = kreator.makeMCComponent("THQ_ctcvcp_sm", "/THQ_ctcvcp_HIncl_M125_4FS_TuneCP5_13p6TeV_madgraph-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM",  "CMS", ".*root", 6.505e-02) # now they dont include the ITC
THW_ctcvcp_sm                   = kreator.makeMCComponent("THW_ctcvcp_sm", "/THW_ctcvcp_HIncl_M125_5FS_TuneCP5_13p6TeV_madgraph-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM",  "CMS", ".*root", 1.600e-02)



samples=[WZto3LNu,
ZZto4L,
ZZto4L_ext,
GluGlutoContinto2Zto4E,
GluGlutoContinto2Zto4Mu,
GluGlutoContinto2Zto4Tau,
TTG_1Jets_PTG_10to100,
TTG_1Jets_PTG_100to200,
TTG_1Jets_PTG_200,
TTHtoNon2B,
TTLL_MLL_50,
TTLL_MLL_4to50,
TTLNu_1Jets,
TZQB,
WZZ,
WWW_4F,
WWZ_4F,
ZZZ,
TTto2L2Nu,
TTto2L2Nu_ext,
TTtoLNu2Q,
TTtoLNu2Q_ext,
TbarWplusto2L2Nu,
TbarWplusto2L2Nu_ext,
TWminusto2L2Nu,
TWminusto2L2Nu_ext,
WZto2L2Q,
WZto2L2Q_ext,
WWto2L2Nu,
WWto2L2Nu_ext,
ZZto2L2Nu,
ZZto2L2Nu_ext,
ZZto2L2Q,
ZZto2L2Q_ext,
DYto2L_2Jets_MLL_50,
DYto2L_2Jets_MLL_50_ext,
DYto2L_2Jets_MLL_10to50,
DYto2L_2Jets_MLL_10to50_ext,
WtoLNu_2Jets,
VH_HtoNonbb,
WGtoLNuG_PTG_10to100,
WGtoLNuG_PTG_100to200,
WZGtoLNuZG,
DYGto2LG_MLL_4to50_PTG_10to100,
DYGto2LG_MLL_4to50_PTG_100to200,
DYGto2LG_MLL_4to50_PTG_200,
DYGto2LG_MLL_50_PTG_10to50,
DYGto2LG_MLL_50_PTG_50to100,
DYGto2LG_MLL_50_PTG_100to200,
DYGto2LG_MLL_50_PTG_200to400,
DYGto2LG_MLL_50_PTG_400to600,
DYGto2LG_MLL_50_PTG_600,
TWZ_Tto2Q_WtoLNu_Zto2L_DR1 ,
TWZ_Tto2Q_WtoLNu_Zto2L_DR2 ,
TWZ_TtoLNu_Wto2Q_Zto2L_DR1 ,
TWZ_TtoLNu_Wto2Q_Zto2L_DR2 ,
TWZ_TtoLNu_WtoLNu_Zto2L_DR1,
TWZ_TtoLNu_WtoLNu_Zto2L_DR2,
TTWW,
THW_ctcvcp_sm,
THQ_ctcvcp_sm,
QCD_PT_10to30_EMEnriched,
QCD_PT_10to30_EMEnriched_ext,
QCD_PT_30to50_EMEnriched,
QCD_PT_50to80_EMEnriched,
QCD_PT_80to120_EMEnriched,
QCD_PT_120to170_EMEnriched,
QCD_PT_15to20_MuEnrichedPt5,
QCD_PT_20to30_MuEnrichedPt5,
QCD_PT_30to50_MuEnrichedPt5,
QCD_PT_50to80_MuEnrichedPt5,
QCD_PT_80to120_MuEnrichedPt5,
QCD_PT_120to170_MuEnrichedPt5,
QCD_PT_20to30_bcToE,
QCD_PT_30to80_bcToE,
         QCD_PT_80to170_bcToE,
         TTTT,
         ]
