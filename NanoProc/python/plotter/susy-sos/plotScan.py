import os
import re
import glob
import array
import argparse
import sys

import ROOT
from ROOT import *

parser = argparse.ArgumentParser()
parser.add_argument("--indir", default=[], action="append", required=True, help="Choose the input directories")
parser.add_argument("--outdir", default="susy-sos/scanPlots/", help="Choose the output directory. Default='%(default)s'")
parser.add_argument("--tag", default=[], action="append", help="Choose the tags to plot. Default=['all','2lep','3lep']")
parser.add_argument("--savefmts", default=[], action="append", help="Choose save formats for plots. Default=['.pdf','.png','.jpg','.root','.C']")
parser.add_argument("--reweight", default=[], action="append", help="Choose the signal mll reweight scenarios to plot. Default=['none']")
parser.add_argument("--signalModel", default="TChiWZ", choices=["TChiWZ","Higgsino","HiggsPMSSM","T2tt","T2bW"], help="Signal model to consider")
parser.add_argument("--unblind", action='store_true', default=False, help="Run unblinded scans")
parser.add_argument("--print", dest="prnt", action='store_true', default=False, help="Print results")
parser.add_argument("--logy", action='store_true', default=False, help="Plot logy limit plot")
parser.add_argument("--pretend", action='store_true', default=False, help="Get limits and run algorithms but don't plot (for debugging purposes)")
# Limit specific options
parser.add_argument("--xsec", action='store_true', default=False, help="Plot xsec instead of signal strength (which is the default)")
parser.add_argument("--sigma2", action='store_true', default=False, help="Also plot the 2 sigma line")
parser.add_argument("--smooth", nargs=2, default=[0,"k3a"], help="Apply smoothing X times with kernel Y (Y='k3a','k5a','k5b'). Multiple smoothings are not recommended. Not guaranteed to be compatible with a tag other than 'all'.")
# Nuisance parameter specific options
parser.add_argument("--NPscan", default=None, help="Run scan of specific nuisances parameter")
parser.add_argument("--NPerror", action='store_true', default=False, help="Plot NP error instead of central value")
parser.add_argument("--fit", default="fit_b", choices=["fit_b","fit_s"], help="Use b or (s+b) fit for ML diagnostics. Default(b-only fit)")
# Significance specific options
parser.add_argument("--significance", dest="signif", default=None, choices=["exp_aprio","exp_apost","obs"], help="Plot significance maps")


args = parser.parse_args()

if len(args.indir) == 0: raise RuntimeError("No input directories given!")
if len(args.tag) == 0: args.tag = ['all','2lep','3lep']
if len(args.reweight) == 0: args.reweight = ['none']
if len(args.savefmts) == 0: args.savefmts = ['.pdf','.png','.jpg','.root','.C']
if (args.signif == "exp_apost" or args.signif == "obs") and not args.unblind: raise RuntimeError("Asking for unblinded significance without using the 'unblind' flag is not allowed!")

if args.signif:
    ncontours = 999
    stops = [0.00, 0.34, 0.61, 0.84, 1.00]
    red   = [0.00, 0.00, 0.87, 1.00, 0.51]
    green = [0.00, 0.81, 1.00, 0.20, 0.00]
    blue  = [0.51, 1.00, 0.12, 0.00, 0.00]

    s = array.array('d', stops)
    r = array.array('d', red)
    g = array.array('d', green)
    b = array.array('d', blue)

    npoints = len(s)
    TColor.CreateGradientColorTable(npoints, s, r, g, b, ncontours)
    ROOT.gStyle.SetNumberContours(ncontours)

# Cross section definitions
TChiWZ_xsec = {
100 : 22.6701, 125 : 10.0348,  150 : 5.18086, 175 : 2.95328,  200 : 1.807,\
225 : 1.16509, 250 : 0.782487, 275 : 0.54303, 300 : 0.386936, 325 : 0.281911}
TChiWZ_xsec_unc = {
100 : 0.973967, 125 : 0.457604,  150 : 0.253223, 175 : 0.154386,  200 : 0.101316,\
225 : 0.0688042, 250 : 0.0487463, 275 : 0.0354083, 300 : 0.0263602, 325 : 0.0200201}
Higgsino_xsec = {
100 : 8.603,  120 : 4.524,  140 : 2.5324, 160 : 1.5393, 180 : 1.0014,\
200 : 0.6684, 220 : 0.4679, 240 : 0.3365, 250 : 0.2880}
Higgsino_xsec_unc = {
100 : 0.225952,  120 : 0.122902,  140 : 0.0732226, 160 : 0.0474496, 180 : 0.0326946,\
200 : 0.0232810, 220 : 0.0171179, 240 : 0.0129217, 250 : 0.0113304}
HiggsPMSSM_xsec = {
"100_1000" : 14.750, "100_1200" : 14.680, "100_300" : 16.300, "100_400" : 15.630, "100_500" : 15.304, "100_600" : 15.112, "100_800" : 14.881,\
"120_1000" : 7.634,  "120_1200" : 7.586,  "120_300" : 8.364,  "120_400" : 8.035,  "120_500" : 7.893,  "120_600" : 7.788,  "120_800" : 7.679,\
"140_1000" : 4.375,  "140_1200" : 4.359,  "140_300" : 4.784,  "140_400" : 4.612,  "140_500" : 4.525,  "140_600" : 4.463,  "140_800" : 4.405,\
"160_1000" : 2.706,  "160_1200" : 2.698,  "160_300" : 2.967,  "160_400" : 2.848,  "160_500" : 2.791,  "160_600" : 2.765,  "160_800" : 2.717,\
"180_1000" : 1.771,  "180_1200" : 1.761,  "180_300" : 1.937,  "180_400" : 1.857,  "180_500" : 1.820,  "180_600" : 1.796,  "180_800" : 1.777,\
"200_1000" : 1.205,  "200_1200" : 1.203,  "200_300" : 1.324,  "200_400" : 1.262,  "200_500" : 1.237,  "200_600" : 1.224,  "200_800" : 1.210,\
"220_1000" : 0.840,  "220_1200" : 0.836,  "220_300" : 0.936,  "220_400" : 0.888,  "220_500" : 0.866,  "220_600" : 0.862,  "220_800" : 0.847,\
"240_1000" : 0.612,  "240_1200" : 0.609,  "240_300" : 0.683,  "240_400" : 0.643,  "240_500" : 0.627,  "240_600" : 0.622,  "240_800" : 0.613}
HiggsPMSSM_xsec_unc = HiggsPMSSM_xsec.copy()
for key in list(HiggsPMSSM_xsec_unc.keys()): HiggsPMSSM_xsec_unc[key] = HiggsPMSSM_xsec_unc[key]*0.06 # Assign 6% as in previous analysis
T2XX_xsec = {
250  : 21.5949,    275  : 13.3231,    300  : 8.51615,   325 : 5.60471,   350 : 3.78661,    375 : 2.61162,    400  : 1.83537,    425  : 1.31169,\
450  : 0.948333,   475  : 0.697075,   500  : 0.51848,   525 : 0.390303,  550 : 0.296128,   575 : 0.226118,   600  : 0.174599,   625  : 0.136372,\
650  : 0.107045,   675  : 0.0844877,  700  : 0.0670476, 725 : 0.0536438, 750 : 0.0431418,  775 : 0.0348796,  800  : 0.0283338,  825  : 0.0230866,\
850  : 0.0189612,  875  : 0.015625,   900  : 0.0128895, 925 : 0.0106631, 950 : 0.00883465, 975 : 0.00735655, 1000 : 0.00615134, 1025 : 0.00514619,\
1050 : 0.00432261, 1075 : 0.00364174, 1100 : 0.00307413}
T2XX_xsec_unc = {
250  : 3.03613,     275  : 1.89919,     300  : 1.18564,    325 : 0.774257,   350 : 0.518300,   375 : 0.361649,   400  : 0.251418,   425  : 0.177095,\
450  : 0.127607,    475  : 0.0933565,   500  : 0.0693711,  525 : 0.0520832,  550 : 0.0392923,  575 : 0.0300151,  600  : 0.0230600,  625  : 0.0174504,\
650  : 0.0138336,   675  : 0.0110428,   700  : 0.00894609, 725 : 0.00728504, 750 : 0.00593006, 775 : 0.00486909, 800  : 0.00401518, 825  : 0.00333435,\
850  : 0.00278768,  875  : 0.00233698,  900  : 0.00195954, 925 : 0.00165071, 950 : 0.00138860, 975 : 0.00118108, 1000 : 0.00100238, 1025 : 0.000853043,\
1050 : 0.000725589, 1075 : 0.000621405, 1100 : 0.000532983}
xsec = TChiWZ_xsec if args.signalModel=="TChiWZ" else Higgsino_xsec if args.signalModel=="Higgsino" else HiggsPMSSM_xsec if args.signalModel=="HiggsPMSSM" else T2XX_xsec
xsec_unc = TChiWZ_xsec_unc if args.signalModel=="TChiWZ" else Higgsino_xsec_unc if args.signalModel=="Higgsino" else HiggsPMSSM_xsec_unc if args.signalModel=="HiggsPMSSM" else T2XX_xsec_unc

# Legend info
reweightText = ""
# The following labelling won't work properly for commands with multiple reweightings
if "pos" in args.reweight: reweightText = "#tilde{m}_{#lower[-0.25]{#tilde{#chi}_{2}^{0}}} #times #tilde{m}_{#lower[-0.15]{#tilde{#chi}_{1}^{0}}} > 0, "
elif "neg" in args.reweight: reweightText = "#tilde{m}_{#lower[-0.25]{#tilde{#chi}_{2}^{0}}} #times #tilde{m}_{#lower[-0.15]{#tilde{#chi}_{1}^{0}}} < 0, "

moreText = ""
if args.signalModel == "TChiWZ": moreText = "pp #rightarrow #tilde{#chi}_{1}^{#pm}#tilde{#chi}_{2}^{0} #rightarrow WZ#tilde{#chi}^{0}_{1}#tilde{#chi}^{0}_{1} (Wino/Bino)"
elif args.signalModel == "T2tt": moreText = "pp #rightarrow #tilde{t}#tilde{t}, #tilde{t} #rightarrow bf#bar{f}#tilde{#chi}^{0}_{1} (T2bff)"
elif args.signalModel == "T2bW": moreText = "pp #rightarrow #tilde{t}#tilde{t}, #tilde{t} #rightarrow b#tilde{#chi}^{#pm}_{1}#rightarrow bW#tilde{#chi}^{0}_{1}, m_{#lower[-0.20]{#tilde{#chi}_{1}^{#pm}}}=(m_{#lower[-0.25]{#tilde{t}}}+m_{#lower[-0.15]{#tilde{#chi}_{1}^{0}}})/2 (T2bW)"
elif args.signalModel == "Higgsino": moreText = "pp #rightarrow #tilde{#chi}_{1}^{#pm}#tilde{#chi}_{2}^{0}, #tilde{#chi}_{2}^{0}#tilde{#chi}_{2}^{0}, m_{#lower[-0.20]{#tilde{#chi}_{1}^{#pm}}}=(m_{#lower[-0.25]{#tilde{#chi}_{2}^{0}}}+m_{#lower[-0.15]{#tilde{#chi}_{1}^{0}}})/2 (Higgsino simplified)"
elif args.signalModel == "HiggsPMSSM": moreText = "Higgsino pMSSM"
moreText2 = reweightText+"NLO-NLL exclusion"
if args.NPscan: moreText2 = "Normalized "+("uncertainty constraint" if args.NPerror else "central value shift")+" of parameter '"+str(args.NPscan)+"'"
if args.signif: moreText2 = ("Observed" if args.signif=="obs" else "Expected a-posteriori" if args.signif=="exp_apost" else "Expected a-priori")+" significance"
cmsText               = "#bf{CMS}" #it{Preliminary}"
cmsTextFont           = 42  
cmsTextSize           = 0.55
if args.logy: cmsTextOffset = 0.2 
else:    cmsTextOffset = 0.1
lumiText              = "129#minus137 fb^{-1} (13 TeV)"
lumiTextFont          = 42
lumiTextSize          = 0.45
if args.logy: lumiTextOffset     = 0.3 
else: lumiTextOffset        = 0.2
leg_ylo=78.5 if args.signalModel in ["T2tt","T2bW"] else 40. if args.signalModel=="Higgsino" else 1200. if args.signalModel=="HiggsPMSSM" else 50.
leg_nlines=2 if args.NPscan or args.signif else 3

# Plot range
range_xlo=297. if args.signalModel in ["T2tt","T2bW"] else 100.
range_xhi=650. if args.signalModel in ["T2tt","T2bW"] else 250. if args.signalModel=="Higgsino" else 240. if args.signalModel=="HiggsPMSSM" else 300.
range_ylo=10. if args.signalModel in ["T2tt","T2bW"] else 3. if args.signalModel=="Higgsino" else 300. if args.signalModel=="HiggsPMSSM" else 3.5
if args.logy: range_yhi=155. if args.signalModel in ["T2tt","T2bW"] else 79.5 if args.signalModel=="Higgsino" else 2000. if args.signalModel=="HiggsPMSSM" else 90
else: range_yhi=95. if args.signalModel in ["T2tt","T2bW"] else 50. if args.signalModel=="Higgsino" else 1500. if args.signalModel=="HiggsPMSSM" else 63 


def mass_from_str(s):
    return float(s.replace('p','.'))

class Limit:
    def __init__(self,fname):
        self.obs = None
        self.exp = {}
        if not os.path.exists(fname): 
            self.exp.update({'0' : None})
            return
        f = ROOT.TFile.Open(fname)
        if f:
            tree = f.Get('limit')
            if not tree:
                self.exp.update({'0' : None})
                return
            translate = {0.02500000037252903: '-2', 0.1599999964237213: '-1', 0.50: '0', 0.8399999737739563: '1', 0.9750000238418579: '2'}
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
            for i in range(pars_f.getSize()):
                x = pars_f[i]
                if x.GetName()!='r':
                    self.nuisances[x.GetName()] = (x.getVal(),x.getError())
                else:
                    raise RuntimeError("Not implemented in this context, use the default behavior to get the signal strength scan!")

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
        self.m1, self.m2 = [mass_from_str(x) for x in self.modname.split('_')[-2:]]
        self.indir = indir
        self.tag = tag
        self.unblind = unblind
        self.parse()

    def parse(self):
        self.limit = Limit(self.indir+'/higgsCombine_%s_%s_blind.AsymptoticLimits.mH%d.root'%(self.modname,self.tag,int(self.m1)))
        if args.signif: self.signif = Significance(self.indir+'/higgsCombine_%s_%s_%s.Significance.mH%d.root'%(self.modname,self.tag,args.signif,int(self.m1))).val
        if args.NPscan: self.mlfit = MLFit(self.indir+'/fitDiagnostics_%s_%s_aprio_bonly.root'%(self.modname,self.tag),args.fit)
        if self.unblind:
            self.limit = Limit(self.indir+'/higgsCombine_%s_%s_obs.AsymptoticLimits.mH%d.root'%(self.modname,self.tag,int(self.m1)))
            if args.NPscan: self.mlfit = MLFit(self.indir+'/fitDiagnostics_%s_%s_obs.root'%(self.modname,self.tag),args.fit)

class LimitPoint:
    def __init__(self,mass, Dm, vals):
        self.mass = mass
        self.Dm = Dm
        self.vals = vals

class GraphSmoothing:
    def __init__(self,initialGraph,kernel):
        self.k5a = ( ( 0, 0, 1, 0, 0 ),
                     ( 0, 2, 2, 2, 0 ),
                     ( 1, 2, 5, 2, 1 ),
                     ( 0, 2, 2, 2, 0 ),
                     ( 0, 0, 1, 0, 0 ) );
        self.k5b = ( ( 0, 1, 2, 1, 0 ),
                     ( 1, 2, 4, 2, 1 ),
                     ( 2, 4, 8, 4, 2 ),
                     ( 1, 2, 4, 2, 1 ),
                     ( 0, 1, 2, 1, 0 ) );
        self.k3a = ( ( 0, 1, 0 ),
                     ( 1, 2, 1 ),
                     ( 0, 1, 0 ) );
        self.ksize_x = 3 if kernel=="k3a" else 5
        self.ksize_y = 3 if kernel=="k3a" else 5
        self.kernel = self.k3a if kernel=="k3a" else self.k5a if kernel=="k5a" else self.k5b if kernel=="k5b" else None
        if self.kernel==None: raise RuntimeError("Unavailable kernel")

        self.graph = initialGraph
        self.buf = [0.0] * self.graph.GetN()
    
    def smoothedGraph(self,debug=False): # debug=True triggers a lot of printouts
        for i in range(self.graph.GetN()):
            self.buf[i] = self.graph.GetZ()[i]
            if debug: print(self.graph.GetZ()[i],"\t", end=' ')
        if debug: print()

        smoothGraph = TGraph2D(self.graph.GetN())

        x_push = (self.ksize_x-1)/2;
        y_push = (self.ksize_y-1)/2;
        npx = 9 if args.signalModel=="TChiWZ" else 9 if args.signalModel=="Higgsino" else 8 if args.signalModel=="HiggsPMSSM" else 15
        npy = 9 if args.signalModel=="TChiWZ" else 8 if args.signalModel=="Higgsino" else 7 if args.signalModel=="HiggsPMSSM" else 11
  
        for j in range(npy):
            for i in range(npx):
                content = 0.0
                norm = 0.0
                iGraph = j*npx+i
                if debug: print("\nGraph Bin =", iGraph)

                for m in range(self.ksize_y):
                    for n in range(self.ksize_x):
                        xb = i+(n-x_push)
                        yb = j+(m-y_push)
                        if debug: print("xb =", xb); print("yb =", yb)
                        if (xb >= 0) and (xb < npx) and (yb >= 0) and (yb < npy):
                            iBin = yb*npx + xb
                            if debug: print("Buffer Bin =", iBin)
                            k = self.kernel[n][m]
                            if k!=0.0:
                                norm = norm + k
                                content = content + k*self.buf[iBin]
                                if debug: print("Adding value", self.buf[iBin], " with weight", k, ". Resulting Sweights =", norm, " and Svalues =", content)
                if norm!=0.0:
                    if debug: print("Previous value =", self.graph.GetZ()[iGraph], " Updated value =", content/norm)
                    smoothGraph.SetPoint(iBin,self.graph.GetX()[iGraph],self.graph.GetY()[iGraph],content/norm)

        self.graph = smoothGraph
        return smoothGraph

def DeltaMsorting(lim):
    return lim.mass+lim.Dm*1000 # Dummy function to order limit points first by DeltaM and then by M_NLSP

def getLimitHists(files, tag):
    limits=[]
    for f in files:
        mass = '%d_%d'%(f.m1,f.m2)
        massH = f.m1
        massL = f.m2 if args.signalModel=="HiggsPMSSM" else f.m1-f.m2
        key = str(int(massH))+"_"+str(int(massL)) if args.signalModel=="HiggsPMSSM" else int(massH)
        vals = {}
        if args.NPscan:
            if args.NPscan in f.mlfit.nuisances:
                vals.update({'0' : f.mlfit.nuisances[args.NPscan][1 if args.NPerror else 0]})
            else: vals.update({'0' : None})
        elif args.signif:
            vals.update({'0' : f.signif})
        else:
            if f.limit.exp:
                vals.update(f.limit.exp)
            if f.limit.obs:
                vals['obs'] = f.limit.obs
                vals['obs1'] = xsec[key] / (xsec[key] + xsec_unc[key]) * f.limit.obs
                vals['obs-1'] = xsec[key] / (xsec[key] - xsec_unc[key]) * f.limit.obs
            if vals['0']!=None:
                vals['xs'] = xsec[key] * vals['0']
        if args.prnt: print(massH, massL, vals['0'])
        lim = LimitPoint(massH, massL, vals)
        if vals['0']!=None: limits.append(lim)
    limits.sort(key=DeltaMsorting)
    hs={}
    vars_to_plot = ['0','1','-1','xs']
    if args.sigma2: vars_to_plot = ['0','1','-1','2','-2','xs']
    if args.unblind: vars_to_plot.append('obs'); vars_to_plot.append('obs1'); vars_to_plot.append('obs-1');

    if args.NPscan: vars_to_plot = ['0']
    if args.signif: vars_to_plot = ['0']

    for var in vars_to_plot:
        # Include i-->i+1 hack to fill the 625/18 masspoint of the T2bW scan... Needs to be revised if results change.
        g = TGraph2D(len(limits)+1) if args.signalModel=="T2bW" else TGraph2D(len(limits))
        for i,lim in enumerate(limits):
            if len(lim.vals)<len(vars_to_plot): continue
            if args.signalModel=="T2bW" and ((lim.Dm==18.0 and lim.mass>625.0) or lim.Dm>18.0): i=i+1
            g.SetPoint(i,lim.mass,lim.Dm,lim.vals[var])
            if args.signalModel=="T2bW" and lim.Dm==18.0 and lim.mass==600.0:
                g.SetPoint(i+1,625.0,18.0,(limits[i].vals[var]+limits[i+1].vals[var])/2.0) 
        smoothing = GraphSmoothing(g,args.smooth[1])
        for iSmooth in range(int(args.smooth[0])): g = smoothing.smoothedGraph(debug=False)
        # Hack to extend limit plots and make space for the legend
        g.SetPoint(len(limits)+1,range_xlo,range_yhi,1)
        g.SetPoint(len(limits)+1,range_xhi,range_yhi,1)
        g.SetNpx(300)
        g.SetNpy(300)
        h = g.GetHistogram().Clone()
        h.SetTitle('')
        hs[var]=h
    return hs


def plotLimits(limits_hists, limit_labels, label, outdir):

    h_bkgd = limits_hists[0]['xs' if args.xsec else '0'].Clone('h_bkgd') # 'xs' plots cross sections, '0' plots the signal strength
    nlim=len(limits_hists)

    c1=TCanvas()
    c1.SetLeftMargin(0.12)
    c1.SetRightMargin(0.15)
    c1.SetBottomMargin(0.13)

    h_bkgd.SetStats(0)

    h_bkgd.GetXaxis().SetRangeUser(range_xlo,range_xhi)
    h_bkgd.GetYaxis().SetRangeUser(range_ylo,range_yhi)   
    if args.NPscan: h_bkgd.GetZaxis().SetRangeUser(-1.0,1.0)
    elif args.signif: h_bkgd.GetZaxis().SetRangeUser(-3.0,3.0)
    else: h_bkgd.GetZaxis().SetRangeUser(3e-2,70)

    h_bkgd.GetXaxis().SetTitle("m_{#lower[-0.15]{#tilde{t}}} [GeV]" if args.signalModel in ["T2tt","T2bW"] else "m_{#lower[-0.15]{#tilde{#chi}_{2}^{0}}} [GeV]" if args.signalModel=="Higgsino" else "#mu [GeV]" if args.signalModel=="HiggsPMSSM" else "m_{#lower[-0.15]{#tilde{#chi}_{1}^{#pm}}}=m_{#lower[-0.15]{#tilde{#chi}_{2}^{0}}} [GeV]")
    h_bkgd.GetXaxis().SetLabelFont(42)
    h_bkgd.GetXaxis().SetTitleFont(42)
    h_bkgd.GetXaxis().SetLabelSize(0.042)
    h_bkgd.GetXaxis().SetTitleSize(0.042)

    h_bkgd.GetYaxis().SetTitle("#Delta m(#tilde{t}, #tilde{#chi}_{1}^{0}) [GeV]" if args.signalModel in ["T2tt","T2bW"] else "M_{1} = 0.5 M_{2} [GeV]" if args.signalModel=="HiggsPMSSM" else "#Delta m(#tilde{#chi}_{2}^{0}, #tilde{#chi}_{1}^{0}) [GeV]")
    h_bkgd.GetYaxis().SetTitleOffset(1.10)
    h_bkgd.GetYaxis().SetLabelFont(42)
    h_bkgd.GetYaxis().SetTitleFont(42)
    h_bkgd.GetYaxis().SetLabelSize(0.042)
    h_bkgd.GetYaxis().SetTitleSize(0.042)

    h_bkgd.Draw("colz" if nlim==1 else "axis")

    colz = [ROOT.kRed,ROOT.kBlue]

    h_bkgd.GetZaxis().SetTitle("95% CL upper limit on the cross section [pb]")
    h_bkgd.GetZaxis().SetTitleOffset(1.10)
    h_bkgd.GetZaxis().SetLabelFont(42)
    h_bkgd.GetZaxis().SetTitleFont(42)
    h_bkgd.GetZaxis().SetLabelSize(0.042)
    h_bkgd.GetZaxis().SetTitleSize(0.042)

    for iLim, limit_hists in enumerate(limits_hists):
        for var,lim in limit_hists.items():
            if var=='xs': continue
            if args.NPscan or args.signif: lim.SetContour(1,array.array('d',[-5]))
            else: lim.SetContour(1,array.array('d',[1]))
            lim.Draw("CONT3 same")
            lim.SetLineColor(colz[iLim])

        if args.NPscan or args.signif: h2lim = limit_hists['0']
        else:
            h2lim, h2limP1, h2limM1 = limit_hists['0'], limit_hists['1'], limit_hists['-1']
            if args.unblind:
                h2limObs, h2limObsP1, h2limObsM1 = limit_hists['obs'], limit_hists['obs1'], limit_hists['obs-1']
                h2limObs.SetLineWidth(2)
                h2limObs.SetLineColor(ROOT.kBlack)
                h2limObsP1.SetLineColor(ROOT.kBlack)
                h2limObsM1.SetLineColor(ROOT.kBlack)
            h2limP1.SetLineWidth(1)
            h2limM1.SetLineWidth(1)
            h2limP1.SetLineStyle(1)
            h2limM1.SetLineStyle(1)
            if args.sigma2:
                h2limP2, h2limM2 = limit_hists['2'], limit_hists['-2']
                h2limP2.SetLineWidth(1)
                h2limM2.SetLineWidth(1)
                h2limP2.SetLineStyle(2)
                h2limM2.SetLineStyle(2)
        h2lim.SetLineWidth(2)

    if not args.NPscan and not args.signif: c1.SetLogz()
    c1.SetLogy(args.logy)
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
    Dx = x2-x1
    y1 = leg_ylo
    y2 = range_yhi

    delta = (y2-y1)/leg_nlines
    ylines = [y1+(i+0.5)*delta for i in range(leg_nlines)]
    ylines.reverse()

    if args.logy: 
        if args.signalModel in ["T2tt", "T2bW", "HiggsPMSSM"]: b = TBox(x1,y1,x2,y2) 
        if args.signalModel in ["Higgsino", "TChiWZ"] : b = TBox(x1,y1-2,x2,y2+3)
    else: 
        if args.signalModel == "TChiWZ" and 'neg' in args.reweight: b = TBox(x1,y1,x2,y2+1)
        else: b = TBox(x1,y1,x2,y2+0.5)
    b.SetFillColor(ROOT.kWhite)
    b.SetLineColor(ROOT.kBlack)
    b.SetLineWidth(1)
    b.Draw("l")
    c1.Update()
    if args.logy: 
        if args.signalModel == "HiggsPMSSM": mT=ROOT.TLatex(x1+0.025*Dx,ylines[0]+2, moreText)
        elif args.signalModel in ["Higgsino", "TChiWZ"]: mT=ROOT.TLatex(x1+0.025*Dx,ylines[0]-1, moreText)
        else: mT=ROOT.TLatex(x1+0.025*Dx,ylines[0]-5, moreText)
    else: mT=ROOT.TLatex(x1+0.025*Dx,ylines[0], moreText)
    mT.SetTextFont(42)
    mT.SetTextAlign(12)
    mT.SetTextSize(0.040)
    mT.Draw()
    if args.logy: 
        if args.signalModel == "HiggsPMSSM": mT2=ROOT.TLatex(x1+0.025*Dx,ylines[1]-2.1, moreText2)
        elif args.signalModel in ["Higgsino", "TChiWZ"]: mT2=ROOT.TLatex(x1+0.025*Dx,ylines[1]-4, moreText2)
        else: mT2=ROOT.TLatex(x1+0.025*Dx,ylines[1]-3, moreText2)
    else: mT2=ROOT.TLatex(x1+0.025*Dx,ylines[1], moreText2)
    mT2.SetTextAlign(12)
    mT2.SetTextFont(42)
    mT2.SetTextSize(0.040)
    mT2.Draw()

    if not args.NPscan and not args.signif:
        spread = delta*0.2
        fudge = delta*0.1
        gl1=TGraph(2)
        if args.logy:
            if args.signalModel == "TChiWZ" :
                gl1.SetPoint(0, x1+0.025*Dx, ylines[2]+fudge-3.0)
                gl1.SetPoint(1, x1+0.070*Dx, ylines[2]+fudge-3.0)

            else:
                gl1.SetPoint(0, x1+0.025*Dx, ylines[2]+fudge-2.8)
                gl1.SetPoint(1, x1+0.070*Dx, ylines[2]+fudge-2.8)
        else:
            gl1.SetPoint(0, x1+0.025*Dx, ylines[2]+fudge)
            gl1.SetPoint(1, x1+0.070*Dx, ylines[2]+fudge) 
        gl1.SetLineColor(colz[0])
        gl1.SetLineStyle(1)
        gl1.SetLineWidth(2)
        gl1.Draw("lsame")

        gl1p=TGraph(2)
        if args.logy:
            if args.signalModel == "TChiWZ" :
                gl1p.SetPoint(0, x1+0.025*Dx, ylines[2]+spread+fudge-3.0)
                gl1p.SetPoint(1, x1+0.070*Dx, ylines[2]+spread+fudge-3.0)
            else:
                gl1p.SetPoint(0, x1+0.025*Dx, ylines[2]+spread+fudge-2.8)
                gl1p.SetPoint(1, x1+0.070*Dx, ylines[2]+spread+fudge-2.8)
        else:
            gl1p.SetPoint(0, x1+0.025*Dx, ylines[2]+spread+fudge)
            gl1p.SetPoint(1, x1+0.070*Dx, ylines[2]+spread+fudge)
        gl1p.SetLineColor(colz[0])
        gl1p.SetLineStyle(1)
        gl1p.SetLineWidth(1)
        gl1p.Draw("lsame")

        gl1m=TGraph(2)
        if args.logy:
            if args.signalModel == "TChiWZ" :
                gl1m.SetPoint(0, x1+0.025*Dx, ylines[2]-spread+fudge-3.0)
                gl1m.SetPoint(1, x1+0.070*Dx, ylines[2]-spread+fudge-3.0)
            else:
                gl1m.SetPoint(0, x1+0.025*Dx, ylines[2]-spread+fudge-2.8)
                gl1m.SetPoint(1, x1+0.070*Dx, ylines[2]-spread+fudge-2.8)                
        else:
            gl1m.SetPoint(0, x1+0.025*Dx, ylines[2]-spread+fudge)
            gl1m.SetPoint(1, x1+0.070*Dx, ylines[2]-spread+fudge)
        gl1m.SetLineColor(colz[0])
        gl1m.SetLineStyle(1)
        gl1m.SetLineWidth(1)
        gl1m.Draw("lsame")

        if args.sigma2:
            gl2p=TGraph(2)
            gl2p.SetPoint(0, x1+0.025*Dx, ylines[2]+2*spread+fudge)
            gl2p.SetPoint(1, x1+0.070*Dx, ylines[2]+2*spread+fudge)
            gl2p.SetLineColor(colz[0])
            gl2p.SetLineStyle(2)
            gl2p.SetLineWidth(1)
            gl2p.Draw("lsame")

            gl2m=TGraph(2)
            gl2m.SetPoint(0, x1+0.025*Dx, ylines[2]-2*spread+fudge)
            gl2m.SetPoint(1, x1+0.070*Dx, ylines[2]-2*spread+fudge)
            gl2m.SetLineColor(colz[0])
            gl2m.SetLineStyle(2)
            gl2m.SetLineWidth(1)
            gl2m.Draw("lsame")

        if args.unblind:
            gl1Obs=TGraph(2)
            if args.logy: 
                if args.signalModel == "TChiWZ" : 
                    gl1Obs.SetPoint(0, x1+0.5*(x2-x1)+0.025*Dx, ylines[2]+fudge-3.0)
                    gl1Obs.SetPoint(1, x1+0.5*(x2-x1)+0.070*Dx, ylines[2]+fudge-3.0)
                else:
                    gl1Obs.SetPoint(0, x1+0.5*(x2-x1)+0.025*Dx, ylines[2]+fudge-2.8)
                    gl1Obs.SetPoint(1, x1+0.5*(x2-x1)+0.070*Dx, ylines[2]+fudge-2.8)

            else: 
                gl1Obs.SetPoint(0, x1+0.5*(x2-x1)+0.025*Dx, ylines[2]+fudge)
                gl1Obs.SetPoint(1, x1+0.5*(x2-x1)+0.070*Dx, ylines[2]+fudge)
            gl1Obs.SetLineColor(ROOT.kBlack)
            gl1Obs.SetLineStyle(1)
            gl1Obs.SetLineWidth(2)
            gl1Obs.Draw("lsame")

            gl1Obsp=TGraph(2)
            if args.logy:
                if args.signalModel == "TChiWZ":
                    gl1Obsp.SetPoint(0, x1+0.5*(x2-x1)+0.025*Dx, ylines[2]+spread+fudge-3.0)
                    gl1Obsp.SetPoint(1, x1+0.5*(x2-x1)+0.070*Dx, ylines[2]+spread+fudge-3.0)
                else:
                    gl1Obsp.SetPoint(0, x1+0.5*(x2-x1)+0.025*Dx, ylines[2]+spread+fudge-2.8)
                    gl1Obsp.SetPoint(1, x1+0.5*(x2-x1)+0.070*Dx, ylines[2]+spread+fudge-2.8)
            else:
                gl1Obsp.SetPoint(0, x1+0.5*(x2-x1)+0.025*Dx, ylines[2]+spread+fudge)
                gl1Obsp.SetPoint(1, x1+0.5*(x2-x1)+0.070*Dx, ylines[2]+spread+fudge) 
            gl1Obsp.SetLineColor(ROOT.kBlack)
            gl1Obsp.SetLineStyle(1)
            gl1Obsp.SetLineWidth(1)
            gl1Obsp.Draw("lsame")

            gl1Obsm=TGraph(2)
            if args.logy:
                if args.signalModel == "TChiWZ":
                    gl1Obsm.SetPoint(0, x1+0.5*(x2-x1)+0.025*Dx, ylines[2]-spread+fudge-3.0)
                    gl1Obsm.SetPoint(1, x1+0.5*(x2-x1)+0.070*Dx, ylines[2]-spread+fudge-3.0)
                else:
                    gl1Obsm.SetPoint(0, x1+0.5*(x2-x1)+0.025*Dx, ylines[2]-spread+fudge-2.8)
                    gl1Obsm.SetPoint(1, x1+0.5*(x2-x1)+0.070*Dx, ylines[2]-spread+fudge-2.8)
            else:
                gl1Obsm.SetPoint(0, x1+0.5*(x2-x1)+0.025*Dx, ylines[2]-spread+fudge)
                gl1Obsm.SetPoint(1, x1+0.5*(x2-x1)+0.070*Dx, ylines[2]-spread+fudge)
            gl1Obsm.SetLineColor(ROOT.kBlack)
            gl1Obsm.SetLineStyle(1)
            gl1Obsm.SetLineWidth(1)
            gl1Obsm.Draw("lsame")

        if args.logy: 
            if args.signalModel == "TChiWZ": mT3=ROOT.TLatex(x1+0.095*Dx, ylines[2]-3.0, "Expected #pm 1 #sigma_{experiment}")
            else: mT3=ROOT.TLatex(x1+0.095*Dx, ylines[2]-2.8, "Expected #pm 1 #sigma_{experiment}")
        else:  mT3=ROOT.TLatex(x1+0.095*Dx, ylines[2], "Expected #pm 1 #sigma_{experiment}")
        mT3.SetTextAlign(12)
        mT3.SetTextFont(42)
        mT3.SetTextSize(0.040)
        mT3.Draw()

        if args.unblind:
            if args.logy:
                if args.signalModel == "TChiWZ": mT3a=ROOT.TLatex(x1+0.5*(x2-x1)+0.095*Dx, ylines[2]-3.0, "Observed #pm 1 #sigma_{theory}")
                else: mT3a=ROOT.TLatex(x1+0.5*(x2-x1)+0.095*Dx, ylines[2]-2.8, "Observed #pm 1 #sigma_{theory}")
            else: mT3a=ROOT.TLatex(x1+0.5*(x2-x1)+0.095*Dx, ylines[2], "Observed #pm 1 #sigma_{theory}")
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
        c1.SaveAs("%s/h2%s_%s%s"%(outdir,"NP_"+str(args.NPscan) if args.NPscan else "Significance_"+args.signif if args.signif else "lim",label+args.logy*('_log')+(("_smooth"+args.smooth[0]+args.smooth[1]) if int(args.smooth[0])>0 else ""),fmt))


def run(indirs,tag,label,outdir):
    dirs=glob.glob(indirs)
    points = {}
    for d in dirs:
        x = SignalPoint(d,tag,args.unblind)
        if x:
            # Parse only points that are needed
            if args.signalModel=="TChiWZ":
                if x.m1 < 100 or x.m1 > 300 or x.m1-x.m2 < 3.0 or x.m1-x.m2 > 50.0: continue
            elif args.signalModel=="Higgsino":
                if x.m1 < 100 or x.m1 > 250 or x.m1-x.m2 < 3.0 or x.m1-x.m2 > 40.0: continue
            elif args.signalModel=="HiggsPSSM":
                if x.m1 < 100 or x.m1 > 240 or x.m2 < 300.0 or x.m2 > 1200.0: continue
            elif args.signalModel=="T2tt" or args.signalModel=="T2bW":
                if x.m1 < 300 or x.m1 > 650 or x.m1-x.m2 < 10.0 or x.m1-x.m2 > 80.0: continue
            points[(x.m1,x.m2)] = x
    print('Found %d files'%len(points))
    if len(points)==0: raise RuntimeError("No points found")
    lims = getLimitHists(list(points.values()),tag)
    if not args.pretend: plotLimits([lims], [], label, outdir)

def runMLL(indirs,tag,label,outdir):
    limCurves=[]
    lim_labels=['N1*N2>0','N1*N2<0']

    for mll in args.reweight:
        if mll=='none': continue
        files=glob.glob(indirs.format(MLL='-%s'%mll, TAG=tag))
        print('Found %d files'%len(files))
        if len(files)==0: raise RuntimeError("No files found")
        l = getLimitHists(files, mll)
        limCurves.append( l )
        plotLimits([l], [lim_labels[mll=='neg']], "%s_%s_only"%(label,mll), outdir)

    if 'pos' in args.reweight and 'neg' in args.reweight:
        plotLimits(limCurves, lim_labels, label+"_both", outdir)


outdir=args.outdir.rstrip("/")
print("Scans will be saved in the folder '%s'..."%outdir)

rwt_comp = False
for sel in args.indir:
    sel = sel.rstrip("/")
    name = sel.split("/")[-1]
    for tag in args.tag:
        print("For tag "+tag+":")
        for mll in args.reweight:
            run("%s_merged/cards/%s%s_*"%(sel,args.signalModel,'-%s'%mll if mll!='none' else ''),tag,"%s_%s%s"%(name,tag,'_%s'%mll if mll!='none' else ''),outdir)

        if rwt_comp:
            card_prototype=sel+"_merged/cards/"+args.model+"{MLL}_*/log%s_*_{TAG}.txt"%("" if args.unblind else "_b")
            runMLL(card_prototype,tag,'mll_'+tag,outdir)
