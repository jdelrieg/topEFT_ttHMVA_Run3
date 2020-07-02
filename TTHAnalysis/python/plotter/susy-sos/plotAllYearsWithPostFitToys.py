import ROOT, argparse, math

parser = argparse.ArgumentParser()
parser.add_argument("--asimov", default="fit_s", choices=["fit_b","fit_s","prefit"], help="Signal model to consider")
parser.add_argument("--reweight", default="none", help="Comma-separated list of scenarios to consider: none, pos, neg")
parser.add_argument("--signalModel", default="TChiWZ", choices=["TChiWZ","Higgsino","T2tt"], help="Signal model to consider")
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
if args.signalModel!="T2tt":
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
procs = ["prompt_dy","prompt_tt","prompt_vv","prompt_wz","Rares","Convs","FRfakes_data","semidd_fakes","signal_"+args.signalModel+"_"+args.masspoint+"_"+args.reweight]

catDirs = {}
toyHists = {}
Ntoys = 200
outFile = ROOT.TFile("plotAllYearsWithPostFitToys.root","recreate")
rootDir = outFile.mkdir("shapes_"+args.asimov)
for itoy in range(Ntoys):
    toyFile = ROOT.TFile("toys_"+args.asimov+str(itoy)+".root","read")
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
                if toyHists.has_key(catDirName+"_total"): toyHists.get(catDirName+"_total").Add(hist)
                else: toyHists[catDirName+"_total"] = hist.Clone("total")
            if itoy == Ntoys-1:
                if toyHists.has_key(tempKeyName): finalHist = toyHists[tempKeyName].Clone()
                else: continue
                finalHist.Scale(1/float(Ntoys))
                for i in range(1,finalHist.GetNbinsX()+1): finalHist.SetBinError(i,finalHist.GetBinError(i)*math.sqrt(Ntoys))
                catDirs[catDirName].WriteObject(finalHist,proc)
        if itoy == Ntoys-1:
            finalHistTotal = toyHists[catDirName+"_total"].Clone()
            finalHistTotal.Scale(1/float(Ntoys))
            for i in range(1,finalHistTotal.GetNbinsX()+1): finalHistTotal.SetBinError(i,finalHistTotal.GetBinError(i)*math.sqrt(Ntoys))
            catDirs[catDirName].WriteObject(finalHistTotal,"total")
