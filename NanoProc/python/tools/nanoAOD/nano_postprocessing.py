import os
from CMGTools.Production.globalOptions import getCMGOption

year = getCMGOption("year", "2018")

conf = dict(
        muPt = 5, 
        elePt = 7, 
        miniRelIso = 0.4, 
        sip3d = 8, 
        dxy =  0.05, 
        dz = 0.1, 
        eleId = "mvaFall17V2noIso_WPL",
        muoId = "looseId"
)

ttH_skim_cut = ("nMuon + nElectron >= 2 &&" + 
       "Sum$(Muon_pt > {muPt} && Muon_miniPFRelIso_all < {miniRelIso} && Muon_sip3d < {sip3d} &&  Muon_{muoId}) +"
       "Sum$(Electron_pt > {muPt} && Electron_miniPFRelIso_all < {miniRelIso} && Electron_sip3d < {sip3d} && Electron_{eleId}) >= 2").format(**conf)

if year not in ['2016APV', '2016', '2017', '2018']:
    ttH_skim_cut = ttH_skim_cut.replace("&& Electron_mvaFall17V2noIso_WPL", "") 
    electronSelection = lambda l : abs(l.eta) < 2.5 and l.pt > conf["elePt"] and l.miniPFRelIso_all < conf["miniRelIso"] and l.sip3d < conf["sip3d"] and abs(l.dxy) < conf["dxy"] and abs(l.dz) < conf["dz"]
else:
    electronSelection = lambda l : abs(l.eta) < 2.5 and l.pt > conf["elePt"] and l.miniPFRelIso_all < conf["miniRelIso"] and l.sip3d < conf["sip3d"] and abs(l.dxy) < conf["dxy"] and abs(l.dz) < conf["dz"] and getattr(l, conf["eleId"])
muonSelection     = lambda l : abs(l.eta) < 2.4 and l.pt > conf["muPt" ] and l.miniPFRelIso_all < conf["miniRelIso"] and l.sip3d < conf["sip3d"] and abs(l.dxy) < conf["dxy"] and abs(l.dz) < conf["dz"] and getattr(l, conf["muoId"])


from CMGTools.NanoProc.tools.nanoAOD.ttHPrescalingLepSkimmer import ttHPrescalingLepSkimmer
from PhysicsTools.NanoAODTools.postprocessing.framework.collectionMerger import collectionMerger

lepSkim = ttHPrescalingLepSkimmer(5, 
                muonSel = muonSelection, electronSel = electronSelection,
                minLeptonsNoPrescale = 2, # things with less than 2 leptons are rejected irrespectively of the prescale
                minLeptons = 2, requireSameSignPair = True,
                jetSel = lambda j : j.pt > 25 and abs(j.eta) < 2.4 and j.jetId > 0, 
                minJets = 4, minMET = 70)
lepMerge = collectionMerger(input = ["Electron","Muon"], 
                            output = "LepGood", 
                            selector = dict(Muon = muonSelection, Electron = electronSelection))



from CMGTools.NanoProc.tools.nanoAOD.autoPuWeight import autoPuWeight
from CMGTools.NanoProc.tools.nanoAOD.xsecTagger import xsecTag
from CMGTools.NanoProc.tools.nanoAOD.yearTagger import yearTag
from CMGTools.NanoProc.tools.nanoAOD.lepJetBTagAdder import lepJetBTagCSV, lepJetBTagDeepCSV, lepJetBTagDeepFlav, lepJetBTagDeepFlavC

if year in ['2016APV', '2016', '2017', '2018']:
    from CMGTools.NanoProc.tools.nanoAOD.LepMVAULFriend import lepMVA
else:
    from CMGTools.NanoProc.tools.nanoAOD.lepMVAWZ_run3  import lepMVAWZ_run3
    lepMVA = lepMVAWZ_run3(
        os.environ['CMSSW_BASE'] + '/src/CMGTools/NanoProc/data/leptonMVA/tth/', 
        elxmlpath = "Electron-mvaTTH.2022EE.weights_mvaISO.xml",
        muxmlpath = "Muon-mvaTTH.2022EE.weights.xml",
        suffix = "_run3",
    )


ttH_sequence_step1 = [lepSkim, lepMerge, autoPuWeight, yearTag, xsecTag,  lepJetBTagDeepFlav, lepMVA]

#==== 
#from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import DeltaR
# from CMGTools.NanoProc.tools.nanoAOD.ttHLepQCDFakeRateAnalyzer import ttHLepQCDFakeRateAnalyzer
# centralJetSel = lambda j : j.pt > 25 and abs(j.eta) < 2.4 and j.jetId > 0
# lepFR = ttHLepQCDFakeRateAnalyzer(jetSel = centralJetSel,
#                                   pairSel = lambda pair : DeltaR(pair[0].eta, pair[0].phi, pair[1].eta, pair[1].phi) > 0.7,
#                                   maxLeptons = 1, requirePair = True)
# from CMGTools.NanoProc.tools.nanoAOD.nBJetCounter import nBJetCounter
# nBJetDeepCSV25NoRecl = lambda : nBJetCounter("DeepCSV25", "btagDeepB", centralJetSel)
# nBJetDeepFlav25NoRecl = lambda : nBJetCounter("DeepFlav25", "btagDeepFlavB", centralJetSel)

# ttH_sequence_step1_FR = [m for m in ttH_sequence_step1 if m != lepSkim] + [ lepFR, nBJetDeepCSV25NoRecl, nBJetDeepFlav25NoRecl ]
# ttH_skim_cut_FR = ("nMuon + nElectron >= 1 && nJet >= 1 && Sum$(Jet_pt > 25 && abs(Jet_eta)<2.4) >= 1 &&" + 
#        "Sum$(Muon_pt > {muPt} && Muon_miniPFRelIso_all < {miniRelIso} && Muon_sip3d < {sip3d}) +"
#        "Sum$(Electron_pt > {muPt} && Electron_miniPFRelIso_all < {miniRelIso} && Electron_sip3d < {sip3d} && Electron_{eleId}) >= 1").format(**conf)



triggerGroups_dict=dict(
    Trigger_1e={
        "2016"    :  ['HLT_Ele27_WPTight_Gsf' , 'HLT_Ele25_eta2p1_WPTight_Gsf' , 'HLT_Ele27_eta2p1_WPLoose_Gsf'],
        "2016APV" :  ['HLT_Ele27_WPTight_Gsf' , 'HLT_Ele25_eta2p1_WPTight_Gsf' , 'HLT_Ele27_eta2p1_WPLoose_Gsf'],
        "2017"    :  ['HLT_Ele32_WPTight_Gsf' , 'HLT_Ele35_WPTight_Gsf'],
        "2018"    :  ['HLT_Ele32_WPTight_Gsf'],
        "2022"    :  ['HLT_Ele32_WPTight_Gsf'],
        "2022EE"  :  ['HLT_Ele32_WPTight_Gsf'], 
    },
    Trigger_1m={
        "2016"    :  ['HLT_IsoMu24' , 'HLT_IsoTkMu24' , 'HLT_IsoMu22_eta2p1' , 'HLT_IsoTkMu22_eta2p1' , 'HLT_IsoMu22' , 'HLT_IsoTkMu22'],
        "2016APV" :  ['HLT_IsoMu24' , 'HLT_IsoTkMu24' , 'HLT_IsoMu22_eta2p1' , 'HLT_IsoTkMu22_eta2p1' , 'HLT_IsoMu22' , 'HLT_IsoTkMu22'],
        "2017"    :  ['HLT_IsoMu24' , 'HLT_IsoMu27'],
        "2018"    :  ['HLT_IsoMu24'],
        "2022"    :  ['HLT_IsoMu24'],
        "2022EE"  :  ['HLT_IsoMu24'], 
    },
    Trigger_2e={
        "2016"    :  ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'],
        "2016APV" :  ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'],
        "2017"    :  ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'],
        "2018"    :  ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'],
        "2022"    :  ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'],
        "2022EE"  :  ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'],
    },
    Trigger_2m={
        "2016"    :  ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL' , 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL' ,  'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ' , 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ'],
        "2016APV" :  ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL' , 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL' ,  'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ' , 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ'],
        "2017"    :  ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8' , 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8'],
        "2018"    :  ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8'],
        "2022"    :  ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8'],
        "2022EE"  :  ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8'],
    },
    Trigger_em={
        "2016"    :   ['HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL' , 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ', 'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL' , 'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_DZ'],
        "2016APV" :   ['HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL' , 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ', 'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL' , 'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_DZ'],
        "2017"    :   ['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL', 'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'        , 'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'        , 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'],
        "2018"    :   ['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL', 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'        , 'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'],
        "2022"    :   ['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL', 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'        , 'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'],
        "2022EE"  :   ['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL', 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'        , 'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'],
        
    },
    Trigger_3e={
        "2016"    :  ['HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL'],
        "2016APV" :  ['HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL'],
        "2017"    :  ['HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL'],
        "2018"    :  ['HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL'], # prescaled in the two years according to https://twiki.cern.ch/twiki/bin/view/CMS/EgHLTRunIISummary#2018
        "2022"    :  ['HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL'],
        "2022EE"  :  ['HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL'], 
    },
    Trigger_3m={
        "2016"    :  ['HLT_TripleMu_12_10_5'],
        "2016APV" :  ['HLT_TripleMu_12_10_5'],
        "2017"    :  ['HLT_TripleMu_12_10_5'],
        "2018"    :  ['HLT_TripleMu_12_10_5'],
        "2022"    :  ['HLT_TripleMu_12_10_5'],
        "2022EE"  :  ['HLT_TripleMu_12_10_5'],
    },
    Trigger_mee={
        "2016"    :  ['HLT_Mu8_DiEle12_CaloIdL_TrackIdL'],
        "2016APV" :  ['HLT_Mu8_DiEle12_CaloIdL_TrackIdL'],
        "2017"    :  ['HLT_Mu8_DiEle12_CaloIdL_TrackIdL'],
        "2018"    :  ['HLT_Mu8_DiEle12_CaloIdL_TrackIdL'],
        "2022"    :  ['HLT_Mu8_DiEle12_CaloIdL_TrackIdL'],
        "2022EE"  :  ['HLT_Mu8_DiEle12_CaloIdL_TrackIdL'],
    },
    Trigger_mme={
        "2016"    :  ['HLT_DiMu9_Ele9_CaloIdL_TrackIdL'   ],
        "2016APV" :  ['HLT_DiMu9_Ele9_CaloIdL_TrackIdL'   ],
        "2017"    :  ['HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ'],
        "2018"    :  ['HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ'],
        "2022"    :  ['HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ'],
        "2022EE"  :  ['HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ'],
    },
    Trigger_MET={ 
        "2016"    : ["HLT_PFMET120_PFMHT120_IDTight"],
        "2016APV" : ["HLT_PFMET120_PFMHT120_IDTight"],
        "2017"    : ["HLT_PFMET120_PFMHT120_IDTight"],
        "2018"    : ["HLT_PFMET120_PFMHT120_IDTight"],
    }
)


