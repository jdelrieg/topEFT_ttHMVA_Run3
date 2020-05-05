import os
import re
import glob
import array
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--indir", default=[], action="append", required=True, help="Choose the input directories")
parser.add_argument("--outDir", default="susy-sos/scanPlots/", help="Choose the output directory. Default='%(default)s'")
parser.add_argument("--tag", default=[], action="append", help="Choose the tags to plot. Default=['all','2lep','3lep']")
parser.add_argument("--savefmts", default=[], action="append", help="Choose save formats for plots. Default=['.pdf','.png','.jpg','.root','.C']")
parser.add_argument("--mll", default=[], action="append", help="Choose the signal mll reweight scenarios to plot. Default=['none','pos','neg']")
args = parser.parse_args()

if len(args.indir) == 0: raise RuntimeError("No input directories given!")
if len(args.tag) == 0: args.tag = ['all','2lep','3lep']
if len(args.mll) == 0: args.mll = ['none','pos','neg']
if len(args.savefmts) == 0: args.savefmts = ['.pdf','.png','.jpg','.root','.C']

import ROOT
from ROOT import *

if len(args.indir) == 0: raise RuntimeError("No input directories given!")
if len(args.tag) == 0: args.tag = ['all','2lep','3lep']
if len(args.savefmts) == 0: args.savefmts = ['.pdf','.png','.jpg','.root','.C']

logy=False
#logy=True

# Legend info
moreText = "pp #rightarrow #tilde{#chi}_{1}^{#pm}#tilde{#chi}_{2}^{0} #rightarrow WZ#tilde{#chi}^{0}_{1}#tilde{#chi}^{0}_{1}, NLO-NLL excl."
moreText2 = "median expected upper limit on cross section at 95% CL"
cmsText               = "#bf{CMS} Preliminary"
cmsTextFont           = 52  
cmsTextSize           = 0.55
cmsTextOffset         = 0.1
lumiText              = "137 fb^{-1} (13 TeV)"
lumiTextFont          = 42
lumiTextSize          = 0.45
lumiTextOffset        = 0.2
leg_ylo=60.
leg_nlines=3

# Plot range
range_xlo=100.
range_xhi=300.
range_ylo=3.
range_yhi=75.

if logy:
    range_yhi=350.
    leg_ylo=100.

class Limit:
    def __init__(self,mass, Dm, vals):
        self.mass = mass
        self.Dm = Dm
        self.vals = vals

def getLimitHists(files, tag):
    limits=[]
    parser={
        'Expected 50.0' : 0,
        'Expected 84.0' : 1,
        'Expected 16.0' : -1,
    }
    for f in files:
        mass=os.path.basename(f).split('_')[3:5]
        massH=float(mass[0])
        massL=float(mass[0])-float(mass[1])
        with open(f) as fin:
            vals={}
            for line in fin:
                for text,var in parser.iteritems():
                    if text in line:
                        vals[var] = float(line.split()[-1])
            if len(vals)<len(parser): continue
            lim=Limit(massH, massL, vals)
            limits.append(lim)

    hs={}
    for var in parser.values():
        g = TGraph2D(len(limits))
        for i,lim in enumerate(limits):
            g.SetPoint(i,lim.mass,lim.Dm,lim.vals[var])
        g.SetNpx(200)
        g.SetNpy(200)
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

    h_bkgd.GetXaxis().SetTitle("m_{#tilde{#chi}_{1}^{#pm}}=m_{#tilde{#chi}_{2}^{0}} [GeV]")
    h_bkgd.GetXaxis().SetLabelFont(42)
    h_bkgd.GetXaxis().SetTitleFont(42)
    h_bkgd.GetXaxis().SetLabelSize(0.042)
    h_bkgd.GetXaxis().SetTitleSize(0.052)

    h_bkgd.GetYaxis().SetTitle("#Delta m(#tilde{#chi}_{1}^{#pm}, #tilde{#chi}_{1}^{0}) [GeV]")
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

        h2lim, h2limP1, h2limM1 = limit_hists[0], limit_hists[1], limit_hists[-1]
        h2lim.SetLineWidth(2)
        h2limP1.SetLineWidth(1)
        h2limM1.SetLineWidth(1)
        h2limP1.SetLineStyle(2)
        h2limM1.SetLineStyle(2)

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

    mT3=ROOT.TLatex(x1+16.5,ylines[2], "Expected #pm #sigma_{exp}")
    mT3.SetTextAlign(12)
    mT3.SetTextFont(42)
    mT3.SetTextSize(0.040)
    mT3.Draw()

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
    limCurves=[]
    dirs=glob.glob(indirs)
    files = ['%s/log_b_%s_%s.txt'%(d,os.path.basename(d),tag) for d in dirs]
    files = filter(lambda f: os.path.exists(f),files)
    print 'Found %d files'%len(files)

    lims = getLimitHists(files,tag)
    plotLimits([lims], [], label, outdir)

def runMLL(indirs,tag,label,outdir):
    limCurves=[]
    lim_labels=['N1*N2>0','N1*N2<0']

    for mll in args.mll:
        if mll=='none': continue
        files=glob.glob(indirs.format(MLL='-%s'%mll, TAG=tag))
        print 'Found %d files'%len(files)
        l = getLimitHists(files, mll)
        limCurves.append( l )
        plotLimits([l], [lim_labels[mll=='neg']], "%s_%s_only"%(label,mll), outdir)

    if 'pos' in args.mll and 'neg' in args.mll:
        plotLimits(limCurves, lim_labels, label+"_both", outdir)


outdir=args.outDir.rstrip("/")
print "Scans will be saved in the folder '%s'..."%outdir
for sel in args.indir:
    sel = sel.rstrip("/")
    name = sel.split("/")[-1]
    for tag in args.tag:
        print "For tag "+tag+":"
        for mll in args.mll:
            run("%s_merged/cards/TChiWZ%s_*"%(sel,'-%s'%mll if mll!='none' else ''),tag,"%s_%s%s"%(name,tag,'_%s'%mll if mll!='none' else ''),outdir)

        card_prototype=sel+"_merged/cards/TChiWZ{MLL}_*/log_b_*_{TAG}.txt"
        runMLL(card_prototype,tag,'mll_'+tag,outdir)
