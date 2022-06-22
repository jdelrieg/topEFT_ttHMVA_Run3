import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("outDir", help="Choose the output directory.\nOutput will be saved to 'outDir/year/LEP_REG_BIN'")
parser.add_argument("year", help="Choose the year: '2016', '2017' or '2018'")
parser.add_argument("--lep", default=None, required=True, help="Choose number of leptons to use (REQUIRED)")
parser.add_argument("--reg", default=None, required=True, help="Choose region to use (REQUIRED)")
parser.add_argument("--bin", default=None, required=True, help="Choose bin to use (REQUIRED)")
args = parser.parse_args()

fileName = args.outDir+"/"+args.year+"/"+args.lep+"_"+args.reg+"_"+args.bin+"_"+"mc_data/"+"yields.txt"
fakes = 0.0
bkg = 0.0
data = 0.0
with open(fileName) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       line = fp.readline()
       line_list = line.strip().split()
       if len(line_list) > 0:
           bkg_category = line_list[0]
           if 'fakes' in bkg_category: fakes = fakes + float(line_list[1])
           if 'BACKGROUND' in bkg_category: bkg = float(line_list[1])
           if 'DATA' in bkg_category: data = float(line_list[1])
       cnt += 1
if data==0 or fakes==0: SF = 0
else: SF = (data - (bkg - fakes)) / fakes
SF_string = "ScaleFactor1F" if "1F" in args.reg else "ScaleFactor2F" if "2F" in args.reg else "ScaleFactor3F"
SF_string = SF_string+"_"+str(args.year)[-2:]
subprocess.call(["echo", "%s: %f"%(SF_string,SF)])
