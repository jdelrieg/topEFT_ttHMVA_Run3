import os
import re
import glob
import ROOT
from ROOT import *
import array
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--indir", default=[], action="append", required=True, help="Choose the input directories")
parser.add_argument("--outDir", default="susy-sos/scanPlots/", help="Choose the output directory. Default='%(default)s'")
parser.add_argument("--tag", default=[], action="append", help="Choose the tags to plot. Default=['all','2lep','3lep']")
parser.add_argument("--savefmts", default=[], action="append", help="Choose save formats for plots. Default=['.pdf','.png','.jpg','.root','.C']")
args = parser.parse_args()

if len(args.indir) == 0: raise RuntimeError("No input directories given!")
if len(args.tag) == 0: args.tag = ['all','2lep','3lep']
if len(args.savefmts) == 0: args.savefmts = ['.pdf','.png','.jpg','.root','.C']


moreText = "pp #rightarrow #tilde{#chi}_{1}^{#pm}#tilde{#chi}_{2}^{0} #rightarrow WZ#tilde{#chi}^{0}_{1}#tilde{#chi}^{0}_{1}, NLO-NLL excl."
moreText2 = "median expected upper limit on cross section at 95% CL"

lumiText              = "137 fb^{-1} (13 TeV)"
cmsText               = "#bf{CMS} Preliminary"
cmsTextFont           = 52  
writeExtraText        = True
extraText             = "Internal"
extraTextFont         = 52 
lumiTextSize          = 0.45
lumiTextOffset        = 0.2
cmsTextSize           = 0.55
cmsTextOffset         = 0.1
relPosX               = 0.045
relPosY               = 0.035
relExtraDY            = 1.2
extraOverCmsTextSize  = 0.56 #0.76


class Limit:
    def __init__(self,mass, Dm, med, p1s, m1s):
        self.mass=mass
        self.Dm=Dm
        self.med=med
        self.p1s=p1s
        self.m1s=m1s
        
        
def getLimit(files, label, outdir):
    limits=[]
    for f in files:
        mass=os.path.basename(f).split('_')[3:5]
        massH=float(mass[0])
        massL=float(mass[0])-float(mass[1])
        with open(f) as fin:
            med=0
            p1s=0
            m1s=0
            for line in fin:
                if "Expected 50.0" in line:
                    med = float(line.split()[-1])
                if "Expected 84.0" in line:
                    p1s = float(line.split()[-1])
                if "Expected 16.0" in line:
                    m1s = float(line.split()[-1])
            lim=Limit(massH, massL, med, p1s, m1s)
            limits.append(lim)    
    vm=map(lambda lim : lim.mass, limits)
    vDm=map(lambda lim : lim.Dm, limits)
    vMed=map(lambda lim : lim.med, limits)
    
    
    thisLim=map(lambda im, idm, ilim: (im,idm,ilim), vm,vDm,vMed)
    
    vDmBins=vDm
    vDmBins.sort()
    vDmBins=list(sorted(set(vDmBins))[:11])
    vDmBins.append(85)
    h2lim = TH2D("lim","",11, 87.5,362.5,11,array.array('d', vDmBins))#70,1,71)
    
    for lim in thisLim:
#        print lim[0],lim[1],lim[2]
        h2lim.Fill(lim[0],lim[1],lim[2])

#    h2lim.Print("all")
#    h2lim.Smooth(1,"k3a")
#    h2lim.Smooth(1,"kba")
#    h2lim.Smooth(1,"kba")
    h2limRet=h2lim.Clone("h2lim_ret")

    c1=TCanvas()
    c1.SetLeftMargin(0.12)
    c1.SetRightMargin(0.12)
    c1.SetBottomMargin(0.13)

    h2lim.SetStats(0)
    h2lim.GetXaxis().SetTitle("m_{#tilde{#chi}_{1}^{#pm}}=m_{#tilde{#chi}_{2}^{0}} [GeV]")
    h2lim.GetYaxis().SetTitle("#Delta m(#tilde{#chi}_{1}^{#pm}, #tilde{#chi}_{1}^{0}) [GeV]")
    h2lim.GetXaxis().SetLabelFont(42)   
    h2lim.GetXaxis().SetTitleFont(42)   
    h2lim.GetXaxis().SetLabelSize(0.042)
    h2lim.GetXaxis().SetTitleSize(0.052)

    h2lim.GetXaxis().SetRangeUser(100,270)
    h2lim.GetZaxis().SetRangeUser(3e-2,70)

    h2lim.GetYaxis().SetTitleOffset(1.10)   
    h2lim.GetYaxis().SetLabelFont(42)   
    h2lim.GetYaxis().SetTitleFont(42)   
    h2lim.GetYaxis().SetLabelSize(0.042)
    h2lim.GetYaxis().SetTitleSize(0.052)

    h2lim.DrawCopy("colz")
    h2lim.SetContour(1,array.array('d',[1]))
    h2lim.Draw("CONT3 same")
    h2lim.SetLineColor(ROOT.kRed)
    c1.SetLogz()
    t = c1.GetTopMargin()
    r = c1.GetRightMargin()
    l = c1.GetLeftMargin()
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(ROOT.kBlack)    
    extraTextSize = extraOverCmsTextSize*cmsTextSize
    latex.SetTextFont(42)
    latex.SetTextAlign(31) 
    latex.SetTextSize(lumiTextSize*t)    
    latex.DrawLatex(1-r,1-t+lumiTextOffset*t,lumiText)
    latex.SetTextFont(cmsTextFont)
    latex.SetTextAlign(11) 
    latex.SetTextFont(cmsTextFont)
    latex.SetTextAlign(11) 
    latex.SetTextSize(cmsTextSize*t)    
    latex.DrawLatex(l,1-t+lumiTextOffset*t,cmsText)
    x1=87.5
    y1=65.
    x2=287.5
    y2=85.


    b = TBox(x1,y1,x2,y2)
    b.SetFillColor(ROOT.kWhite)
    b.SetLineColor(ROOT.kBlack)
    b.SetLineWidth(2)
    b.Draw("l")
    c1.Update()
    mT=ROOT.TLatex(x1+4.5,y1+0.78*(y2-y1), moreText2)
    mT.SetTextFont(42)
    mT.SetTextSize(0.040)
    mT.Draw()
    mT2=ROOT.TLatex(x1+4.5,y1+0.45*(y2-y1), moreText)
    mT2.SetTextFont(42)
    mT2.SetTextSize(0.040)
    mT2.Draw()

    gl1=TGraph(2)
    gl1.SetPoint(0, x1+4.5, y1+0.17*(y2-y1))
    gl1.SetPoint(1, x1+12.5, y1+0.17*(y2-y1))
    gl1.SetLineColor(ROOT.kRed)
#    gl1.SetLineStyle(7)
    gl1.SetLineWidth(2)
    gl1.Draw("lsame")
    mT3=ROOT.TLatex(x1+16.5,y1+0.13*(y2-y1), "expected exclusion contour")
    mT3.SetTextFont(42)
    mT3.SetTextSize(0.040)
    mT3.Draw()


    os.system("mkdir -p %s"%outdir)
    for fmt in args.savefmts:
        c1.SaveAs("%s/h2lim_%s%s"%(outdir,label,fmt))
    return h2limRet


def run(indirs,tag,label,outdir):
    limCurves=[]
    dirs=glob.glob(indirs)
    files = ['%s/log_b_%s_%s.txt'%(d,os.path.basename(d),tag) for d in dirs]
    files = filter(lambda f: os.path.exists(f),files)
    print 'Found %d files'%len(files)
    h2All = getLimit(files, label, outdir)


outdir=args.outDir.rstrip("/")
print "Scans will be saved in the folder '%s'..."%outdir
for sel in args.indir:
    sel = sel.rstrip("/")
    name = sel.split("/")[-1]
    for tag in args.tag:
        print "For tag "+tag+":"
        run("%s_merged/cards/TChiWZ_*"%sel,tag,"%s_%s"%(name,tag),outdir)


#files=glob.glob(indir+'*limit_2lep.txt')
#print "FILES 2L"
#print files
#h22l = getLimit(files, label+"_2lep", outdir)


#h22l = h2All#h22l.Divide(h2All)
#c1=TCanvas()
#ROOT.gStyle.SetPaintTextFormat("4.3f")
#
#
#c1=TCanvas()
#c1.SetLeftMargin(0.12)
#c1.SetRightMargin(0.12)
#c1.SetBottomMargin(0.13)
#
#h22l.SetStats(0)
#h22l.GetXaxis().SetTitle("m_{#tilde{#chi}_{1}^{#pm}}=m_{#tilde{#chi}_{2}^{0}} [GeV]")
#h22l.GetYaxis().SetTitle("#Delta m(#tilde{#chi}_{1}^{#pm}, #tilde{#chi}_{1}^{0}) [GeV]")
#h22l.GetXaxis().SetLabelFont(42)   
#h22l.GetXaxis().SetTitleFont(42)   
#h22l.GetXaxis().SetLabelSize(0.042)
#h22l.GetXaxis().SetTitleSize(0.052)
#
#h22l.GetXaxis().SetRangeUser(100,270)
#h22l.GetZaxis().SetRangeUser(1.,4.)
#
#h22l.GetYaxis().SetTitleOffset(1.10)   
#h22l.GetYaxis().SetLabelFont(42)   
#h22l.GetYaxis().SetTitleFont(42)   
#h22l.GetYaxis().SetLabelSize(0.042)
#h22l.GetYaxis().SetTitleSize(0.052)
#
#h22l.Draw("colz text")
#
#t = c1.GetTopMargin()
#r = c1.GetRightMargin()
#l = c1.GetLeftMargin()
#latex = ROOT.TLatex()
#latex.SetNDC()
#latex.SetTextAngle(0)
#latex.SetTextColor(ROOT.kBlack)    
#extraTextSize = extraOverCmsTextSize*cmsTextSize
#latex.SetTextFont(42)
#latex.SetTextAlign(31) 
#latex.SetTextSize(lumiTextSize*t)    
#latex.DrawLatex(1-r,1-t+lumiTextOffset*t,lumiText)
#latex.SetTextFont(cmsTextFont)
#latex.SetTextAlign(11) 
#latex.SetTextFont(cmsTextFont)
#latex.SetTextAlign(11) 
#latex.SetTextSize(cmsTextSize*t)    
#latex.DrawLatex(l,1-t+lumiTextOffset*t,cmsText)
#x1=87.5
#y1=70.
#x2=287.5
#y2=85.
#
#
#b = TBox(x1,y1,x2,y2)
#b.SetFillColor(ROOT.kWhite)
#b.SetLineColor(ROOT.kBlack)
#b.SetLineWidth(2)
#b.Draw("l")
#c1.Update()
#mT=ROOT.TLatex(x1+3.5,y1+0.67*(y2-y1), moreText)
#mT.SetTextFont(42)
#mT.SetTextSize(0.040)
#mT.Draw()
#mT2=ROOT.TLatex(x1+3.5,y1+0.22*(y2-y1), "median exp. lim. at 95% CL, ratio of (2 lep.) to (2+3 lep.) cats.")
#mT2.SetTextFont(42)
#mT2.SetTextSize(0.040)
#mT2.Draw()
#
#for fmt in args.savefmts:
#    c1.SaveAs("%s/h2lim_ratio2lto2lp3l%s"%(outdir,fmt))
