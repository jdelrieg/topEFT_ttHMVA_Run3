import os
import re
import glob
import array
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--indir", default=[], action="append", required=True, help="Choose the input directories")
parser.add_argument("--outdir", default="susy-sos/scanPlots/", help="Choose the output directory. Default='%(default)s'")
parser.add_argument("--tag", default=[], action="append", help="Choose the tags to plot. Default=['all','2lep','3lep']")
parser.add_argument("--savefmts", default=[], action="append", help="Choose save formats for plots. Default=['.pdf','.png','.jpg','.root','.C']")
parser.add_argument("--reweight", default=[], action="append", help="Choose the signal mll reweight scenarios to plot. Default=['none']")
parser.add_argument("--signalModel", default="TChiWZ", choices=["TChiWZ","Higgsino","T2tt"], help="Signal model to consider")
parser.add_argument("--unblind", action='store_true', default=False, help="Run unblinded scans")
args = parser.parse_args()


if len(args.indir) == 0: raise RuntimeError("No input directories given!")
if len(args.tag) == 0: args.tag = ['all','2lep','3lep']
if len(args.reweight) == 0: args.reweight = ['none']
if len(args.savefmts) == 0: args.savefmts = ['.pdf','.png','.jpg','.root','.C']
#if args.signalModel == "Higgsino": args.reweight = ['neg']

import ROOT
from ROOT import *

logy=False
#logy=True

# Legend info
moreText = ""
if args.signalModel == "TChiWZ": moreText = "pp #rightarrow #tilde{#chi}_{1}^{#pm}#tilde{#chi}_{2}^{0} #rightarrow WZ#tilde{#chi}^{0}_{1}#tilde{#chi}^{0}_{1}, NLO-NLL excl."
elif args.signalModel=="T2tt": moreText = "pp #rightarrow #tilde{t}#tilde{t}, #tilde{t} #rightarrow bW#tilde{#chi}^{0}_{1}, NLO-NLL excl."
elif args.signalModel == "Higgsino": moreText = "pp #rightarrow #tilde{#chi}_{1}^{#pm}#tilde{#chi}_{2}^{0}, #tilde{#chi}_{2}^{0}#tilde{#chi}_{2}^{0}, NLO-NLL excl."
moreText2 = "median expected upper limit on signal strength at 95% CL"
cmsText               = "#bf{CMS} Preliminary"
cmsTextFont           = 52  
cmsTextSize           = 0.55
cmsTextOffset         = 0.1
lumiText              = "137 fb^{-1} (13 TeV)"
lumiTextFont          = 42
lumiTextSize          = 0.45
lumiTextOffset        = 0.2
leg_ylo=50.
leg_nlines=3

# Plot range
range_xlo=297. if args.signalModel=="T2tt" else 100.
range_xhi=653. if args.signalModel=="T2tt" else 250. if args.signalModel=="Higgsino" else 300.
range_ylo=10. if args.signalModel=="T2tt" else 3.5
range_yhi=61.5

if logy:
    range_yhi=350.
    leg_ylo=100.

def mass_from_str(s):
    return float(s.replace('p','.'))

class Limit:
    def __init__(self,fname):
        self.obs = None
        self.exp = {}
        if not os.path.exists(fname): return
        f = ROOT.TFile.Open(fname)
        if f:
            tree = f.Get('limit')
            if not tree: return
            self.exp = {}
            translate = {0.02500000037252903: -2, 0.1599999964237213: -1, 0.50: 0, 0.8399999737739563: 1, 0.9750000238418579: 2}
            for ev in tree:
                if ev.quantileExpected==-1:
                    self.obs = ev.limit
                else:
                    self.exp[translate[ev.quantileExpected]] = ev.limit

class MLFit:
    def __init__(self,fname,frname):
        self.nuisances = {}
        self.mu = None
        if not os.path.exists(fname): return
        f = ROOT.TFile.Open(fname)
        if f:
            pars = f.Get(frname)
            if not pars: return
            pars_f = pars.floatParsFinal()
            for i in xrange(pars_f.getSize()):
                x = pars_f[i]
                if x.GetName()!='r':
                    self.nuisances[x.GetName()] = (x.getVal(),x.getError())
                else:
                    self.mu = (x.getVal(), x.getError(), (x.getErrorLo(),x.getErrorHi()))

class Significance:
    def __init__(self,fname):
        self.val = None
        if not os.path.exists(fname): return
        f = ROOT.TFile.Open(fname)
        if f:
            tree = f.Get('limit')
            if not tree: return
            for ev in tree:
                if ev.quantileExpected==-1: self.val = ev.limit

class SignalPoint:
    def __init__(self,indir,tag='all',unblind=False):
        self.modname = indir.split('/')[-1]
        self.m1, self.m2 = map(lambda x: mass_from_str(x), self.modname.split('_')[-2:])
        self.indir = indir
        self.tag = tag
        self.unblind = unblind
        self.parse()

    def parse(self):
        self.limit = Limit(self.indir+'/higgsCombine_%s_%s_blind.AsymptoticLimits.mH%d.root'%(self.modname,self.tag,int(self.m1)))
#        self.signif_aprio = Significance(self.indir+'/higgsCombine_%s_%s_exp_aprio.Significance.mH%d.root'%(self.modname,self.tag,int(self.m1))).val
#        self.mlfit_aprio_b = MLFit(self.indir+'/fitDiagnostics_%s_%s_aprio_bonly.root'%(self.modname,self.tag),'fit_b')
#        self.mlfit_aprio_s = MLFit(self.indir+'/fitDiagnostics_%s_%s_aprio_bonly.root'%(self.modname,self.tag),'fit_s')
        if self.unblind:
            self.limit = Limit(self.indir+'/higgsCombine_%s_%s_obs.AsymptoticLimits.mH%d.root'%(self.modname,self.tag,int(self.m1)))
#            self.signif = Significance(self.indir+'/higgsCombine_%s_%s_obs.Significance.mH%d.root'%(self.modname,self.tag,int(self.m1))).val
#            self.signif_apost = Significance(self.indir+'/higgsCombine_%s_%s_exp_apost.Significance.mH%d.root'%(self.modname,self.tag,int(self.m1))).val
#            self.mlfit_b = MLFit(self.indir+'/fitDiagnostics_%s_%s_obs.root'%(self.modname,self.tag),'fit_b')
#            self.mlfit_s = MLFit(self.indir+'/fitDiagnostics_%s_%s_obs.root'%(self.modname,self.tag),'fit_s')

class LimitPoint:
    def __init__(self,mass, Dm, vals):
        self.mass = mass
        self.Dm = Dm
        self.vals = vals

def getLimitHists(files, tag):
    limits=[]
    for f in files:
        mass = '%d_%d'%(f.m1,f.m2)
        massH = f.m1
        massL = f.m1-f.m2
        vals = {}
        if f.limit.exp:
            vals.update(f.limit.exp)
        if f.limit.obs:
            vals[9] = f.limit.obs
        lim = LimitPoint(massH, massL, vals)
        limits.append(lim)

    hs={}
    vars_to_plot = [0,1,-1,2,-2]
    if args.unblind: vars_to_plot.append(9)
    for var in vars_to_plot:
        g = TGraph2D(len(limits))
        for i,lim in enumerate(limits):
            if len(lim.vals)<len(vars_to_plot): continue
            g.SetPoint(i,lim.mass,lim.Dm,lim.vals[var])
        g.SetNpx(300)
        g.SetNpy(300)
        h = g.GetHistogram().Clone()
        h.SetTitle('')
        hs[var]=h

    return hs


def plotLimits(limits_hists, limit_labels, label, outdir):

    h_bkgd = limits_hists[0][0].Clone('h_bkgd')
    nlim=len(limits_hists)

    c1=TCanvas()
    c1.SetLeftMargin(0.12)
    c1.SetRightMargin(0.12)
    c1.SetBottomMargin(0.13)

    h_bkgd.SetStats(0)

    h_bkgd.GetXaxis().SetRangeUser(range_xlo,range_xhi)
    h_bkgd.GetYaxis().SetRangeUser(range_ylo,range_yhi)
    h_bkgd.GetZaxis().SetRangeUser(3e-2,70)

    h_bkgd.GetXaxis().SetTitle("m_{#tilde{t}} [GeV]" if args.signalModel=="T2tt" else "m_{#tilde{#chi}_{2}^{0}} [GeV]" if args.signalModel=="Higgsino" else "m_{#tilde{#chi}_{1}^{#pm}}=m_{#tilde{#chi}_{2}^{0}} [GeV]")
    h_bkgd.GetXaxis().SetLabelFont(42)
    h_bkgd.GetXaxis().SetTitleFont(42)
    h_bkgd.GetXaxis().SetLabelSize(0.042)
    h_bkgd.GetXaxis().SetTitleSize(0.052)

    h_bkgd.GetYaxis().SetTitle("#Delta m(#tilde{t}, #tilde{#chi}_{1}^{0}) [GeV]" if args.signalModel=="T2tt" else "#Delta m(#tilde{#chi}_{2}^{0}, #tilde{#chi}_{1}^{0}) [GeV]")
    h_bkgd.GetYaxis().SetTitleOffset(1.10)
    h_bkgd.GetYaxis().SetLabelFont(42)
    h_bkgd.GetYaxis().SetTitleFont(42)
    h_bkgd.GetYaxis().SetLabelSize(0.042)
    h_bkgd.GetYaxis().SetTitleSize(0.052)

    h_bkgd.Draw("colz" if nlim==1 else "axis")

    colz = [ROOT.kRed,ROOT.kBlue]
    for iLim, limit_hists in enumerate(limits_hists):
        for var,lim in limit_hists.iteritems():
            lim.SetContour(1,array.array('d',[1]))
            lim.Draw("CONT3 same")
            lim.SetLineColor(colz[iLim])

        h2lim, h2limP1, h2limM1, h2limP2, h2limM2 = limit_hists[0], limit_hists[1], limit_hists[-1], limit_hists[2], limit_hists[-2]
        if args.unblind:
            h2limObs = limit_hists[9]
            h2limObs.SetLineWidth(2)
            h2limObs.SetLineColor(ROOT.kBlack)
        h2lim.SetLineWidth(2)
        h2limP1.SetLineWidth(1)
        h2limM1.SetLineWidth(1)
        h2limP1.SetLineStyle(2)
        h2limM1.SetLineStyle(2)
        h2limP2.SetLineWidth(1)
        h2limM2.SetLineWidth(1)
        h2limP2.SetLineStyle(3)
        h2limM2.SetLineStyle(3)

    c1.SetLogz()
    c1.SetLogy(logy)
    t = c1.GetTopMargin()
    r = c1.GetRightMargin()
    l = c1.GetLeftMargin()
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(ROOT.kBlack)    
    latex.SetTextFont(lumiTextFont)
    latex.SetTextAlign(31) 
    latex.SetTextSize(lumiTextSize*t)    
    latex.DrawLatex(1-r,1-t+lumiTextOffset*t,lumiText)
    latex.SetTextFont(cmsTextFont)
    latex.SetTextAlign(11) 
    latex.SetTextFont(cmsTextFont)
    latex.SetTextAlign(11) 
    latex.SetTextSize(cmsTextSize*t)    
    latex.DrawLatex(l,1-t+lumiTextOffset*t,cmsText)

    x1 = range_xlo
    x2 = range_xhi
    y1 = leg_ylo
    y2 = range_yhi

    if logy:
        y1 = ROOT.TMath.Log(y1)
        y2 = ROOT.TMath.Log(y2)
    delta = (y2-y1)/leg_nlines
    ylines = [y1+(i+0.5)*delta for i in range(leg_nlines)]
    ylines.reverse()
    if logy:
        y1 = ROOT.TMath.Exp(y1)
        y2 = ROOT.TMath.Exp(y2)
        ylines = [ROOT.TMath.Exp(l) for l in ylines]

    b = TBox(x1,y1,x2,y2)
    b.SetFillColor(ROOT.kWhite)
    b.SetLineColor(ROOT.kBlack)
    b.SetLineWidth(1)
    b.Draw("l")
    c1.Update()
    mT=ROOT.TLatex(x1+4.5,ylines[0], moreText2)
    mT.SetTextFont(42)
    mT.SetTextAlign(12)
    mT.SetTextSize(0.040)
    mT.Draw()
    mT2=ROOT.TLatex(x1+4.5,ylines[1], moreText)
    mT2.SetTextAlign(12)
    mT2.SetTextFont(42)
    mT2.SetTextSize(0.040)
    mT2.Draw()

    spread = delta*0.2
    fudge = delta*0.1
    gl1=TGraph(2)
    gl1.SetPoint(0, x1+4.5, ylines[2]+fudge)
    gl1.SetPoint(1, x1+12.5, ylines[2]+fudge)
    gl1.SetLineColor(colz[0])
    gl1.SetLineStyle(1)
    gl1.SetLineWidth(2)
    gl1.Draw("lsame")

    gl1p=TGraph(2)
    gl1p.SetPoint(0, x1+4.5, ylines[2]+spread+fudge)
    gl1p.SetPoint(1, x1+12.5,ylines[2]+spread+fudge)
    gl1p.SetLineColor(colz[0])
    gl1p.SetLineStyle(2)
    gl1p.SetLineWidth(1)
    gl1p.Draw("lsame")

    gl1m=TGraph(2)
    gl1m.SetPoint(0, x1+4.5, ylines[2]-spread+fudge)
    gl1m.SetPoint(1, x1+12.5,ylines[2]-spread+fudge)
    gl1m.SetLineColor(colz[0])
    gl1m.SetLineStyle(2)
    gl1m.SetLineWidth(1)
    gl1m.Draw("lsame")

    gl2p=TGraph(2)
    gl2p.SetPoint(0, x1+4.5, ylines[2]+2*spread+fudge)
    gl2p.SetPoint(1, x1+12.5,ylines[2]+2*spread+fudge)
    gl2p.SetLineColor(colz[0])
    gl2p.SetLineStyle(3)
    gl2p.SetLineWidth(1)
    gl2p.Draw("lsame")

    gl2m=TGraph(2)
    gl2m.SetPoint(0, x1+4.5, ylines[2]-2*spread+fudge)
    gl2m.SetPoint(1, x1+12.5,ylines[2]-2*spread+fudge)
    gl2m.SetLineColor(colz[0])
    gl2m.SetLineStyle(3)
    gl2m.SetLineWidth(1)
    gl2m.Draw("lsame")

    if args.unblind:
        gl1Obs=TGraph(2)
        gl1Obs.SetPoint(0, x1+74.5, ylines[2]+fudge)
        gl1Obs.SetPoint(1, x1+82.5, ylines[2]+fudge)
        gl1Obs.SetLineColor(ROOT.kBlack)
        gl1Obs.SetLineStyle(1)
        gl1Obs.SetLineWidth(2)
        gl1Obs.Draw("lsame")

    mT3=ROOT.TLatex(x1+16.5,ylines[2], "Expected #pm #sigma_{exp}")
    mT3.SetTextAlign(12)
    mT3.SetTextFont(42)
    mT3.SetTextSize(0.040)
    mT3.Draw()

    if args.unblind:
        mT3a=ROOT.TLatex(x1+86.5,ylines[2], "Observed")
        mT3a.SetTextAlign(12)
        mT3a.SetTextFont(42)
        mT3a.SetTextSize(0.040)
        mT3a.Draw()

    if len(limit_labels):
        XOFF = 100.
        gl2=TGraph(2)
        gl2.SetPoint(0, XOFF+x1+4.5, ylines[2]+fudge)
        gl2.SetPoint(1, XOFF+x1+12.5, ylines[2]+fudge)
        gl2.SetLineColor(colz[0])
        gl2.SetLineWidth(2)
        gl2.Draw("lsame")

        mT4=ROOT.TLatex(XOFF+x1+16.5,ylines[2]+fudge, limit_labels[0])
        mT4.SetTextAlign(12)
        mT4.SetTextFont(42)
        mT4.SetTextSize(0.040)
        mT4.Draw()

    if len(limit_labels)>1:
        XOFF = 150.
        gl3=TGraph(2)
        gl3.SetPoint(0, XOFF+x1+4.5, ylines[2]+fudge)
        gl3.SetPoint(1, XOFF+x1+12.5, ylines[2]+fudge)
        gl3.SetLineColor(colz[1])
        gl3.SetLineWidth(2)
        gl3.Draw("lsame")

        mT5=ROOT.TLatex(XOFF+x1+16.5,ylines[2]+fudge, limit_labels[1])
        mT5.SetTextAlign(12)
        mT5.SetTextFont(42)
        mT5.SetTextSize(0.040)
        mT5.Draw()

    os.system("mkdir -p %s"%outdir)
    for fmt in args.savefmts:
        c1.SaveAs("%s/h2lim_%s%s"%(outdir,label+logy*('_log'),fmt))


def run(indirs,tag,label,outdir):
    dirs=glob.glob(indirs)
    points = {}
    for d in dirs:
        x = SignalPoint(d,tag,args.unblind)
        if x: points[(x.m1,x.m2)] = x
    print 'Found %d files'%len(points)
    if len(points)==0: raise RuntimeError("No points found")

    lims = getLimitHists(points.values(),tag)
    plotLimits([lims], [], label, outdir)

def runMLL(indirs,tag,label,outdir):
    limCurves=[]
    lim_labels=['N1*N2>0','N1*N2<0']

    for mll in args.reweight:
        if mll=='none': continue
        files=glob.glob(indirs.format(MLL='-%s'%mll, TAG=tag))
        print 'Found %d files'%len(files)
        if len(files)==0: raise RuntimeError("No files found")
        l = getLimitHists(files, mll)
        limCurves.append( l )
        plotLimits([l], [lim_labels[mll=='neg']], "%s_%s_only"%(label,mll), outdir)

    if 'pos' in args.reweight and 'neg' in args.reweight:
        plotLimits(limCurves, lim_labels, label+"_both", outdir)


outdir=args.outdir.rstrip("/")
print "Scans will be saved in the folder '%s'..."%outdir

rwt_comp = False
for sel in args.indir:
    sel = sel.rstrip("/")
    name = sel.split("/")[-1]
    for tag in args.tag:
        print "For tag "+tag+":"
        for mll in args.reweight:
            run("%s_merged/cards/%s%s_*"%(sel,args.signalModel,'-%s'%mll if mll!='none' else ''),tag,"%s_%s%s"%(name,tag,'_%s'%mll if mll!='none' else ''),outdir)

        if rwt_comp:
            card_prototype=sel+"_merged/cards/"+args.model+"{MLL}_*/log%s_*_{TAG}.txt"%("" if args.unblind else "_b")
            runMLL(card_prototype,tag,'mll_'+tag,outdir)
