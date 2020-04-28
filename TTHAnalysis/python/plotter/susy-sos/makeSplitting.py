import os, argparse, itertools

parser = argparse.ArgumentParser()
parser.add_argument("--duration", type=int, default=8, help="job duration in hours")
parser.add_argument("what", help="what to do'")
parser.add_argument("outDir", help="output directory'")
parser.add_argument("--addopts", default=None, help="additional options to sos_plots.py")
parser.add_argument("--onlyFit", action='store_true', default=False, help="only rerun fits")
parser.add_argument("--accountingGroup", default=None, help="accounting group for condor jobs")
parser.add_argument("--reuseBackground", default=None, help="outDir from previous run for re-using backgrounds")
parser.add_argument("--reweight", default="none,pos,neg", help="Comma-separated list of scenarios to consider: none, pos, neg")
args = parser.parse_args()

years=["2016","2017","2018"]
_signals=[
"signal_TChiWZ_100_1","signal_TChiWZ_100_20","signal_TChiWZ_100_30","signal_TChiWZ_100_40","signal_TChiWZ_100_50","signal_TChiWZ_100_60","signal_TChiWZ_100_70","signal_TChiWZ_100_80","signal_TChiWZ_100_85","signal_TChiWZ_100_90","signal_TChiWZ_100_92","signal_TChiWZ_100_95","signal_TChiWZ_100_97","signal_TChiWZ_100_99",\
"signal_TChiWZ_125_105","signal_TChiWZ_125_110","signal_TChiWZ_125_115","signal_TChiWZ_125_117","signal_TChiWZ_125_120","signal_TChiWZ_125_122","signal_TChiWZ_125_124","signal_TChiWZ_125_35","signal_TChiWZ_125_45","signal_TChiWZ_125_5","signal_TChiWZ_125_55","signal_TChiWZ_125_65","signal_TChiWZ_125_75","signal_TChiWZ_125_85","signal_TChiWZ_125_95",\
"signal_TChiWZ_150_1","signal_TChiWZ_150_10","signal_TChiWZ_150_100","signal_TChiWZ_150_110","signal_TChiWZ_150_120","signal_TChiWZ_150_130","signal_TChiWZ_150_135","signal_TChiWZ_150_140","signal_TChiWZ_150_142","signal_TChiWZ_150_145","signal_TChiWZ_150_147","signal_TChiWZ_150_149","signal_TChiWZ_150_30","signal_TChiWZ_150_40","signal_TChiWZ_150_50","signal_TChiWZ_150_60","signal_TChiWZ_150_70","signal_TChiWZ_150_80","signal_TChiWZ_150_90",\
"signal_TChiWZ_175_1","signal_TChiWZ_175_105","signal_TChiWZ_175_115","signal_TChiWZ_175_125","signal_TChiWZ_175_135","signal_TChiWZ_175_145","signal_TChiWZ_175_155","signal_TChiWZ_175_160","signal_TChiWZ_175_165","signal_TChiWZ_175_167","signal_TChiWZ_175_170","signal_TChiWZ_175_172","signal_TChiWZ_175_174","signal_TChiWZ_175_45","signal_TChiWZ_175_65","signal_TChiWZ_175_95",\
"signal_TChiWZ_200_1","signal_TChiWZ_200_100","signal_TChiWZ_200_110","signal_TChiWZ_200_120","signal_TChiWZ_200_130","signal_TChiWZ_200_140","signal_TChiWZ_200_150","signal_TChiWZ_200_160","signal_TChiWZ_200_170","signal_TChiWZ_200_180","signal_TChiWZ_200_185","signal_TChiWZ_200_190","signal_TChiWZ_200_192","signal_TChiWZ_200_195","signal_TChiWZ_200_197","signal_TChiWZ_200_199","signal_TChiWZ_200_50","signal_TChiWZ_200_60","signal_TChiWZ_200_70","signal_TChiWZ_200_80","signal_TChiWZ_200_90",\
"signal_TChiWZ_225_1","signal_TChiWZ_225_105","signal_TChiWZ_225_115","signal_TChiWZ_225_125","signal_TChiWZ_225_135","signal_TChiWZ_225_145","signal_TChiWZ_225_155","signal_TChiWZ_225_165","signal_TChiWZ_225_175","signal_TChiWZ_225_185","signal_TChiWZ_225_195","signal_TChiWZ_225_205","signal_TChiWZ_225_210","signal_TChiWZ_225_215","signal_TChiWZ_225_217","signal_TChiWZ_225_220","signal_TChiWZ_225_222","signal_TChiWZ_225_224","signal_TChiWZ_225_25","signal_TChiWZ_225_75","signal_TChiWZ_225_95",\
"signal_TChiWZ_250_1","signal_TChiWZ_250_100","signal_TChiWZ_250_120","signal_TChiWZ_250_130","signal_TChiWZ_250_140","signal_TChiWZ_250_170","signal_TChiWZ_250_180","signal_TChiWZ_250_190","signal_TChiWZ_250_200","signal_TChiWZ_250_210","signal_TChiWZ_250_220","signal_TChiWZ_250_230","signal_TChiWZ_250_235","signal_TChiWZ_250_240","signal_TChiWZ_250_242","signal_TChiWZ_250_245","signal_TChiWZ_250_247","signal_TChiWZ_250_249","signal_TChiWZ_250_25","signal_TChiWZ_250_75",\
"signal_TChiWZ_275_1","signal_TChiWZ_275_125","signal_TChiWZ_275_135","signal_TChiWZ_275_145","signal_TChiWZ_275_155","signal_TChiWZ_275_165","signal_TChiWZ_275_175","signal_TChiWZ_275_195","signal_TChiWZ_275_205","signal_TChiWZ_275_215","signal_TChiWZ_275_225","signal_TChiWZ_275_235","signal_TChiWZ_275_245","signal_TChiWZ_275_25","signal_TChiWZ_275_255","signal_TChiWZ_275_260","signal_TChiWZ_275_265","signal_TChiWZ_275_267","signal_TChiWZ_275_270","signal_TChiWZ_275_272","signal_TChiWZ_275_274",\
"signal_TChiWZ_300_1","signal_TChiWZ_300_100","signal_TChiWZ_300_125","signal_TChiWZ_300_150","signal_TChiWZ_300_160","signal_TChiWZ_300_170","signal_TChiWZ_300_180","signal_TChiWZ_300_200","signal_TChiWZ_300_210","signal_TChiWZ_300_220","signal_TChiWZ_300_230","signal_TChiWZ_300_240","signal_TChiWZ_300_25","signal_TChiWZ_300_250","signal_TChiWZ_300_260","signal_TChiWZ_300_270","signal_TChiWZ_300_280","signal_TChiWZ_300_285","signal_TChiWZ_300_290","signal_TChiWZ_300_292","signal_TChiWZ_300_295","signal_TChiWZ_300_297","signal_TChiWZ_300_299","signal_TChiWZ_300_75",\
"signal_TChiWZ_325_1","signal_TChiWZ_325_100","signal_TChiWZ_325_125","signal_TChiWZ_325_150","signal_TChiWZ_325_175","signal_TChiWZ_325_185","signal_TChiWZ_325_195","signal_TChiWZ_325_205","signal_TChiWZ_325_215","signal_TChiWZ_325_225","signal_TChiWZ_325_235","signal_TChiWZ_325_245","signal_TChiWZ_325_25","signal_TChiWZ_325_255","signal_TChiWZ_325_265","signal_TChiWZ_325_275","signal_TChiWZ_325_285","signal_TChiWZ_325_295","signal_TChiWZ_325_50","signal_TChiWZ_325_75"
]
_signals=[x.lstrip('signal_') for x in _signals]
signals=[]
for mll in args.reweight.split(','):
   if mll=='none':
      signals += _signals
   else:
      signals += ['%s_%s'%(x,mll) for x in _signals]
categories=[
'2los/sr/low',
'2los/sr/med',
'2los/sr/high',
'2los/sr/ultra',
'3l/sr/low',
'3l/sr/med',
'2los/cr_ss/med',
'2los/cr_dy/low',
'2los/cr_dy/med',
'2los/cr_tt/low',
'2los/cr_tt/med',
'2los/cr_vv/low',
'2los/cr_vv/med',
'3l/cr_wz/low',
'3l/cr_wz/med',
]            

what=args.what
odir=args.outDir.rstrip("/")
duration=args.duration*3600
opts="--unc --fakes=semidd"
if args.addopts: opts+=' %s'%args.addopts

def prepSubmission(outdir,subdir,duration):
   odir = '%s/%s'%(outdir,subdir)
   os.system("rm -r %s"%odir)
   os.system("mkdir -p %s %s/logs"%(odir,odir))
   os.system("cp susy-sos/scripts/htcondor_runner.sh %s/"%odir)
   submitter = """executable      = {odir}/htcondor_runner.sh
arguments       = {path} $(Chunk)
output          = {odir}/logs/out.$(Cluster).$(Process)
error           = {odir}/logs/err.$(Cluster).$(Process)
log             = {odir}/logs/log.$(Cluster).$(Process)
+MaxRuntime = {duration}
{acctgroup}
getenv = True

request_cpus = 4
queue Chunk matching {odir}/job_*_bkg.sh

request_cpus = 1
queue Chunk matching {odir}/job_*_sig.sh
queue Chunk matching {odir}/job_*_fit.sh
""".format(odir=odir, path=os.environ['CMSSW_BASE'], duration=duration, acctgroup = '+AccountingGroup = "%s"'%args.accountingGroup if args.accountingGroup else '')
   with open('%s/htcondor_submitter.sub'%odir,'w') as outf:
      outf.write(submitter)

class bare_production:
   def __init__(self):

      class task:
         def __init__(self,pr,yr,cat):
            self.pr = pr
            self.yr = yr
            self.cat = cat

      tasks=[]
      prs = signals if args.reuseBackground else signals+['background']
      for pr in prs:
         for yr in years:
            for cat in categories:
               tasks.append(task(pr,yr,cat))

      def _printCmd(lep,reg,bin,sigstring,yr,outfile=None):
         cmd = 'echo "set -e; MYTMPFILE=\$(mktemp); python susy-sos/sos_plots.py --lep %s --reg %s --bin %s --doWhat cards --justdump %s %s %s/bare %s > \${MYTMPFILE}; source \${MYTMPFILE}; rm \${MYTMPFILE};"'%(lep,reg,bin,opts,sigstring,odir,yr)
         if outfile:
            cmd += " >> %s"%outfile
         os.system(cmd)

      def printCmd(job,outfile=None):
         expoutput=[]
         yrs = set([tk.yr for tk in job])
         cats = set([tk.cat for tk in job])
         # always merge different processes in the same yr,cat
         allprs = set([tk.pr for pr in job])
         reUseSkim = False
         keepSkim = False
         if len(allprs)==1 and len(yrs)==1 and ('background' not in allprs):
            reUseSkim = True
            keepSkim = True
         for yr in yrs:
            for _cat in cats:
               cat = _cat.replace('/','_')
               prs = set([tk.pr for tk in job if (yr==tk.yr and _cat==tk.cat)])
               lep,reg,bin = _cat.split('/')
               if 'background' in prs:
                  _printCmd(lep,reg,bin,'--data --nCores 4',yr,outfile)
                  expoutput.append('%s/bare/%s/%s/nosignal/sos_%s.bare.root'%(odir,yr,cat,cat))
               prs.discard('background')
               if len(prs):
                  if reUseSkim:
                     if keepSkim:
                        skim_instr='--preskim --keep-preskim'
                        keepSkim = False
                     else:
                        skim_instr='--inputDir \${MYTEMPSKIMDIR}'
                  else:
                     skim_instr='--preskim'
                  _printCmd(lep,reg,bin,'%s --nCores 1 --signal --signalMasses '%skim_instr+','.join(['signal_%s'%pr for pr in prs if pr!='background']),yr,outfile)
                  if len(prs)>1: raise
                  for _pr in prs: pr=_pr
                  expoutput.append('%s/bare/%s/%s/%s/sos_%s.bare.root'%(odir,yr,cat,pr,cat))
         if reUseSkim:
            cmd = 'echo "rm -r \${MYTEMPSKIMDIR}"'
            if outfile:
               cmd += " >> %s"%outfile
            os.system(cmd)
         return expoutput

      def splitStrategyFull():
         return [[x] for x in tasks]

      def splitStrategyByProc():
         jobs = {}
         for tk in tasks:
            if tk.pr not in jobs: jobs[tk.pr]=[]
            jobs[tk.pr].append(tk)
         return jobs.values()

      def splitStrategyByWhat(keyer):
         jobs = {}
         for tk in tasks:
            key = keyer(tk)
            if key not in jobs: jobs[key]=[]
            jobs[key].append(tk)
         return jobs.values()

      jobs=filter(lambda job: any([tk.pr=='background' for tk in job]),splitStrategyByWhat(lambda tk: (tk.yr,tk.cat,tk.pr=='background')))
      jobs+=filter(lambda job: all([tk.pr!='background' for tk in job]),splitStrategyByWhat(lambda tk: (tk.pr,tk.yr)))

      prepSubmission(odir,'card_submission',duration)

      for i,job in enumerate(jobs):
         outfiles=printCmd(job,"%s/card_submission/job_%d_%s.sh"%(odir,i,'bkg' if any([tk.pr=='background' for tk in job]) else 'sig'))
         for outf in outfiles:
            os.system("echo %s >> %s/card_submission/job_%d_expoutput.txt"%(outf,odir,i))



class merge_and_fit:
   def __init__(self,onlyFit=False, bkgdDir=None):
      self.onlyFit = onlyFit


      def runPoint(pr):
         ret=[]
         cards=[]
         out=[]
         badPoint = False
         splitted = pr.rstrip('+').split('_')
         model,m1,m2 = splitted[:3]
         tags = splitted[3:]
         if len(tags)>0:
            model += '-'+'-'.join(splitted[3:])
         mass = '%s_%s'%(m1,m2)
         fullpoint = '%s_%s'%(model,mass)
         if not onlyFit:
            for (_cat,yr) in itertools.product(categories,years):
               cat = _cat.replace('/','_')
               lep,reg,bin = _cat.split('/')
               f = '%s/bare/%s/%s/%s/sos_%s.bare.root'%(odir,yr,cat,pr.rstrip('+'),cat)
               f0 = '%s/bare/%s/%s/nosignal/sos_%s.bare.root'%(bkgdDir if bkgdDir else odir,yr,cat,cat)
               f2 = '%s_merged/bare/%s/%s/%s/sos_%s.bare.root'%(odir,yr,cat,pr.rstrip('+'),cat)
               if not (os.path.exists(f) and os.path.exists(f0)):
                  badPoint = True
                  break
               else:
                  out.append("set -e; mkdir -p \$(dirname %s)"%f2)
                  out.append("hadd -f %s %s %s"%(f2,f,f0))
                  out.append("MYTMPFILE=\$(mktemp); python susy-sos/sos_plots.py --lep %s --reg %s --bin %s --data --asimov background --doWhat cards %s --signal --signalMasses %s --allowRest --infile %s_merged/bare %s > \${MYTMPFILE}; source \${MYTMPFILE}; rm \${MYTMPFILE};"%(lep,reg,bin,opts,pr,odir,yr))
                  cards.append(('sos_'+cat+'_'+yr,os.path.dirname(f2)+'/sos_%s.txt'%cat))
            if badPoint:
               print 'Skipping %s because not all bare inputs are present'%pr
               return []

         out.append('export ORIGDIR=\$(pwd)')
         cdir = '%s_merged/cards/%s'%(odir,fullpoint)
         out.append("mkdir -p %s && cd %s && set +e"%(cdir,cdir))
         flags = {
            'all': lambda (x,y): True,
            '2lep': lambda (x,y): ('2los_' in x or 'cr_' in x),
            '3lep': lambda (x,y): ('3l_' in x or 'cr_' in x),
         }
         for tag,filt in flags.iteritems():
            cn = 'card_%s_%s.txt'%(fullpoint,tag)
            if not onlyFit: out.append("combineCards.py %s > %s"%(' '.join(['%s=%s'%(x,y) for x,y in filter(filt,cards)]), cn))
            elif os.path.exists(cdir+'/'+cn): return []
            out.append("combine -M AsymptoticLimits -t -1 --expectSignal 0 --run blind -n _%s_%s -m %s %s 2>&1 > log_b_%s_%s.txt"%(fullpoint,tag,m1,cn,fullpoint,tag)) # bkg-only asimov
            out.append("combine -M AsymptoticLimits -t -1 --expectSignal 1 --run blind -n _%s_%s -m %s %s 2>&1 > log_s_%s_%s.txt"%(fullpoint,tag,m1,cn,fullpoint,tag)) # sig-injected asimov
            out.append("combine -M FitDiagnostics --setParameterRanges r=-10,10 -t -1 -n _%s_%s -m %s %s 2>&1 > log_mlfit_%s_%s.txt"%(fullpoint,tag,m1,cn,fullpoint,tag)) # ML fit
         out.append("cd \${ORIGDIR}")
         return out

      prepSubmission(odir,'fit_submission',duration)

      for i,pr in enumerate(signals):
         outfile='%s/fit_submission/job_%d_fit.sh'%(odir,i)
         outlines = runPoint(pr)
         for line in outlines:
            os.system('echo "%s" >> %s/fit_submission/job_%d_fit.sh'%(line,odir,i))

if __name__ == '__main__':
   if what=='bare': x = bare_production()
   if what=='fit': x = merge_and_fit(onlyFit=args.onlyFit, bkgdDir=args.reuseBackground)
