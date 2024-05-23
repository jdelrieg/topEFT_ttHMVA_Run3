import ROOT
import sys

# this script returns the number of entries in a friend tree file

for myfile in sys.argv[1:]:
    f = ROOT.TFile.Open(myfile)
    t = f.Get("Friends")
    print((myfile+': '), end=' ')
    print(t.GetEntries())
    f.Close()
