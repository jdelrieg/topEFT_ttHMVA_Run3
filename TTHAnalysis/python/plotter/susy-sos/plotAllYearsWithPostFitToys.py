import ROOT, argparse, math

parser = argparse.ArgumentParser()
parser.add_argument("--dir", default="", required=True, help="Directory with saved toys")
parser.add_argument("--asimov", default="fit_b", choices=["fit_b","fit_s","prefit"], help="Signal model to consider")
parser.add_argument("--reweight", default="none", help="Comma-separated list of scenarios to consider: none, pos, neg")
parser.add_argument("--signalModel", default="TChiWZ", choices=["TChiWZ","Higgsino","T2tt","T2bW","HiggsPMSSM"], help="Signal model to consider")
parser.add_argument("--masspoint", default="250_230", help="Signal masspoint to consider")
args = parser.parse_args()

categories=[
"2los_cr_ss_med",
"2los_cr_dy_low",
"2los_cr_dy_med",
"2los_cr_tt_low",
"2los_cr_tt_med",
"3l_cr_wz_low",
"3l_cr_wz_med"
]            
if args.signalModel!="T2tt" and args.signalModel!="T2bW":
   categories.append("2los_sr_low")
   categories.append("2los_sr_med")
   categories.append("2los_sr_high")
   categories.append("2los_sr_ultra")
   categories.append("3l_sr_low")
   categories.append("3l_sr_med")
else:
   categories.append("2los_sr_col_low")
   categories.append("2los_sr_col_med")
   categories.append("2los_sr_col_high")
   categories.append("2los_sr_col_ultra")
years = ["2016","2017","2018"]
procs = ["prompt_dy","prompt_tt","prompt_vv","prompt_wz","Rares","Convs","FRfakes_data","semidd_fakes","signal_"+args.signalModel+"_"+args.masspoint+("_"+args.reweight if args.reweight!="none" else "")]

catDirs = {}
toyHists = {}
Ntoys = 200
args.dir = args.dir.rstrip("/") + "/"
outFile = ROOT.TFile(args.dir+"plotAllYearsWithPostFitToys.root","recreate")
rootDir = outFile.mkdir("shapes_"+args.asimov)
for itoy in range(Ntoys):
    toyFile = ROOT.TFile(args.dir+"toys_"+args.asimov+str(itoy)+".root","read")
    outFile.cd()
    for category in categories:
        catDirName = "sos_"+category
        if not rootDir.FindKey(catDirName): catDir = rootDir.mkdir(catDirName)
        if catDirs.has_key(catDirName): pass
        else: catDirs[catDirName] = catDir
        histTotal = None
        for proc in procs:
            tempKeyName = catDirName+"_"+proc
            newHisto = True
            hist = None
            for year in years:
                tempHistName = "bin"+catDirName+"_"+year+"_proc_"+proc
                tempHist = None
                if toyFile.GetKey("n_exp_final_"+tempHistName): tempHist = toyFile.Get("n_exp_final_"+tempHistName)
                elif toyFile.GetKey("n_exp_"+tempHistName): tempHist = toyFile.Get("n_exp_"+tempHistName)
                else: continue
                if newHisto:
                    hist = tempHist.Clone(proc)
                    newHisto = False
                else: hist.Add(tempHist)
            if hist:
                if toyHists.has_key(tempKeyName): toyHists.get(tempKeyName).Add(hist)
                else: toyHists[tempKeyName] = hist.Clone("proc")
                if "signal" not in tempKeyName:
                    if toyHists.has_key(catDirName+"_total_background"): toyHists.get(catDirName+"_total_background").Add(hist)
                    else: toyHists[catDirName+"_total_background"] = hist.Clone("total_background")
                if toyHists.has_key(catDirName+"_total"): toyHists.get(catDirName+"_total").Add(hist)
                else: toyHists[catDirName+"_total"] = hist.Clone("total")
            if itoy == Ntoys-1:
                if toyHists.has_key(tempKeyName): finalHist = toyHists[tempKeyName].Clone()
                else: continue
                finalHist.Scale(1/float(Ntoys))
                for i in range(1,finalHist.GetNbinsX()+1): finalHist.SetBinError(i,finalHist.GetBinError(i)*math.sqrt(Ntoys))
                catDirs[catDirName].WriteObject(finalHist,proc)
        if itoy == Ntoys-1:
            finalHistTotalBackground = toyHists[catDirName+"_total_background"].Clone()
            finalHistTotalBackground.Scale(1/float(Ntoys))
            for i in range(1,finalHistTotalBackground.GetNbinsX()+1): finalHistTotalBackground.SetBinError(i,finalHistTotalBackground.GetBinError(i)*math.sqrt(Ntoys))
            catDirs[catDirName].WriteObject(finalHistTotalBackground,"total_background")

            finalHistTotal = toyHists[catDirName+"_total"].Clone()
            finalHistTotal.Scale(1/float(Ntoys))
            for i in range(1,finalHistTotal.GetNbinsX()+1): finalHistTotal.SetBinError(i,finalHistTotal.GetBinError(i)*math.sqrt(Ntoys))
            catDirs[catDirName].WriteObject(finalHistTotal,"total")
