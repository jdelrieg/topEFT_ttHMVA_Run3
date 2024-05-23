import os

conf = dict(
    muPt = 3, 
    elePt = 5, 
    sip3d = 2.5, 
    dxy =  0.05, 
    dz = 0.1, 
    minMet = 50.,
    ip3d = 0.0175,
    iperbolic_iso_0 = 20.,
    iperbolic_iso_1 = 300.,
)
#susySOS_skim_cut =  ("nMuon + nElectron >= 2 &&" + ##if heppy option fast
#        "MET_pt > {minMet}  &&"+
#        "Sum$(Muon_pt > {muPt}) +"
#        "Sum$(Electron_pt > {elePt}) >= 2").format(**conf)
susySOS_skim_cut =  "1"

muonSelection     = lambda l: abs(l.eta) < 2.4 and l.pt > conf["muPt"]  and l.sip3d < conf["sip3d"] and abs(l.dxy) < conf["dxy"] and abs(l.dz) < conf["dz"]  and l.pfRelIso03_all*l.pt < ( conf["iperbolic_iso_0"]+conf["iperbolic_iso_1"]/l.pt) and abs(l.ip3d) < conf["ip3d"]
electronSelection = lambda l: abs(l.eta) < 2.5 and l.pt > conf["elePt"]  and l.sip3d < conf["sip3d"] and abs(l.dxy) < conf["dxy"] and abs(l.dz) < conf["dz"] and l.pfRelIso03_all*l.pt < ( conf["iperbolic_iso_0"]+conf["iperbolic_iso_1"]/l.pt) and abs(l.ip3d) < conf["ip3d"] 


from CMGTools.NanoProc.tools.nanoAOD.ttHPrescalingLepSkimmer import ttHPrescalingLepSkimmer
# NB: do not wrap lepSkim a lambda, as we modify the configuration in the cfg itself 
lepSkim = ttHPrescalingLepSkimmer(0, ##do not apply prescale
                                  muonSel = muonSelection, electronSel = electronSelection,
                                  minLeptonsNoPrescale = 2, # things with less than 2 leptons are rejected irrespectively of the prescale
                                  minLeptons = 2, requireSameSignPair = False,
                                  jetSel = lambda j: j.pt > 25 and abs(j.eta) < 2.4  and j.jetId > 0, 
                                  minJets = 0, minMET = 0, minMETNoPrescale = 50)

from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import collectionMerger
lepMerge = collectionMerger(input = ["Electron","Muon"], 
                            output = "LepGood", 
                            selector = dict(Muon = muonSelection, Electron = electronSelection))

from CMGTools.NanoProc.tools.nanoAOD.ttHLeptonCombMasses import ttHLeptonCombMasses
lepMasses = ttHLeptonCombMasses( [ ("Muon",muonSelection), ("Electron",electronSelection) ], maxLeps = 4)

from CMGTools.NanoProc.tools.nanoAOD.autoPuWeight import autoPuWeight
from CMGTools.NanoProc.tools.nanoAOD.yearTagger import yearTag
from CMGTools.NanoProc.tools.nanoAOD.xsecTagger import xsecTag
from CMGTools.NanoProc.tools.nanoAOD.lepJetBTagAdder import lepJetBTagCSV, lepJetBTagDeepCSV

susySOS_sequence_step1 = [autoPuWeight, lepSkim, lepMerge, yearTag, xsecTag, lepJetBTagCSV, lepJetBTagDeepCSV, lepMasses]


#from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
#from CMGTools.NanoProc.tools.nanoAOD.ttHLepQCDFakeRateAnalyzer import ttHLepQCDFakeRateAnalyzer
#lepFR = ttHLepQCDFakeRateAnalyzer(jetSel = lambda j: j.pt > 25 and abs(j.eta) < 2.4,
#                                  pairSel = lambda pair: deltaR(pair[0].eta, pair[0].phi, pair[1].eta, pair[1].phi) > 0.7,
#                                  maxLeptons = 1, requirePair = True)
#
#susySOS_sequence_step1_FR = [m for m in susySOS_sequence_step1 if m != lepSkim] + [ lepFR ]


#==== items below are normally run as friends ====

import numpy
from numpy import log
def calculateRawMVA(score):
    if score == -1.:
        return -999.
    elif score == 1.:
        return 999.
    else:
        return -0.5*numpy.log((1-score)/(1+score))


def SOSTightID2018(lep):
    if (lep.pt < 10): ##loose at low pt
        return lep.mvaFall17V2noIso_WPL
    else: #susy tight at higher, from https://twiki.cern.ch/twiki/pub/CMS/SUSLeptonSF/Run2_SUSYwp_EleCB_MVA_8Jan19.pdf
        mvaRaw = calculateRawMVA(lep.mvaFall17V2noIso)
        if abs(lep.eta)<0.8:
            if lep.pt<25:
                return mvaRaw > 4.277 + 0.112*(lep.pt - 25)
            else:
                return mvaRaw > 4.277
        elif abs(lep.eta)>=0.8 and abs(lep.eta)<1.479:
            if lep.pt<25:
                return mvaRaw > 3.152 + 0.60*(lep.pt - 25)
            else:
                return mvaRaw > 3.152
        elif abs(lep.eta)>=1.479:
            if lep.pt<25:
                return mvaRaw > 2.359 + 0.89*(lep.pt - 25)
            else:
                return mvaRaw > 2.359


def susyEleIdParametrization(p1,p2,pt,year):
    if year ==  2016 or year ==2018:
        return p1 + p2*(pt-25.)
    else:
        return p1 + (p2/15.)*(pt-10.)

def VLooseFOEleID(lep,year):# from https://twiki.cern.ch/twiki/pub/CMS/SUSLeptonSF/Run2_SUSYwp_EleCB_MVA_8Jan19.pdf
    if year == 2016:
        cuts = dict(cEB = [-0.259, -0.388, 0.109, -0.388], 
                    oEB = [-0.256, -0.696, 0.106, -0.696],
                    EE  = [-1.630, -1.219, 0.148, -1.219],
                    IdVersion = "mvaFall17V2noIso") 
    elif year == 2017:
        cuts = dict(cEB = [-0.135, -0.930, 0.043, -0.887], 
                    oEB = [-0.417, -0.930, 0.040, -0.890],
                    EE  = [-0.470, -0.942, 0.032, -0.910],
                    IdVersion = "mvaFall17V1noIso") 
    elif year == 2018:
        cuts = dict(cEB = [+0.053, -0.106, 0.062, -0.106], 
                    oEB = [-0.434, -0.769, 0.038, -0.769],
                    EE  = [-0.956, -1.461, 0.042, -1.461],
                    IdVersion = "mvaFall17V2noIso") 
    else:
        print("Year not in [2016,2017,2018], returning False")
        return False
    mvaValue = getattr(lep, cuts["IdVersion"]) if year==2017 else  calculateRawMVA(getattr(lep, cuts["IdVersion"])) ##raw for 2016 and 2018, normalized for 2017
    if abs(lep.eta)<0.8:
        if lep.pt<10:
            return mvaValue > cuts["cEB"][0]
        elif lep.pt<25:
            return mvaValue > susyEleIdParametrization( cuts["cEB"][1],  cuts["cEB"][2], lep.pt, year)
        else:
            return mvaValue >  cuts["cEB"][3]
    elif abs(lep.eta)>=0.8 and abs(lep.eta)<1.479:
        if lep.pt<10:
            return mvaValue > cuts["oEB"][0]
        elif lep.pt<25:
            return mvaValue > susyEleIdParametrization( cuts["oEB"][1],  cuts["oEB"][2], lep.pt, year)
        else:
            return mvaValue >  cuts["oEB"][3]
    elif abs(lep.eta)>=1.479:
        if lep.pt<10:
            return mvaValue > cuts["EE"][0]
        elif lep.pt<25:
            return mvaValue > susyEleIdParametrization( cuts["EE"][1],  cuts["EE"][2], lep.pt, year)
        else:
            return mvaValue >  cuts["EE"][3]

          
def new_FOEleID(lep,year):# from https://indico.cern.ch/event/878236/contributions/3699845/attachments/1968758/3274470/FRFlavPerYear_Muons_Electrons_NewFODef.pdf, slide 22
    if year == 2016:
        cuts = dict(EB = [0.97, 0.97, 0.85], 
                    EE  = [0.98, 0.80, 0.20],
                    IdVersion = "mvaFall17V2noIso") 
    elif year == 2017:
        cuts = dict(EB = [0.80, -0.20, -0.40], 
                    EE  = [0.75, -0.20, -0.40],
                    IdVersion = "mvaFall17V1noIso") 
    elif year == 2018:
        cuts = dict(EB = [0.98, 0.98, 0.80], 
                    EE  = [0.98, 0.90, 0.00],
                    IdVersion = "mvaFall17V2noIso") 
    else:
        print("Year not in [2016,2017,2018], returning False")
        return False
    mvaValue = getattr(lep, cuts["IdVersion"]) ##using only normalised mva values, no raw ones for this ID
    if  abs(lep.eta)<1.479:
        if lep.pt<10:
            return mvaValue > cuts["EB"][0]
        elif lep.pt<20:
            return mvaValue > cuts["EB"][1]
        else:
            return mvaValue >  cuts["EB"][2]
    elif abs(lep.eta)>=1.479:
        if lep.pt<10:
            return mvaValue > cuts["EE"][0]
        elif lep.pt<20:
            return mvaValue > cuts["EE"][1]
        else:
            return mvaValue >  cuts["EE"][2]



def tightEleID(lep,year):# from https://twiki.cern.ch/twiki/pub/CMS/SUSLeptonSF/Run2_SUSYwp_EleCB_MVA_8Jan19.pdf
    if year == 2016:
        cuts = dict(cEB = [3.447, 0.063, 4.392], 
                    oEB = [2.522, 0.058, 3.392],
                    EE  = [1.555, 0.075, 2.680],
                    IdVersion = "mvaFall17V2noIso",
                    wpLowPt = "WP80") 
    elif year == 2017:
        cuts = dict(cEB = [0.200, 0.032, 0.680], 
                    oEB = [0.100, 0.025, 0.475],
                    EE  = [-0.100, 0.028, 0.320],
                    IdVersion = "mvaFall17V1noIso",
                    wpLowPt = "WP90") 
    elif year == 2018:
        cuts = dict(cEB = [4.277, 0.112, 4.277], 
                    oEB = [3.152, 0.060, 3.152],
                    EE  = [2.359, 0.087, 2.359],
                    IdVersion = "mvaFall17V2noIso",
                    wpLowPt = "WP80") 
    else:
        print("Year not in [2016,2017,2018], returning False")
        return False
    mvaValue = getattr(lep, cuts["IdVersion"]) if year==2017 else  calculateRawMVA(getattr(lep, cuts["IdVersion"])) ##raw for 2016 and 2018, normalized for 2017
    if lep.pt<10:
        return getattr(lep, cuts["IdVersion"]+"_"+cuts["wpLowPt"])
    if abs(lep.eta)<0.8:
        if lep.pt<25:
            return mvaValue > susyEleIdParametrization( cuts["cEB"][0],  cuts["cEB"][1], lep.pt, year)
        elif lep.pt<40: #2016 still has slope between 25 and 40
            if year == 2016:
                return mvaValue > susyEleIdParametrization( cuts["cEB"][0],  cuts["cEB"][1], lep.pt, year)
            else:
                return mvaValue >  cuts["cEB"][2]
        else:
            return mvaValue >  cuts["cEB"][2]

    elif abs(lep.eta)>=0.8 and abs(lep.eta)<1.479:
        if lep.pt<25:
            return mvaValue > susyEleIdParametrization( cuts["oEB"][0],  cuts["oEB"][1], lep.pt, year)
        elif lep.pt<40:
            if year == 2016:
                return mvaValue > susyEleIdParametrization( cuts["cEB"][0],  cuts["cEB"][1], lep.pt, year)
            else:
                return mvaValue >  cuts["oEB"][2]
        else:
            return mvaValue >  cuts["oEB"][2]
    elif abs(lep.eta)>=1.479:
        if lep.pt<25:
            return mvaValue > susyEleIdParametrization( cuts["EE"][0],  cuts["EE"][1], lep.pt, year)
        elif lep.pt<40:
            if year == 2016:
                return mvaValue > susyEleIdParametrization( cuts["EE"][0],  cuts["EE"][1], lep.pt, year)
            else:
                return mvaValue >  cuts["EE"][2]
        else:
            return mvaValue >  cuts["EE"][2]



def tightLeptonSel_SOS(lep,year):
    bTagCut = 0.4 if year==2016 else 0.1522 if year==2017 else 0.1241 ##2016 loose recomm is 0.2217, while 0.4 derived to match 2018 performance
    return ( lep.jetBTagDeepCSV < bTagCut) and ( (abs(lep.pdgId)==13 and lep.softId) or (abs(lep.pdgId)==11 and VLooseFOEleID(lep, year) and lep.lostHits==0 and lep.convVeto and tightEleID(lep, year) )) and lep.pfRelIso03_all<0.5 and (lep.pfRelIso03_all*lep.pt)<5. and abs(lep.ip3d)<0.01 and lep.sip3d<2
    
def looseNotTight_SOS(lep,year):
    return  lep.pfRelIso03_all<1. and  ( (abs(lep.pdgId)==11 and new_FOEleID(lep, year) and lep.lostHits==0 and lep.convVeto)
                                         or (abs(lep.pdgId)==13 and lep.softId ) )


##old cleaning selections, used only for flags
def clean_and_FO_selection_SOS(lep,year):
    bTagCut = 0.4 if year==2016 else 0.1522 if year==2017 else 0.1241 ##2016 loose recomm is 0.2217, while 0.4 derived to match 2018 performance
    return lep.jetBTagDeepCSV < bTagCut and ( (abs(lep.pdgId)==11 and VLooseFOEleID(lep, year) and lep.lostHits==0 and lep.convVeto)
                                         or (abs(lep.pdgId)==13 and lep.softId ) )
def clean_and_FO_selection_SOS_noBtag(lep,year):
    return ( (abs(lep.pdgId)==11 and VLooseFOEleID(lep,year) and lep.lostHits==0 and lep.convVeto)
                                         or (abs(lep.pdgId)==13 and lep.softId ) )

def fullCleaningLeptonSel(lep,year):
    return clean_and_FO_selection_SOS(lep,year) and ( (abs(lep.pdgId)==11 and (VLooseFOEleID(lep, year) and lep.lostHits<=1))
										or (abs(lep.pdgId)==13 and lep.looseId) )
def fullCleaningLeptonSel_noBtag(lep, year):
    return clean_and_FO_selection_SOS_noBtag(lep,year) and ( (abs(lep.pdgId)==11 and (VLooseFOEleID(lep, year) and lep.lostHits<=1))
										or (abs(lep.pdgId)==13 and lep.looseId) )

def fullTightLeptonSel(lep,year):
    return ( fullCleaningLeptonSel(lep,year) and ( abs(lep.pdgId)==13 or tightEleID(lep, year) )
										and lep.pfRelIso03_all<0.5 and (lep.pfRelIso03_all*lep.pt)<5. and abs(lep.ip3d)<0.01 and lep.sip3d<2 )
def fullTightLeptonSel_noBtag(lep,year):
    return ( fullCleaningLeptonSel_noBtag(lep,year) and ( abs(lep.pdgId)==13 or tightEleID(lep, year) )
										and lep.pfRelIso03_all<0.5 and (lep.pfRelIso03_all*lep.pt)<5. and abs(lep.ip3d)<0.01 and lep.sip3d<2 )

def tightLepDY(lep,year):
	return ( clean_and_FO_selection_SOS(lep,year) and ( abs(lep.pdgId)==13 or tightEleID(lep, year) )
										and lep.pfRelIso03_all<0.5 and ((lep.pfRelIso03_all*lep.pt)<5. or lep.pfRelIso03_all<0.1) ) # relax iso cut,no ip3d cut,no sip3d cut
def tightLepTT(lep,year):
	return ( clean_and_FO_selection_SOS(lep,year) and ( abs(lep.pdgId)==13 or tightEleID(lep, year) )
										and lep.pfRelIso03_all<0.5 and ((lep.pfRelIso03_all*lep.pt)<5. or lep.pfRelIso03_all<0.1) and abs(lep.ip3d)<0.01 and lep.sip3d<2 ) #r elax iso cut
def tightLepVV(lep,year):
	return ( clean_and_FO_selection_SOS(lep,year) and ( abs(lep.pdgId)==13 or tightEleID(lep, year) )
										and lep.pfRelIso03_all<0.5 and ((lep.pfRelIso03_all*lep.pt)<5. or lep.pfRelIso03_all<0.1) and abs(lep.ip3d)<0.01 and lep.sip3d<2 ) #r elax iso cut
def tightLepWZ(lep,year):
	return ( clean_and_FO_selection_SOS(lep,year) and ( abs(lep.pdgId)==13 or tightEleID(lep, year) )
										and lep.pfRelIso03_all<0.5 and ((lep.pfRelIso03_all*lep.pt)<5. or lep.pfRelIso03_all<0.1) and abs(lep.ip3d)<0.01 and lep.sip3d<2 ) #r elax iso cut

foTauSel = lambda tau: False
tightTauSel = lambda tau: False

from CMGTools.NanoProc.tools.combinedObjectTaggerForCleaning import CombinedObjectTaggerForCleaning
from CMGTools.NanoProc.tools.nanoAOD.fastCombinedObjectRecleaner import fastCombinedObjectRecleaner
recleaner_step1 = lambda : CombinedObjectTaggerForCleaning("InternalRecl",
	looseLeptonSel = lambda lep,year: ((abs(lep.pdgId)==11 and (VLooseFOEleID(lep,year) and lep.lostHits<=1))) or (abs(lep.pdgId)==13 and lep.looseId),
	cleaningLeptonSel = lambda lep,year: tightLeptonSel_SOS(lep,year) or  looseNotTight_SOS(lep,year) ,
        FOLeptonSel = lambda lep,year: tightLeptonSel_SOS(lep,year) or  looseNotTight_SOS(lep,year) ,
	tightLeptonSel = lambda lep,year: tightLeptonSel_SOS(lep,year), #tight wp
	FOTauSel = foTauSel,
	tightTauSel = tightTauSel,
	selectJet = lambda jet: abs(jet.eta)<2.4 and jet.pt > 25 and jet.jetId > 0, # FIXME need to select on pt or ptUp or ptDown
	coneptdef = lambda lep: lep.pt)
recleaner_step2_mc = lambda : fastCombinedObjectRecleaner(label="Recl", inlabel="_InternalRecl",
	cleanTausWithLooseLeptons=True,
	cleanJetsWithFOTaus=True,
	doVetoZ=False, doVetoLMf=False, doVetoLMt=False,
	jetPts=[25,40],
	jetPtsFwd=[25,40],
	btagL_thr=lambda year: 0.4 if year==2016 else 0.1522 if year==2017 else 0.1241,
	btagM_thr=lambda year: 0.6324 if year==2016 else 0.4941 if year==2017 else 0.4184,
        jetBTag='btagDeepB',
        isMC = True,
        variations=["jesTotal","jer"])
recleaner_step2_data = lambda : fastCombinedObjectRecleaner(label="Recl", inlabel="_InternalRecl",
	cleanTausWithLooseLeptons=True,
	cleanJetsWithFOTaus=True,
	doVetoZ=False, doVetoLMf=False, doVetoLMt=False,
	jetPts=[25,40],
	jetPtsFwd=[25,40],
	btagL_thr=lambda year: 0.4 if year==2016 else 0.1522 if year==2017 else 0.1241,
	btagM_thr=lambda year: 0.6324 if year==2016 else 0.4941 if year==2017 else 0.4184,
        jetBTag='btagDeepB',
        isMC = False,
        variations=[])

from CMGTools.NanoProc.tools.eventVars_2lss import EventVars2LSS
eventVars = lambda : EventVars2LSS('','Recl', doSystJEC=False)

from CMGTools.NanoProc.tools.objTagger import ObjTagger
isMatchRightCharge = lambda : ObjTagger('isMatchRightCharge','LepGood', [lambda l,g: (l.genPartFlav==1 or l.genPartFlav == 15) and (g.pdgId*l.pdgId > 0) ], linkColl='GenPart',linkVar='genPartIdx')
mcMatchId     = lambda : ObjTagger('mcMatchId','LepGood', [lambda l: (l.genPartFlav==1 or l.genPartFlav == 15) ])
mcPromptGamma = lambda : ObjTagger('mcPromptGamma','LepGood', [lambda l: (l.genPartFlav==22)])
mcMatch_seq   = [ isMatchRightCharge, mcMatchId ,mcPromptGamma]

from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import jetmetUncertaintiesProducer
# FullSIM JECs
jetmetUncertainties2016 = lambda : jetmetUncertaintiesProducer("2016", "Summer16_07Aug2017_V11_MC", [ "Total" ])
jetmetUncertainties2017 = lambda : jetmetUncertaintiesProducer("2017", "Fall17_17Nov2017_V32_MC",   [ "Total" ], metBranchName='METFixEE2017')
jetmetUncertainties2018 = lambda : jetmetUncertaintiesProducer("2018", "Autumn18_V19_MC",           [ "Total" ])
# FastSIM JECs
jetmetUncertainties2016Fast = lambda : jetmetUncertaintiesProducer("2016", "Summer16_FastSimV1_MC", [ "Total" ])
jetmetUncertainties2017Fast = lambda : jetmetUncertaintiesProducer("2017", "Fall17_FastSimV1_MC",   [ "Total" ], metBranchName='METFixEE2017')
jetmetUncertainties2018Fast = lambda : jetmetUncertaintiesProducer("2018", "Autumn18_FastSimV1_MC", [ "Total" ])

isVLFOEle = lambda : ObjTagger('isVLFOEle', "Electron", [lambda lep,year: VLooseFOEleID(lep,year) ])
isTightEle = lambda : ObjTagger('isTightEle', "Electron", [lambda lep,year: tightEleID(lep,year)  ])

isCleanEle = lambda : ObjTagger('isCleanEle', "Electron", [ lambda lep,year: fullCleaningLeptonSel(lep,year) and electronSelection(lep) ])
isCleanMu = lambda : ObjTagger('isCleanMu', "Muon", [ lambda lep,year: fullCleaningLeptonSel(lep,year) and muonSelection(lep) ])
isCleanEle_noBtag = lambda : ObjTagger('isCleanEle_noBtag', "Electron", [ lambda lep,year: fullCleaningLeptonSel_noBtag(lep,year) and electronSelection(lep)  ])
isCleanMu_noBtag = lambda : ObjTagger('isCleanMu_noBtag', "Muon", [ lambda lep,year: fullCleaningLeptonSel_noBtag(lep,year) and muonSelection(lep) ])

isTightSOSEle = lambda : ObjTagger('isTightSOSEle', "Electron", [ lambda lep,year: fullTightLeptonSel(lep,year) and electronSelection(lep) ])
isTightSOSMu = lambda : ObjTagger('isTightSOSMu', "Muon", [ lambda lep,year: fullTightLeptonSel(lep,year) and muonSelection(lep) ])
isTightSOSEle_noBtag = lambda : ObjTagger('isTightSOSEle_noBtag', "Electron", [ lambda lep,year: fullTightLeptonSel_noBtag(lep,year) and electronSelection(lep) ])
isTightSOSMu_noBtag = lambda : ObjTagger('isTightSOSMu_noBtag', "Muon", [ lambda lep,year: fullTightLeptonSel_noBtag(lep,year) and muonSelection(lep) ])

isTightSOSLepGood = lambda : ObjTagger('isTightSOSLepGood', "LepGood", [ lambda lep,year: fullTightLeptonSel(lep,year) ])

isTightLepDY = lambda : ObjTagger('isTightLepDY', "LepGood", [ lambda lep,year: tightLepDY(lep,year) ]) # relax iso cut,no ip3d cut,no sip3d cut
isTightLepTT = lambda : ObjTagger('isTightLepTT', "LepGood", [ lambda lep,year: tightLepTT(lep,year) ]) # relax iso cut
isTightLepVV = lambda : ObjTagger('isTightLepVV', "LepGood", [ lambda lep,year: tightLepVV(lep,year) ]) # relax iso cut
isTightLepWZ = lambda : ObjTagger('isTightLepWZ', "LepGood", [ lambda lep,year: tightLepWZ(lep,year) ]) # relax iso cut

isFOLep = lambda : ObjTagger('isFOLep', "LepGood", [ lambda lep,year: tightLeptonSel_SOS(lep,year) or  looseNotTight_SOS(lep,year) ]) 

eleSel_seq = [isVLFOEle, isTightEle]
tightLepCR_seq = [isTightLepDY,isTightLepTT,isTightLepVV,isTightLepWZ]

data_recl_seq=[recleaner_step1,recleaner_step2_data]
mc_recl_seq=[recleaner_step1,recleaner_step2_mc,mcMatchId,mcPromptGamma]


#btag weights
from CMGTools.NanoProc.tools.bTagEventWeightsCSVFullShape import BTagEventWeightFriend
eventBTagWeight_16 = lambda : BTagEventWeightFriend(csvfile=os.environ["CMSSW_BASE"]+"/src/CMGTools/NanoProc/data/btag/DeepCSV_2016LegacySF_V1.csv", discrname="btagDeepB")
eventBTagWeight_17 = lambda : BTagEventWeightFriend(csvfile=os.environ["CMSSW_BASE"]+"/src/CMGTools/NanoProc/data/btag/DeepCSV_94XSF_V4_B_F.csv", discrname="btagDeepB")
eventBTagWeight_18 = lambda : BTagEventWeightFriend(csvfile=os.environ["CMSSW_BASE"]+"/src/CMGTools/NanoProc/data/btag/DeepCSV_102XSF_V1.csv", discrname="btagDeepB")

from CMGTools.NanoProc.tools.bTagEventWeights import BTagEventWeightFriend as BTagEventWeightFriendFast
eventBTagWeight_16Fast = lambda : BTagEventWeightFriendFast(csvfile=os.environ["CMSSW_BASE"]+"/src/CMGTools/NanoProc/data/btag/DeepCSV_2016LegacySF_V1.csv", csvfastsim=os.environ["CMSSW_BASE"]+"/src/CMGTools/NanoProc/data/btag/deepcsv_13TEV_16SL_18_3_2019.csv", eff_rootfile=os.environ['CMSSW_BASE']+"/src/CMGTools/NanoProc/data/btag/bTagEffs.root", wp="M", algo='deepcsv', btag_branch="btagDeepB", year=2016)
eventBTagWeight_17Fast = lambda : BTagEventWeightFriendFast(csvfile=os.environ["CMSSW_BASE"]+"/src/CMGTools/NanoProc/data/btag/DeepCSV_94XSF_V4_B_F.csv", csvfastsim=os.environ["CMSSW_BASE"]+"/src/CMGTools/NanoProc/data/btag/deepcsv_13TEV_17SL_18_3_2019.csv", eff_rootfile=os.environ['CMSSW_BASE']+"/src/CMGTools/NanoProc/data/btag/bTagEffs.root", wp="M", algo='deepcsv', btag_branch="btagDeepB", year=2017)
eventBTagWeight_18Fast = lambda : BTagEventWeightFriendFast(csvfile=os.environ["CMSSW_BASE"]+"/src/CMGTools/NanoProc/data/btag/DeepCSV_102XSF_V1.csv", csvfastsim=os.environ["CMSSW_BASE"]+"/src/CMGTools/NanoProc/data/btag/deepcsv_13TEV_18SL_7_5_2019.csv", eff_rootfile=os.environ['CMSSW_BASE']+"/src/CMGTools/NanoProc/data/btag/bTagEffs.root", wp="M", algo='deepcsv', btag_branch="btagDeepB", year=2018)

### TnP stuff
susySOS_TnP_cut =  ("Sum$(Muon_pt > 3.0 && fabs(Muon_eta) < 2.4 && Muon_looseId == 1) >= 2 || Sum$(Electron_pt > 5.0 && fabs(Electron_eta) < 2.5) >= 2")

from CMGTools.NanoProc.tools.nanoAOD.lepJetBTagAdder import eleJetBTagDeepCSV, muonJetBTagDeepCSV
from CMGTools.NanoProc.tools.nanoAOD.addTnpTree import addTnpTree

def TnP(year,collection):
    return ( lambda : addTnpTree(year,collection) )

def susySOS_sequence_TnP(year,collection): # TnP module should always be last
    if collection == "Muon": return [autoPuWeight, yearTag, xsecTag, muonJetBTagDeepCSV, TnP(year,collection) ]
    if collection == "Electron": return [autoPuWeight, yearTag, xsecTag, eleJetBTagDeepCSV, TnP(year,collection) ]


# signal re-weighting
from CMGTools.NanoProc.tools.nanoAOD.mllReweight import mllReweight
from CMGTools.NanoProc.tools.nanoAOD.vb_decaymodes import VB_DecayModes

sigRew = [mllReweight,VB_DecayModes]

from CMGTools.NanoProc.tools.nanoAOD.isrReweight import isrReweight

isrReweight2016 = lambda :  isrReweight(isrWfile=os.environ["CMSSW_BASE"]+"/src/CMGTools/NanoProc/data/isrReweights_corrections_TChiWZ_2016.json" , normWfile=os.environ["CMSSW_BASE"]+"/src/CMGTools/NanoProc/data/isrReweight_normalizedConsts_TChiWZ_2016.txt")
