#!/usr/bin/env python
import sys
import re
import os
import errno
import argparse

helpText = "LEP = '2los', '3l'\n\
REG = 'sr', 'sr_col', 'cr_dy', 'cr_tt', 'cr_vv', 'cr_ss','cr_wz', 'appl', 'appl_col',\n\
\t'cr_ss_1F_NoSF', 'cr_ss_2F_NoSF', 'cr_ss_1F_SF1', 'cr_ss_2F_SF2',\n\
\t'appl_1F_NoSF', 'appl_2F_NoSF','appl_3F_NoSF', 'appl_1F_SF1F', 'appl_2F_SF2F',\n\
\t'appl_col_1F_NoSF', 'appl_col_2F_NoSF',\n\
\t'sr_closure', 'sr_closure_norm'\n\
BIN =  'low', 'med', 'high', 'ultra'"
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                 epilog=helpText)
parser.add_argument("outDir", help="Choose the output directory.\nOutput will be saved to 'outDir/year/LEP_REG_BIN'")
parser.add_argument("year", help="Choose the year: '2016', '2017' or '2018'")
parser.add_argument("--nCores", type=int, default=8, help="Number of parallel threads")
parser.add_argument("--inputDir", default=None, help="Override input directory")

parser.add_argument("--lep", default=None, required=True, help="Choose number of leptons to use (REQUIRED)")
parser.add_argument("--reg", default=None, required=True, help="Choose region to use (REQUIRED)")
parser.add_argument("--bin", default=None, required=True, help="Choose bin to use (REQUIRED)")

parser.add_argument("--signal", action="store_true", default=False, help="Include signal")
parser.add_argument("--reweight", choices=["none","pos","neg"], default="none", help="Re-weight signal mll distribution for +/- N1*N2")
parser.add_argument("--data", action="store_true", default=False, help="Include data")
parser.add_argument("--fakes", default="mc", help="Use 'mc', 'dd' or 'semidd' fakes. Default = '%(default)s'")
parser.add_argument("--norm", action="store_true", default=False, help="Normalize signal to data")
parser.add_argument("--unc", action="store_true", default=False, help="Include uncertainties")
parser.add_argument("--inPlots", default=None, help="Select plots, separated by commas, no spaces")
parser.add_argument("--exPlots", default=None, help="Exclude plots, separated by commas, no spaces")
parser.add_argument("--lowmll_LowPt_bothlep", action="store_true", default=False, help="Flag to run with low mll & low lead/sublead lep pt cuts")

parser.add_argument("--doWhat", default="plots", help="Do 'plots' or 'cards'. Default = '%(default)s'")
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
YEAR=args.year
conf="%s_%s_%s"%(args.lep,args.reg,args.bin)

if YEAR not in ("2016","2017","2018"): raise RuntimeError("Unknown year: Please choose '2016', '2017' or '2018'")
if args.lep not in ["2los","3l"]: raise RuntimeError("Unknown choice for LEP option. Please check help" )
if args.reg not in ["sr", "sr_col", "cr_dy", "cr_tt", "cr_vv", "cr_ss", "cr_wz", "appl", "appl_col", "cr_ss_1F_NoSF", "cr_ss_2F_NoSF", "cr_ss_1F_SF1", "cr_ss_2F_SF2", "appl_1F_NoSF", "appl_2F_NoSF","appl_3F_NoSF", "appl_1F_SF1F", "appl_2F_SF2F", "appl_col_1F_NoSF", "appl_col_2F_NoSF", "sr_closure", "sr_closure_norm"]: raise RuntimeError("Unknown choice for REG option. Please check help." )
if args.bin not in [ "low", "med", "high","ultra"]: raise RuntimeError("Unknown choice for BIN option. Please check help." )
if args.fakes not in ["mc", "dd", "semidd"]: raise RuntimeError("Unknown choice for FAKES option. Please check help." )
if args.doWhat not in ["plots", "cards"]: raise RuntimeError("Unknown choice for DOWHAT option. Please check help." ) # More options to be added
if (args.signalMasses or args.asimov or args.justdump) and args.doWhat != "cards": raise RuntimeError("Option to be used only with the 'cards' option!")
#if args.fakes == "semidd" and "cr" in args.reg and args.reg != "cr_ss": print "No semidd fakes in the CRs! Using dd fakes..."
#if (args.lowmll_LowPt_bothlep or args.lowmll_NominalPt_bothlep) and args.bin == "low": print "No low Mll extension for low MET! Using nominal selection..."

lumis = {
'2016': '35.9', # '33.2' for low MET
'2017': '41.5', # '36.7' for low MET
'2018': '59.7', # '59.2' for low MET
}
LUMI= " -l %s "%(lumis[YEAR])
submit = '{command}' 

P0="root://eoscms.cern.ch//eos/cms/store/cmst3/group/tthlep/peruzzi/NanoTrees_SOS_070220_v6_skim_2lep_met125/"

if args.inputDir: P0=args.inputDir+'/'
nCores = args.nCores
TREESALL = " --Fs {P}/recleaner --FMCs {P}/bTagWeights --FMCs {P}/jetmetUncertainties -P "+P0+"%s "%(YEAR)+"--readaheadsz 20000000 "
TREESALLSKIM = TREESALL + " --FMCs {P}/signalWeights "

def base(selection):
    plotting=''
    CORE=TREESALL
    CORE+=" -f -j %d --split-factor=-1 --year %s --s2v -L susy-sos/functionsSOS.cc -L susy-sos/functionsSF.cc --tree NanoAOD --mcc susy-sos/mcc_sos.txt --mcc susy-sos/mcc_triggerdefs.txt %s "%(nCores,YEAR,LUMI) # --neg"
    if YEAR == "2017": CORE += " --mcc susy-sos/mcc_METFixEE2017.txt "
    RATIO= " --maxRatioRange 0.6  1.99 --ratioYNDiv 210 "
    RATIO2=" --showRatio --attachRatioPanel --fixRatioRange "
    LEGEND=" --legendColumns 3 --legendWidth 0.62 "
    LEGEND2=" --legendFontSize 0.032 "
    SPAM=" --noCms --topSpamSize 1.1 --lspam '#scale[1.1]{#bf{CMS}} #scale[0.9]{#it{Preliminary}}' "
    if not args.signal:
        CORE+=" --xp signal.* "
    if args.doWhat == "plots": 
        CORE+=RATIO+RATIO2+LEGEND+LEGEND2+SPAM+" --showMCError "
        if args.signal: CORE+=" --noStackSig --showIndivSigs "

    wBG = " '1.0' "
    if selection=='2los':
         GO="%s susy-sos/mca/mca-2los-%s.txt susy-sos/2los_cuts.txt "%(CORE, YEAR)
         if args.doWhat in ["plots"]: plotting+=" susy-sos/2los_plots.txt "
         if args.doWhat in ["cards"]:
             if args.lowmll_LowPt_bothlep : plotting+=" 'mass_2(LepGood1_pt, LepGood1_eta, LepGood1_phi, LepGood1_mass, LepGood2_pt, LepGood2_eta, LepGood2_phi, LepGood2_mass)' [1,4,10,20,30,50] "
             else: plotting+=" 'mass_2(LepGood1_pt, LepGood1_eta, LepGood1_phi, LepGood1_mass, LepGood2_pt, LepGood2_eta, LepGood2_phi, LepGood2_mass)' [4,10,20,30,50] "

         wBG = " 'puWeight*eventBTagSF*triggerSF(muDleg_SF(%s,LepGood1_pt,LepGood1_eta,LepGood2_pt,LepGood2_eta), MET_pt, metmm_pt(LepGood1_pdgId,LepGood1_pt,LepGood1_phi,LepGood2_pdgId,LepGood2_pt,LepGood2_phi,MET_pt,MET_phi), %s)*lepSF(LepGood1_pt,LepGood1_eta,LepGood1_pdgId,%s)*lepSF(LepGood2_pt,LepGood2_eta,LepGood2_pdgId,%s)' "%(YEAR,YEAR,YEAR,YEAR)
         GO="%s -W %s --binname sos_%s "%(GO,wBG,conf)

    elif selection=='3l':
        GO="%s susy-sos/mca/mca-3l-%s.txt susy-sos/3l_cuts.txt "%(CORE,YEAR)
        if args.doWhat in ["plots"]: plotting+=" susy-sos/3l_plots.txt "
        if args.doWhat in ["cards"]:
            if args.lowmll_LowPt_bothlep : plotting+="  minMllSFOS [1,4,10,20,30,50] "
            else: plotting+="  minMllSFOS [4,10,20,30,50] "
        
        wBG = " 'puWeight*eventBTagSF*triggerSF(muDleg_SF(%s,LepGood1_pt,LepGood1_eta,LepGood2_pt,LepGood2_eta,0,LepGood3_pt,LepGood3_eta,lepton_permut(LepGood1_pdgId,LepGood2_pdgId,LepGood3_pdgId)), MET_pt, metmmm_pt(LepGood1_pt, LepGood1_phi, LepGood2_pt, LepGood2_phi, LepGood3_pt, LepGood3_phi, MET_pt, MET_phi, lepton_Id_selection(LepGood1_pdgId,LepGood2_pdgId,LepGood3_pdgId)), %s)*lepSF(LepGood1_pt,LepGood1_eta,LepGood1_pdgId,%s)*lepSF(LepGood2_pt,LepGood2_eta,LepGood2_pdgId,%s)*lepSF(LepGood3_pt,LepGood3_eta,LepGood3_pdgId,%s)' "%(YEAR,YEAR,YEAR,YEAR,YEAR)
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

def runIt(GO,plotting,name):
    if not args.doWhat == "cards" : name=name+"_"+args.fakes
    if args.data and not args.doWhat == "cards" : name=name+"_data"
    if args.norm: name=name+"_norm"

    if args.doWhat == "plots":  
        GO+=plotting
        ret = submit.format(command=' '.join(['python mcPlots.py',"--pdir %s/%s/%s"%(ODIR,YEAR,name),GO,' '.join(['--sP %s'%p for p in (args.inPlots.split(",") if args.inPlots is not None else []) ]),' '.join(['--xP %s'%p for p in (args.exPlots.split(",") if args.exPlots is not None else []) ])]))

    elif args.doWhat == "cards":
        masspt=''
        if not args.signal: masspt='nosignal'
        else:
            if args.signalMasses:
                for pr in args.signalMasses.split(','):
                    masspt+='_'.join(pr.split('_')[-3:])
            else:
                raise RuntimeError('wrong configuration: trying to run a mixture of all signals')
        if args.preskim:
            for pr in args.signalMasses.split(','):
                if 'TChiWZ' not in pr: raise
            FILENAME="SMS_TChiWZ"
            GENMODELSTRING="( " + " || ".join(['GenModel_TChiWZ_ZToLL_%s'%('_'.join(pr.split('_')[2:4])) for pr in args.signalMasses.split(',')]) + " )"
            ret = "export MYTEMPSKIMDIR=$(mktemp -d); python skimTreesNew.py --elist myCustomElistForSignal --skim-friends {TREESALLSKIM} -f -j {nCores} --split-factor=-1 --year {YEAR} --s2v --tree NanoAOD -p {FILENAME} susy-sos/mca-includes/{YEAR}/mca-skim-{YEAR}.txt susy-sos/skim_true.txt ${{MYTEMPSKIMDIR}}/{YEAR} -A alwaystrue model '{GENMODELSTRING}'".format(**{
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
            'outdir': '/'.join([ODIR,YEAR,name,masspt]),
            'procsel': ("--xp='^signal_(?!.*%s).*'"%args.signalMasses if args.allowRest else "-p %s"%args.signalMasses) if args.signalMasses else '',
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
    metBinTrig = ''
    metBinInf = ''
    metBinSup = ''
    x2 = add(x,'-E ^eventFilters$ ')
    if '_low' in torun:
        metBinTrig = 'metlow'
        metBinInf = 'metlow'
        metBinSup = 'metmed'
    elif '_med' in torun:
        metBinTrig = 'metmed'
        metBinInf = 'metmed'
        metBinSup = 'methigh' if ( ('2los_' in torun) and ('cr_' not in torun) ) else ''
        x2 = add(x2,'-X ^mm$ ')
    elif '_high' in torun:
        metBinTrig = 'methigh'
        metBinInf = 'methigh'
        metBinSup = 'metultra' 
        x2 = add(x2,'-X ^mm$ ')
    elif '_ultra' in torun:
        metBinTrig = 'metultra'
        metBinInf  = 'metultra'
        x2 = add(x2,'-X ^mm$ ')
    if metBinInf != '': x2 = add(x2,'-E ^'+metBinInf+'$ -E ^'+metBinTrig+'_trig$ ')
    if metBinSup != '': x2 = add(x2,'-E ^'+metBinSup+'$ -I ^'+metBinSup+'$ ')

    if metBinTrig=='': print "\n--- NO TRIGGER APPLIED! ---\n"
    return x2

allow_unblinding = False


if __name__ == '__main__':

    torun = conf

    if (not args.doWhat=="cards" ) and ((not allow_unblinding) and args.data and (not any([re.match(x.strip()+'$',torun) for x in ['.*appl.*','.*cr.*','3l.*_Zpeak.*']]))): raise RuntimeError, 'You are trying to unblind!'


    if '2los_' in torun:
        x,x2 = base('2los')
        x = binChoice(x,torun)

        if args.fakes == "semidd": x = x.replace('susy-sos/mca/mca-2los-%s.txt'%(YEAR),'susy-sos/mca/semidd_bkg/mca-2los-%s-semidd.txt'%(YEAR))
        if args.fakes == "dd": x = x.replace('susy-sos/mca/mca-2los-%s.txt'%(YEAR),'susy-sos/mca/dd_bkg/mca-2los-%s-dd.txt'%(YEAR))
        if 'sr' in torun:
            if args.lowmll_LowPt_bothlep and not '_low' in torun: x = add(x, "-X ^mll$ -E ^mll_low$ -E ^JPsiVeto$ -X ^pt5sublep$  -E ^mindR$ -X ^ledlepPt$ -E ^ledlepPt3p5$")

            if '_col' in torun:
                x = add(x,"-X ^mT$ -X ^SF$ ")
                if '_med' in torun: 
                     x = add(x,"-X ^pt5sublep$ ")
                     x = x.replace('^methigh$','^methigh_col$')
                if '_high' in torun: 
                     x = add(x,"-X ^pt5sublep$ ")
                     x = x.replace('-E ^methigh$','-E ^methigh_col$')
                     x = x.replace('^metultra$','^metultra_col$')
                if '_ultra' in torun: 
                     x = add(x,"-X ^pt5sublep$ ")
                     x = x.replace('-E ^metultra$','-E ^metultra_col$')                
            if args.fakes == "semidd":
                if '_col' in torun: x = add(x,"--mcc susy-sos/fakerate/%s/%s/ScaleFactors_SemiDD/mcc_SF_col_%s.txt "%(YEAR,args.lep,args.bin))
                else:
                    if args.lowmll_LowPt_bothlep or '_low' in torun: x = add(x, "--mcc susy-sos/fakerate/%s/%s/ScaleFactors_SemiDD/mcc_SF_appl_%s.txt"%(YEAR,args.lep,args.bin))
                    else:
                        raise RuntimeError('The selection you are trying to plot does not exist!')

            if '_closure' in torun:
                x = x.replace('susy-sos/mca/mca-2los-%s.txt'%(YEAR),'susy-sos/mca/closure/mca-2los-%s-closure.txt'%(YEAR))
                x = add(x,"-X ^metmed$ ")
                x = add(x,"-E ^inclMET_2l$ ")
                x = add(x,"--ratioNums=Fakes_MC --ratioDen=QCDFR_fakes ")
                if '_norm' in torun:
                    x = add(x, "--plotmode=%s "%("norm"))
                else:
                    x = add(x, "--plotmode=%s "%("nostack"))

        if 'appl' in torun:
            if args.lowmll_LowPt_bothlep and not '_low' in torun: x = add(x, "-X ^mll$ -E ^mll_low$ -E ^JPsiVeto$ -X ^pt5sublep$  -E ^mindR$ -X ^ledlepPt$ -E ^ledlepPt3p5$")

            if '_col' in torun:
                x = add(x,"-X ^mT$ -X ^SF$ ")
                if '_med' in torun: 
                    x = add(x,"-X ^pt5sublep$ ")
                    x = x.replace('^methigh$','^methigh_col$')
                if '_high' in torun: 
                    x = add(x,"-X ^pt5sublep$ ")
                    x = x.replace('-E ^methigh$','-E ^methigh_col$')
                    x = x.replace('^metultra$','^metultra_col$')
                if '_ultra' in torun: 
                    x = add(x,"-X ^pt5sublep$ ")
                    x = x.replace('-E ^metultra$','-E ^metultra_col$')

            x = add(x,"-X ^twoTight$ ")
            if '1F_NoSF' in torun:
                x = add(x, "-E ^1LNT$ ")
            elif '2F_NoSF' in torun: 
                x = add(x, "-E ^2LNT$ ")
            elif '1F_SF1F' in torun:
                x = x.replace('susy-sos/mca/mca-2los-%s.txt'%(YEAR),'susy-sos/mca/semidd_bkg/Tests/mca-2los-%s-1F.txt'%(YEAR))
                x = add(x,"--mcc susy-sos/fakerate/%s/%s/ScaleFactors_SemiDD/mcc_SF_appl_%s.txt "%(YEAR,args.lep,args.bin))
                x = add(x, " -E ^1LNT$ ")
            elif '2F_SF2F' in torun:
                x = x.replace('susy-sos/mca/mca-2los-%s.txt'%(YEAR),'susy-sos/mca/semidd_bkg/Tests/mca-2los-%s-2F.txt'%(YEAR))
                x = add(x,"--mcc susy-sos/fakerate/%s/%s/ScaleFactors_SemiDD/mcc_SF_appl_%s.txt "%(YEAR,args.lep,args.bin))
                x = add(x, "-E ^2LNT$ ")
            else:
                x = add(x,"-E ^oneNotTight$ ")


        if 'cr_' in torun:
            x = add(x, "-X ^SF$ ")
            if args.reg != "cr_ss" and args.fakes == "semidd": x = x.replace('susy-sos/mca/semidd_bkg/mca-2los-%s-semidd.txt'%(YEAR),'susy-sos/mca/dd_bkg/mca-2los-%s-dd.txt'%(YEAR))

        if 'cr_dy' in torun:
            if args.fakes == "semidd" or args.fakes == "dd": x = x.replace('susy-sos/mca/dd_bkg/mca-2los-%s-dd.txt'%(YEAR),'susy-sos/mca/dd_bkg/mca-2los-%s-dd-DY.txt'%(YEAR))
            x = add(x,"-X ^ledlepPt$ ")
            x = add(x,"-I ^mtautau$ ")
            x = add(x,"-E ^CRDYledlepPt$ ")

        if 'cr_tt' in torun:
            if '_med' in torun:
                x = add(x,'-X ^pt5sublep$ ')
            x = add(x,"-X ^ledlepPt$ -X ^bveto$ -X ^mT$ ")
            x = add(x,"-E ^CRTTledlepPt$ -E ^btag$ ")

        if 'cr_vv' in torun:
            if '_med' in torun:
                x = add(x,'-X ^pt5sublep$ ')
            x = add(x,"-X ^ledlepPt$ -X ^bveto$ -X ^mT$ ")
            x = add(x,"-E ^CRVVledlepPt$ -E ^CRVVbveto$ -E ^CRVVmT$ ")

        if 'cr_ss' in torun: # Only 'med' bin exists
            if args.lowmll_LowPt_bothlep: x = add(x, "-X ^mll$ -E ^mll_low$ -E ^JPsiVeto$ -X ^pt5sublep$  -E ^mindR$ -X ^ledlepPt$ -E ^ledlepPt3p5$")

            if '_med' in torun:
                x = add(x,'-X ^pt5sublep$ ')
            x = add(x,"-X ^mT$")
            x = add(x,"-I ^OS$  ")
            if '1F_NoSF' in torun:
                x = add(x, "-E ^1LNT$ -X ^twoTight$" )
            elif '2F_NoSF' in torun:
                x = add(x, "-E ^2LNT$ -X ^twoTight$" )    
            elif '1F_SF1' in torun:
                x = x.replace('susy-sos/mca/mca-2los-%s.txt'%(YEAR),'susy-sos/mca/semidd_bkg/Tests/mca-2los-%s-1F.txt'%(YEAR))
                x = add(x,"--mcc susy-sos/fakerate/%s/%s/ScaleFactors_SemiDD/mcc_SF_cr_ss.txt "%(YEAR,args.lep))
                x = add(x, "-E ^1LNT$ -X ^twoTight$" )
            elif '2F_SF2' in torun:
                x = x.replace('susy-sos/mca/mca-2los-%s.txt'%(YEAR),'susy-sos/mca/semidd_bkg/Tests/mca-2los-%s-2F.txt'%(YEAR))
                x = add(x,"--mcc susy-sos/fakerate/%s/%s/ScaleFactors_SemiDD/mcc_SF_cr_ss.txt "%(YEAR,args.lep))
                x = add(x, "-E ^2LNT$ -X ^twoTight$")
            if args.fakes == "semidd" :
                if args.lowmll_LowPt_bothlep: x = add(x, "--mcc susy-sos/fakerate/%s/%s/ScaleFactors_SemiDD/mcc_SF_cr_ss.txt"%(YEAR,args.lep))
                else:
                    raise RuntimeError('The selection you are trying to plot does not exist!')


    elif '3l_' in torun:
        x,x2 = base('3l')
        x = binChoice(x,torun)

        if args.fakes == "semidd": x = x.replace('susy-sos/mca/mca-3l-%s.txt'%(YEAR),'susy-sos/mca/semidd_bkg/mca-3l-%s-semidd.txt'%(YEAR))    
        if args.fakes == "dd": x = x.replace('susy-sos/mca/mca-3l-%s.txt'%(YEAR),'susy-sos/mca/dd_bkg/mca-3l-%s-dd.txt'%(YEAR))    

        if 'sr' in torun:
            if args.lowmll_LowPt_bothlep and not '_low' in torun: x = add(x, "-X ^minMll$ -E ^minMll_low$ -E ^JPsiVeto$ -X ^pt5sublep$  -E ^mindR$ -X ^ledlepPt$ -E ^ledlepPt3p5$")

            if '_med' in torun: x = add(x,'-X ^maxMll$ ')
            if args.fakes == "semidd":
                if args.lowmll_LowPt_bothlep or '_low' in torun: x = add(x, "--mcc susy-sos/fakerate/%s/%s/ScaleFactors_SemiDD/mcc_SF_%s.txt"%(YEAR,args.lep,args.bin))
                else:
                    raise RuntimeError('The selection you are trying to plot does not exist!')

        if 'appl' in torun:
            if args.lowmll_LowPt_bothlep and not '_low' in torun: x = add(x, "-X ^minMll$ -E ^minMll_low$ -E ^JPsiVeto$ -X ^pt5sublep$  -E ^mindR$ -X ^ledlepPt$ -E ^ledlepPt3p5$")
            if '_med' in torun: x = add(x,'-X ^maxMll$ ')
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
            if args.fakes == "semidd": x = x.replace('susy-sos/mca/semidd_bkg/mca-3l-%s-semidd.txt'%(YEAR),'susy-sos/mca/dd_bkg/mca-3l-%s-dd.txt'%(YEAR))    
            x = add(x,"-X ^minMll$ -X ^maxMll$ -X ^ledlepPt$ -X ^pt5sublep$ ")
            x = add(x,"-E ^CRWZmll$ ")
            if '_low' in torun: 
                x = add(x,"-E ^CRWZPtLep_MuMu$ ")
                x = x.replace('-E ^metlow_trig','-E ^metlow_trig_CR')
                x = x.replace('triggerSF','triggerWZSF')
            if '_med' in torun: x = add(x,"-E ^CRWZPtLep_HighMET$ ")


    if not args.data: x = add(x,'--xp data ')
    if args.unc: x = add(x,"--unc susy-sos/systsUnc.txt")
    if args.norm: x = add(x,"--sp '.*' --scaleSigToData ")

    if '_low' in torun :
        if YEAR=="2016" and "cr_wz" not in torun: x = x.replace(LUMI," -l 33.2 ")
        if YEAR=="2017": x = x.replace(LUMI," -l 36.7 ")
        if YEAR=="2018" and "cr_wz" not in torun: x = x.replace(LUMI," -l 59.2 ")

    runIt(x,x2,'%s'%torun)

