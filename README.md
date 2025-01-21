# Short recipe for CMGTools 

For the general recipe, [follow these instructions](https://twiki.cern.ch/twiki/bin/view/CMS/CMGToolsReleasesExperimental).

--------------

#### Set up CMSSW and the base git

```
cmsrel CMSSW_14_0_6
cd CMSSW_14_0_6/src
cmsenv
git cms-init
```

<!--#### Add the central cmg-cmssw repository to get the Heppy 80X branch

%```
%git remote add cmg-central https://github.com/CERN-PH-CMG/cmg-cmssw.git -f  -t heppy_80X
%```

#### Configure the sparse checkout, and get the base heppy packages

```
cp /afs/cern.ch/user/c/cmgtools/public/sparse-checkout_80X_heppy .git/info/sparse-checkout
git checkout -b heppy_80X cmg-central/heppy_80X
```

#### Add your mirror, and push the 80X branch to it

```
git remote add origin git@github.com:YOUR_GITHUB_REPOSITORY/cmg-cmssw.git
git push -u origin heppy_80X
```
-->
#### Now get the CMGTools subsystem from the cmgtools-lite repository

```
git clone https://github.com/jdelrieg/topEFT_ttHMVA_Run3.git -b newcmgtools_python3 CMGTools
cd CMGTools
```

#### Add your fork, and push the 80X branch to it

```
git remote add origin  git@github.com:YOUR_GITHUB_REPOSITORY/cmgtools-lite.git
git push -u origin 80X
```

#### Compile

```
cd $CMSSW_BASE/src
scram b -j 8
```
