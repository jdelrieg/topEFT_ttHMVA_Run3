#include "CMGTools/Heppy/interface/BTagSF.h"
#include "CMGTools/Heppy/interface/RochCor.h"
#include "CMGTools/Heppy/interface/RochCor2012.h"
#include "CMGTools/Heppy/interface/FSRWeightAlgo.h"
#include "CMGTools/Heppy/interface/CMGMuonCleanerBySegmentsAlgo.h"
#include "CMGTools/Heppy/interface/TriggerBitChecker.h"
#include "CMGTools/Heppy/interface/MuScleFitCorrector.h"
#include "CMGTools/Heppy/interface/EGammaMvaEleEstimatorFWLite.h"
#include "CMGTools/Heppy/interface/Davismt2.h"
#include "CMGTools/Heppy/interface/mt2w_bisect.h"
#include "CMGTools/Heppy/interface/Hemisphere.h"
#include "CMGTools/Heppy/interface/AlphaT.h"
#include "CMGTools/Heppy/interface/Apc.h"
#include "CMGTools/Heppy/interface/JetUtils.h"
#include "CMGTools/Heppy/interface/Megajet.h"
#include "CMGTools/Heppy/interface/ReclusterJets.h"
#include "CMGTools/Heppy/interface/IsolationComputer.h"
#include "CMGTools/Heppy/interface/FloatZipper.h"
#include "CMGTools/Heppy/interface/PATTauDiscriminationByMVAIsolationRun2FWlite.h"

#include "EgammaAnalysis/ElectronTools/interface/SimpleElectron.h"
#include "EgammaAnalysis/ElectronTools/interface/ElectronEPcombinator.h"
//#include "EgammaAnalysis/ElectronTools/interface/ElectronEnergyCalibrator.h"

#include "CMGTools/Heppy/interface/PdfWeightProducerTool.h"
#include "CMGTools/Heppy/interface/genutils.h"

#include <vector>
namespace {
  struct heppy_dictionary {
    heppy::BTagSF  bTagSF_; 
    heppy::RochCor rc_;
    heppy::RochCor2012 rc2012_;
    heppy::PdfWeightProducerTool  pdfw_; 
    heppy::FSRWeightAlgo walgo_;
    heppy::TriggerBitChecker checker;
    heppy::CMGMuonCleanerBySegmentsAlgo cmgMuonCleanerBySegmentsAlgo;
    heppy::EGammaMvaEleEstimatorFWLite egMVA;
    heppy::Hemisphere hemisphere(std::vector<float> px, 
				 std::vector<float> py, 
				 std::vector<float> pz, 
				 std::vector<float> E, int hemi_seed, 
				 int hemi_association);
    heppy::Hemisphere hemisphere_;
    heppy::Davismt2 mt2;
    heppy::mt2w_bisect::mt2w mt2wlept;
    heppy::AlphaT alphaT;
    heppy::Apc apc;
    heppy::Megajet megajet;
    heppy::ReclusterJets reclusterJets(std::vector<float> px, std::vector<float> py, std::vector<float> pz, std::vector<float> E, double ktpower, double rparam);
    heppy::JetUtils jetUtils;
    //  heppy::SimpleElectron fuffaElectron;
    //  ElectronEnergyCalibrator fuffaElectronCalibrator;
    //  heppy::ElectronEPcombinator fuffaElectronCombinator;
    heppy::PATTauDiscriminationByMVAIsolationRun2FWlite PATTauDiscriminationByMVAIsolationRun2FWlite_;

  };
}
