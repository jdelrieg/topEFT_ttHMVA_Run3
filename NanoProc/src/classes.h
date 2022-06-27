#include "CMGTools/NanoProc/interface/SignedImpactParameter.h"
#include "CMGTools/NanoProc/interface/DistributionRemapper.h"
#include "CMGTools/NanoProc/interface/PdfWeightProducerTool.h"
#include "CMGTools/NanoProc/interface/IgProfHook.h"
#include "CMGTools/NanoProc/interface/CollectionSkimmer.h"
#include "CMGTools/NanoProc/interface/CombinedObjectTags.h"
#include "CMGTools/NanoProc/interface/TensorFlowInterface.h"

namespace {
    struct dictionary {
        SignedImpactParameter sipc;
        DistributionRemapper remapper;
        PdfWeightProducerTool pdfw;
        SetupIgProfDumpHook hook;
        TensorFlowInterface tf;
    };
}
