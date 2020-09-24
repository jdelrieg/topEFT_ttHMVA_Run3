#!/usr/bin/env python
import sys
import re
import os
import errno
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("outDir", help="Choose the output directory.\nOutput will be saved to 'outDir/year/LEP_REG_BIN'")
parser.add_argument("--year", default=[], action="append", required=True, help="Choose the year(s): '2016', '2017', '2018' (REQUIRED). Multiple years work for plotting.")
parser.add_argument("--nCores", type=int, default=8, help="Number of parallel threads")
parser.add_argument("--inputDir", default=None, help="Override input directory")

parser.add_argument("--lep", default=None, required=True, choices=["2los","3l"], help="Choose number of leptons to use (REQUIRED)")
parser.add_argument("--reg", default=None, required=True, choices=["sr","sr_col","cr_dy","cr_tt","cr_vv","cr_ss","cr_wz","appl","appl_col","cr_ss_1F_NoSF","cr_ss_2F_NoSF","cr_ss_1F_SF1","cr_ss_2F_SF2","appl_1F_NoSF","appl_2F_NoSF","appl_3F_NoSF","appl_1F_SF1F","appl_2F_SF2F","appl_col_1F_NoSF","appl_col_2F_NoSF","sr_closure","sr_closure_norm"], help="Choose region to use (REQUIRED)")
parser.add_argument("--bin", default=None, required=True, choices=["low","med","high","ultra"], help="Choose bin to use (REQUIRED)")

parser.add_argument("--signal", action="store_true", default=False, help="Include signal")
parser.add_argument("--signalModel", default="TChiWZ", choices=["TChiWZ","Higgsino","HiggsPMSSM", "T2tt","T2bW"], help="Choose signal model")
parser.add_argument("--reweight", choices=["none","pos","neg","all"], default="none", help="Re-weight signal mll distribution for +/- N1*N2")
parser.add_argument("--data", action="store_true", default=False, help="Include data")
parser.add_argument("--fakes", default="mc", choices=["mc","dd","semidd"], help="Method of estimating fakes. Default = '%(default)s'")
parser.add_argument("--norm", action="store_true", default=False, help="Normalize signal to data")
parser.add_argument("--unc", action="store_true", default=False, help="Include uncertainties")
parser.add_argument("--postfit", default=None, help="Read postfit plot from FitDiagnostics output, format file:shapes_fit_b for bkg-only, file:shapes_fit_s for s+b fit (must plot only the fitted variable)")
parser.add_argument("--inPlots", default=None, help="Select plots, separated by commas, no spaces")
parser.add_argument("--exPlots", default=None, help="Exclude plots, separated by commas, no spaces")

parser.add_argument("--doWhat", default="plots", choices=["plots","cards"], help="Choose running mode. Default = '%(default)s'")
# only valid for doWhat=='cards'
parser.add_argument("--signalMasses", default=None, help="Select only these signal samples (e.g 'signal_TChiWZ_100_70+'), comma separated. Use only when doing 'cards'")
parser.add_argument("--allowRest", action="store_true", default=False, help="Allow for other non-signal processes")
parser.add_argument("--asimov", dest="asimov", default=None, help="Use an Asimov dataset of the specified kind: including signal ('signal','s','sig','s+b') or background-only ('background','bkg','b','b-only')")
parser.add_argument("--justdump", action="store_true", default=False, help="Pass justdump to makeShapeCardsNew.py")
parser.add_argument("--preskim", action="store_true", default=False, help="Do pre-skim to temporary directory")
parser.add_argument("--keep-preskim", action="store_true", default=False, help="Do not clean pre-skim temporary directory")
parser.add_argument("--infile", action="store_true", default=False, help="Start from existing bare input file")

args = parser.parse_args()
ODIR=args.outDir
YEARS=args.year
conf="%s_%s_%s"%(args.lep,args.reg,args.bin)

for years in YEARS:
    if years not in ("2016","2017","2018"): raise RuntimeError("Unknown year: Please choose '2016', '2017', '2018'")
if (args.signalMasses or args.asimov or args.justdump) and args.doWhat != "cards": raise RuntimeError("Option to be used only with the 'cards' option!")
#if args.fakes == "semidd" and "cr" in args.reg and args.reg != "cr_ss": print "No semidd fakes in the CRs! Using dd fakes..."

lumis = {
'2016': '35.9', # '33.2' for low MET
'2017': '41.5', # '36.7' for low MET
'2018': '59.7', # '59.2' for low MET
}
YEAR = ""
LUMI= " -l "
for years in YEARS:
    YEAR += "%s,"%(years)
    LUMI += "%s,"%(lumis[years])
YEAR = YEAR.rstrip(",")
LUMI = LUMI.rstrip(",")

submit = '{command}' 

#P0="root://eoscms.cern.ch//eos/cms/store/cmst3/group/tthlep/peruzzi/NanoTrees_SOS_070220_v6_skim_2lep_met125/"
P0="root://eoscms.cern.ch//eos/cms/store/user/evourlio/NanoTrees_SOS_070220_v6_skim_2lep_met125/"
if args.inputDir: P0=args.inputDir+'/'
nCores = args.nCores
TREESALL = " --Fs {P}/recleaner/ --FMCs {P}/bTagWeights --FMCs {P}/jetmetUncertainties -P "+P0+"%s "%(YEARS[0] if len(YEARS)==1 else "")+"--readaheadsz 20000000 "
# For cards only, no need fr multiple year support
TREESALLSKIM = TREESALL + " --FMCs {P}/signalWeights "
if YEAR == "2016" and args.signalModel=='TChiWZ': TREESALLSKIM = TREESALLSKIM + " --FMCs {P}/isrWeights "


def base(selection):
    plotting=''
    CORE=TREESALL
    CORE+=" -f -j %d --split-factor=-1 --year %s --s2v -L susy-sos/functionsSOS.cc -L susy-sos/functionsSF.cc --tree NanoAOD --mcc susy-sos/mcc_sos_allYears.txt %s "%(nCores,YEAR,LUMI)
    RATIO= " --maxRatioRange 0.6  1.99 --ratioYNDiv 210 "
    RATIO2=" --showRatio --attachRatioPanel --fixRatioRange "
    LEGEND=" --legendColumns 3 --legendWidth 0.62 "
    LEGEND2=" --legendFontSize 0.032 "
    SPAM=" --noCms --topSpamSize 1.1 --lspam '#scale[1.1]{#bf{CMS}} #scale[0.9]{#it{Preliminary}}' "
    if args.signal:
        CORE+=" --xp signal\(\?\!_"+args.signalModel+"\).* "
        CORE+=" --xp signal.*\(_pos\|_neg\) " if args.reweight=="none" else " --xp signal.*\(\?\<\!_pos\) " if args.reweight=="pos" else " --xp signal.*\(\?\<\!_neg\) " if args.reweight=="neg" else ""
    else: CORE+=" --xp signal.* "
    if args.doWhat == "plots": 
        CORE+=RATIO+RATIO2+LEGEND+LEGEND2+SPAM+" --showMCError --perBin "
        if args.signal: CORE+=" --noStackSig --showIndivSigs " if ((not args.postfit) or (':shapes_fit_s' not in args.postfit)) else " "

    wBG = " '1.0' "
    wPrefire = ""   
    if args.signalModel not in ["HiggsPMSSM", "T2tt","T2bW"] and (YEAR=="2016" or YEAR=="2017"): wPrefire = "L1PreFiringWeight_Nom*" # Other FastSIM samples should be added here
    if selection=='2los':
        GO="%s susy-sos/mca/mca-2los.txt susy-sos/2los_cuts.txt "%(CORE)
        if args.doWhat in ["plots"]: plotting+=" susy-sos/2los_plots.txt "
        if args.doWhat in ["cards"]:
            if args.reg == "sr_col": plotting+=" LepGood1_pt [3.5,8,12,16,20,25,30] "
            elif args.bin == "low": plotting+=" 'mass_2(LepGood1_pt, LepGood1_eta, LepGood1_phi, LepGood1_mass, LepGood2_pt, LepGood2_eta, LepGood2_phi, LepGood2_mass)' [4,10,20,30,50] "
            else: plotting+=" 'mass_2(LepGood1_pt, LepGood1_eta, LepGood1_phi, LepGood1_mass, LepGood2_pt, LepGood2_eta, LepGood2_phi, LepGood2_mass)' [1,4,10,20,30,50] "

        wBG = " '{}puWeight*eventBTagSF*triggerSF(muDleg_SF(year,LepGood1_pt,LepGood1_eta,LepGood2_pt,LepGood2_eta), MET_pt, metmm_pt(LepGood1_pdgId,LepGood1_pt,LepGood1_phi,LepGood2_pdgId,LepGood2_pt,LepGood2_phi,MET_pt,MET_phi), year)*lepSF(LepGood1_pt,LepGood1_eta,LepGood1_pdgId,year)*lepSF(LepGood2_pt,LepGood2_eta,LepGood2_pdgId,year)' ".format(wPrefire)
        GO="%s -W %s --binname sos_%s "%(GO,wBG,conf)

    elif selection=='3l':
        GO="%s susy-sos/mca/mca-3l.txt susy-sos/3l_cuts.txt "%(CORE)
        if args.doWhat in ["plots"]: plotting+=" susy-sos/3l_plots.txt "
        if args.doWhat in ["cards"]:
            if args.bin == "low": plotting+="  minMllSFOS [4,10,20,30,50] "
            else: plotting+="  minMllSFOS [1,4,10,20,30,50] "
        
        wBG = " '{}puWeight*eventBTagSF*triggerSF(muDleg_SF(year,LepGood1_pt,LepGood1_eta,LepGood2_pt,LepGood2_eta,0,LepGood3_pt,LepGood3_eta,lepton_permut(LepGood1_pdgId,LepGood2_pdgId,LepGood3_pdgId)), MET_pt, metmmm_pt(LepGood1_pt, LepGood1_phi, LepGood2_pt, LepGood2_phi, LepGood3_pt, LepGood3_phi, MET_pt, MET_phi, lepton_Id_selection(LepGood1_pdgId,LepGood2_pdgId,LepGood3_pdgId)), year)*lepSF(LepGood1_pt,LepGood1_eta,LepGood1_pdgId,year)*lepSF(LepGood2_pt,LepGood2_eta,LepGood2_pdgId,year)*lepSF(LepGood3_pt,LepGood3_eta,LepGood3_pdgId,year)' ".format(wPrefire)
        GO="%s -W %s --binname sos_%s "%(GO,wBG,conf)

    else:
        raise RuntimeError('Unknown selection')

    return GO,plotting

def promptsub(x):
    procs = [ '' ]
    if args.doWhat == "cards": procs += ['_FRe_norm_Up','_FRe_norm_Dn','_FRe_pt_Up','_FRe_pt_Dn','_FRe_be_Up','_FRe_be_Dn','_FRm_norm_Up','_FRm_norm_Dn','_FRm_pt_Up','_FRm_pt_Dn','_FRm_be_Up','_FRm_be_Dn']
    return x + ' '.join(["--plotgroup data_fakes%s+='.*_promptsub%s'"%(x,x) for x in procs])+" --neglist '.*_promptsub.*' "

def procs(GO,mylist):
    return GO+' '+" ".join([ '-p %s'%l for l in mylist ])

def sigprocs(GO,mylist):
    return procs(GO,mylist)+' --showIndivSigs --noStackSig'

def createPath(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def formn2c1(old_str):
    sn2, sc1 = old_str
    n2 = float(sn2.replace('p','.'))
    n1 = float(sc1.replace('p','.'))
    c1 = n2 - 0.5*(n2-n1)
    ret = [sn2,"{:.2f}".format(c1).replace('.','p')]
    return ret

def runIt(GO,plotting,name):
    if args.doWhat == "plots":  
        name=name+"_"+args.fakes
        if not args.reweight=="none": name=name+"_"+args.reweight
        if args.data: name=name+"_data"
        if args.norm: name=name+"_norm"

        GO+=plotting
        ret = submit.format(command=' '.join(['python mcPlots.py',"--pdir %s/%s/%s"%(ODIR,YEAR.replace(",","-"),name),GO,' '.join(['--sP %s'%p for p in (args.inPlots.split(",") if args.inPlots is not None else []) ]),' '.join(['--xP %s'%p for p in (args.exPlots.split(",") if args.exPlots is not None else []) ])]))

    elif args.doWhat == "cards":
        masspt=''
        if not args.signal: masspt='nosignal'
        else:
            if args.signalMasses:
                for pr in args.signalMasses.split(','):
                    masspt+='_'.join(pr.split('_')[1:])
            else:
                raise RuntimeError('wrong configuration: trying to run a mixture of all signals')
        if args.preskim:
            for pr in args.signalMasses.split(','):
                if "TChiWZ" not in pr and "Higgsino" not in pr and "HiggsPMSSM" not in pr and "T2tt" not in pr and "T2bW" not in pr: raise RuntimeError('Unrecognised signal model')
            FILENAME="SMS_TChiWZ"
            GENMODEL = "GenModel_TChiWZ_ZToLL"
            GENMODELSTRING="( " + " || ".join([(GENMODEL+'_%s')%('_'.join(pr.split('_')[2:4])) for pr in args.signalMasses.split(',')]) + " )"
            if "Higgsino" in pr: 
                FILENAME="SMS_HiggsinoN2N1,SMS_HiggsinoN2C1"
                GENMODELSTRING = " || ".join(['AltBranch$(GenModel_SMS_N2C1_higgsino_%s,0)'%('_'.join(formn2c1(pr.split('_')[2:4]))) for pr in args.signalMasses.split(',')])
                GENMODELSTRING+= " || " + " || ".join(['AltBranch$(GenModel_SMS_N2N1_higgsino_%s,0)'%('_'.join(pr.split('_')[2:4])) for pr in args.signalMasses.split(',')])
                GENMODELSTRING = "( " + GENMODELSTRING + " )"
            if "T2tt" in pr:
                FILENAME="SMS_T2tt"
                GENMODEL = "GenModel_T2tt_dM_10to80_2Lfilter"
                GENMODELSTRING="( " + " || ".join([(GENMODEL+'_%s')%('_'.join(pr.split('_')[2:4])) for pr in args.signalMasses.split(',')]) + " )"
            if "HiggsPMSSM" in pr:
                FILENAME="SMS_HiggsinoPMSSM"
                GENMODEL = "GenModel_MSSM_higgsino"
                GENMODELSTRING="( " + " || ".join([(GENMODEL+'_%s')%('_'.join(pr.split('_')[2:4])) for pr in args.signalMasses.split(',')]) + " )"
            if "T2bW" in pr:
                FILENAME="SMS_T2bW"
                GENMODEL = "GenModel_T2bW_X05_dM_10to80_genHT_160_genMET_80"
                GENMODELSTRING="( " + " || ".join([(GENMODEL+'_%s')%('_'.join(pr.split('_')[2:4])) for pr in args.signalMasses.split(',')]) + " )"
            ret = "export MYTEMPSKIMDIR=$(mktemp -d); python skimTreesNew.py --elist myCustomElistForSignal --skim-friends {TREESALLSKIM} -f -j {nCores} --split-factor=-1 --year {YEAR} --s2v --tree NanoAOD -p {FILENAME} susy-sos/mca-includes/mca-skim-{YEAR}.txt susy-sos/skim_true.txt ${{MYTEMPSKIMDIR}}/{YEAR} -A alwaystrue model '{GENMODELSTRING}'".format(**{
                'TREESALLSKIM': TREESALLSKIM,
                'nCores': nCores,
                'YEAR': YEAR,
                'FILENAME': FILENAME,
                'GENMODELSTRING': GENMODELSTRING,
            }).replace("root://eoscms.cern.ch/","")
            print ret
            GO = GO.replace(P0,"${MYTEMPSKIMDIR}/")

        GO+=plotting
        ret = "python makeShapeCardsNew.py {barefile} {justdump} --outdir {outdir} {procsel} --all-processes --amc {asimov} {GO}"
        ret = ret.format(**{
            'barefile': '--infile' if args.infile else '--savefile',
            'justdump': '--justdump' if args.justdump else '',
            'outdir': '/'.join([ODIR,YEAR,name,args.signalMasses.replace(',','_') if args.signalMasses else 'nosignal']),
            'procsel': ("--xp='^signal(?!.*_%s).*'"%masspt if args.allowRest else "-p %s"%args.signalMasses) if args.signalMasses else '',
            'asimov' : "--asimov %s"%args.asimov if args.asimov else '',
            'GO': GO,
        })

    print ret

    if args.preskim and not args.keep_preskim:
        print 'rm -r ${MYTEMPSKIMDIR}'


def add(GO,opt):
    return '%s %s'%(GO,opt)

def setwide(x):
    x2 = add(x,'--wide')
    x2 = x2.replace('--legendWidth 0.35','--legendWidth 0.20')
    return x2

def binChoice(x,torun):
    metBin     = ''
    x2 = add(x,'-E ^eventFilters$ ')
    if '_low' in torun: metBin     = 'metlow'
    elif '_med' in torun:
        metBin     = 'metmed'
        x2 = add(x2,'-X ^mm$ ')
    elif '_high' in torun:
        metBin     = 'methigh'
        x2 = add(x2,'-X ^mm$ ')
    elif '_ultra' in torun:
        metBin  = 'metultra' 
        x2 = add(x2,'-X ^mm$ ')
    if metBin != '': x2 = add(x2,'-E ^'+metBin+'$ -E ^'+metBin+'_trig$ ')

    #if metBinTrig=='': print "\n--- NO TRIGGER APPLIED! ---\n"
    return x2

allow_unblinding = True


if __name__ == '__main__':

    torun = conf

    if (not args.doWhat=="cards" ) and ((not allow_unblinding) and args.data and (not any([re.match(x.strip()+'$',torun) for x in ['.*appl.*','.*cr.*','3l.*_Zpeak.*']]))): raise RuntimeError, 'You are trying to unblind!'


    if '2los_' in torun:
        x,x2 = base('2los')
        x = binChoice(x,torun)

        if args.fakes == "semidd": x = x.replace('susy-sos/mca/mca-2los.txt','susy-sos/mca/semidd_bkg/mca-2los-semidd.txt')
        if args.fakes == "dd": x = x.replace('susy-sos/mca/mca-2los.txt','susy-sos/mca/dd_bkg/mca-2los-dd.txt')
        if 'sr' in torun:
            if not '_low' in torun: x = add(x, "-X ^mll$ -E ^mll_low$ -E ^JPsiVeto$ -X ^pt5sublep$  -E ^mindR$ -X ^ledlepPt$ -E ^ledlepPt3p5$")

            if '_col' in torun:
                x = add(x,"-X ^mT$ -X ^SF$ ")
                if '_med' in torun: 
                     x = add(x,"-X ^pt5sublep$ ")
                     x = x.replace('^metmed$','^metmed_col$')
                if '_high' in torun: 
                     x = add(x,"-X ^pt5sublep$ ")
                     x = x.replace('-E ^methigh$','-E ^methigh_col$')
                if '_ultra' in torun: 
                     x = add(x,"-X ^pt5sublep$ ")
                     x = x.replace('-E ^metultra$','-E ^metultra_col$')
            if args.fakes == "semidd":
                if '_col' in torun: x = add(x,"--mcc susy-sos/fakerate/%s/ScaleFactors_SemiDD/mcc_SF_col_%s.txt "%(args.lep,args.bin))
                else: x = add(x, "--mcc susy-sos/fakerate/%s/ScaleFactors_SemiDD/mcc_SF_appl_%s.txt"%(args.lep,args.bin))                 
                   
            if '_closure' in torun:
                x = x.replace('susy-sos/mca/mca-2los.txt','susy-sos/mca/closure/mca-2los-closure.txt')
                x = add(x,"-X ^metmed$ ")
                x = add(x,"-E ^inclMET_2l$ ")
                x = add(x,"--ratioNums=Fakes_MC --ratioDen=QCDFR_fakes ")
                if '_norm' in torun:
                    x = add(x, "--plotmode=%s "%("norm"))
                else:
                    x = add(x, "--plotmode=%s "%("nostack"))

        if 'appl' in torun:
            if not '_low' in torun: x = add(x, "-X ^mll$ -E ^mll_low$ -E ^JPsiVeto$ -X ^pt5sublep$  -E ^mindR$ -X ^ledlepPt$ -E ^ledlepPt3p5$")

            if  not '_col' in torun:
                if '_med' in torun: x = x.replace('^metmed$', '^metmed_AR$')
                if '_high' in torun: x = x.replace('^methigh$', '^methigh_AR$')
                if '_ultra' in torun: x = x.replace('^metultra$', '^metultra_AR$')

            if '_col' in torun:
                x = add(x,"-X ^mT$ -X ^SF$ ")
                if '_med' in torun: 
                    x = add(x,"-X ^pt5sublep$ ")
                    x = x.replace('^metmed$', '^metmed_col$')
                if '_high' in torun: 
                    x = add(x,"-X ^pt5sublep$ ")
                    x = x.replace('^methigh', '^methigh_col$')
                if '_ultra' in torun: 
                    x = add(x,"-X ^pt5sublep$ ")
                    x = x.replace('^metultra', '^metultra_col$')

            x = add(x,"-X ^twoTight$ ")
            if '1F_NoSF' in torun:
                x = add(x, "-E ^1LNT$ ")
            elif '2F_NoSF' in torun: 
                x = add(x, "-E ^2LNT$ ")
            elif '1F_SF1F' in torun:
                x = x.replace('susy-sos/mca/mca-2los.txt','susy-sos/mca/semidd_bkg/Tests/mca-2los-1F.txt')
                x = add(x,"--mcc susy-sos/fakerate/%s/ScaleFactors_SemiDD/mcc_SF_appl_%s.txt "%(args.lep,args.bin))
                x = add(x, " -E ^1LNT$ ")
            elif '2F_SF2F' in torun:
                x = x.replace('susy-sos/mca/mca-2los.txt','susy-sos/mca/semidd_bkg/Tests/mca-2los-2F.txt')
                x = add(x,"--mcc susy-sos/fakerate/%s/ScaleFactors_SemiDD/mcc_SF_appl_%s.txt "%(args.lep,args.bin))
                x = add(x, "-E ^2LNT$ ")
            else:
                x = add(x,"-E ^oneNotTight$ ")


        if 'cr_' in torun:
            x = add(x, "-X ^SF$ ")
            x = x.replace('^metmed$', '^metmed_CR$')
            if args.reg != "cr_ss" and args.fakes == "semidd": x = x.replace('susy-sos/mca/semidd_bkg/mca-2los-semidd.txt','susy-sos/mca/dd_bkg/mca-2los-dd.txt')

        if 'cr_dy' in torun:
            if args.fakes == "semidd" or args.fakes == "dd": x = x.replace('susy-sos/mca/dd_bkg/mca-2los-dd.txt','susy-sos/mca/dd_bkg/mca-2los-dd-DY.txt')
            x = add(x,"-X ^ledlepPt$ ")
            x = add(x,"-I ^mtautau$ ")
            if not '_low' in torun: x = add(x, "-X ^mll$ -E ^mll_low$ -E ^JPsiVeto$ -X ^pt5sublep$ -E ^mindR$ -E ^CRDYledlepPt_low$ ")
            else: x = add(x,"-E ^CRDYledlepPt$ ")

        if 'cr_tt' in torun:
            x = add(x,"-X ^ledlepPt$ -X ^bveto$ -X ^mT$ ")
            x = add(x,"-E ^btag$ ")
            if not '_low' in torun: x = add(x, "-X ^mll$ -E ^mll_low$ -E ^JPsiVeto$ -X ^pt5sublep$ -E ^mindR$ -E ^CRTTledlepPt_low$ ")
            else: x = add(x,"-E ^CRTTledlepPt$ ")

        if 'cr_vv' in torun:
            x = add(x,"-X ^ledlepPt$ -X ^bveto$ -X ^mT$ ")
            x = add(x,"-E ^CRVVledlepPt$ -E ^CRVVbveto$ -E ^CRVVmT$ ")
            if not '_low' in torun: x = add(x, "-X ^mll$ -E ^mll_low$ -E ^JPsiVeto$ -X ^pt5sublep$ -E ^mindR$ ")

        if 'cr_ss' in torun: # Only 'med' bin exists
            x = add(x, "-X ^mll$ -E ^mll_low$ -E ^JPsiVeto$ -X ^pt5sublep$  -E ^mindR$ -X ^ledlepPt$ -E ^ledlepPt3p5$")

            x = add(x,"-X ^mT$ -X ^pt5sublep$ ")
            x = add(x,"-I ^OS$  ")
            if '1F_NoSF' in torun:
                x = add(x, "-E ^1LNT$ -X ^twoTight$" )
            elif '2F_NoSF' in torun:
                x = add(x, "-E ^2LNT$ -X ^twoTight$" )    
            elif '1F_SF1' in torun:
                x = x.replace('susy-sos/mca/mca-2los.txt','susy-sos/mca/semidd_bkg/Tests/mca-2los-1F.txt')
                x = add(x,"--mcc susy-sos/fakerate/%s/ScaleFactors_SemiDD/mcc_SF_cr_ss.txt "%(args.lep))
                x = add(x, "-E ^1LNT$ -X ^twoTight$" )
            elif '2F_SF2' in torun:
                x = x.replace('susy-sos/mca/mca-2los.txt','susy-sos/mca/semidd_bkg/Tests/mca-2los-2F.txt')
                x = add(x,"--mcc susy-sos/fakerate/%s/ScaleFactors_SemiDD/mcc_SF_cr_ss.txt "%(args.lep))
                x = add(x, "-E ^2LNT$ -X ^twoTight$")
            if args.fakes == "semidd": x = add(x, "--mcc susy-sos/fakerate/%s/ScaleFactors_SemiDD/mcc_SF_cr_ss.txt"%(args.lep))


    elif '3l_' in torun:
        x,x2 = base('3l')
        x = binChoice(x,torun)

        if args.fakes == "semidd": x = x.replace('susy-sos/mca/mca-3l.txt','susy-sos/mca/semidd_bkg/mca-3l-semidd.txt')    
        if args.fakes == "dd": x = x.replace('susy-sos/mca/mca-3l.txt','susy-sos/mca/dd_bkg/mca-3l-dd.txt') 

        if 'sr' in torun:
            if not '_low' in torun: x = add(x, "-X ^maxMll$ -X ^minMll$ -E ^minMll_low$ -E ^JPsiVeto$ -X ^pt5sublep$  -E ^mindR$ -X ^ledlepPt$ -E ^ledlepPt3p5$")
            if args.fakes == "semidd": x = add(x, "--mcc susy-sos/fakerate/%s/ScaleFactors_SemiDD/mcc_SF_%s.txt"%(args.lep,args.bin))

        if 'appl' in torun:
            if not '_low' in torun: x = add(x, "-X ^maxMll$ -X ^minMll$ -E ^minMll_low$ -E ^JPsiVeto$ -X ^pt5sublep$  -E ^mindR$ -X ^ledlepPt$ -E ^ledlepPt3p5$")
            x = add(x,"-X ^threeTight$ ")
            if '1F_NoSF' in torun:
                x = add(x, "-E ^1LNT$ ")
            elif '2F_NoSF' in torun:
                x = add(x, "-E ^2LNT$ ")
            elif '3F_NoSF' in torun:
                x = add(x, "-E ^3LNT$ ")
            else:
                x = add(x,"-E ^oneNotTight$ ")

        if 'cr_wz' in torun:
            if args.fakes == "semidd": x = x.replace('susy-sos/mca/semidd_bkg/mca-3l-semidd.txt','susy-sos/mca/dd_bkg/mca-3l-dd.txt')    
            x = add(x,"-X ^minMll$ -X ^maxMll$ -X ^ledlepPt$ -X ^pt5sublep$ ")
            if not '_low' in torun: x = add(x, "-E ^CRWZmll_low$ -E ^JPsiVeto$ -E ^mindR$ -E ^CRWZPtLep_HighMET$ ")
            else: 
                x = add(x,"-E ^CRWZmll$ -E ^CRWZPtLep_MuMu$ ")
                x = x.replace('-E ^metlow_trig','-E ^metlow_trig_CR')
                x = x.replace('triggerSF','triggerWZSF')



    if not args.data: x = add(x,'--xp data ')
    if args.unc: x = add(x,"--unc susy-sos/systsUnc.txt")
    if args.postfit: x = add(x,"--getHistosFromFile %s/sos_%s"%(args.postfit,conf))+("_%s "%YEARS[0] if len(YEARS)==1 else "")
    if args.norm: x = add(x,"--sp '.*' --scaleSigToData ")

    if '_low' in torun :
        if "cr_wz" not in torun: x = x.replace("35.9","33.2") # 2016
        x = x.replace("41.5","36.7") # 2017
        if "cr_wz" not in torun: x = x.replace("59.7","59.2") # 2018

    runIt(x,x2,'%s'%torun)

