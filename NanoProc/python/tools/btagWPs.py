_btagWPs = {
    "TCHEL": ("pfTrackCountingHighEffBJetTags", 1.7),
    "TCHEM": ("pfTrackCountingHighEffBJetTags", 3.3),
    "TCHPT": ("pfTrackCountingHighPurBJetTags", 3.41),
    "JPL": ("pfJetProbabilityBJetTags", 0.275),
    "JPM": ("pfJetProbabilityBJetTags", 0.545),
    "JPT": ("pfJetProbabilityBJetTags", 0.790),
    "CSVL": ("combinedSecondaryVertexBJetTags", 0.244),
    "CSVM": ("combinedSecondaryVertexBJetTags", 0.679),
    "CSVT": ("combinedSecondaryVertexBJetTags", 0.898),
###https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation74X50ns
    "CMVAL": ("pfCombinedMVABJetTags", 0.630), # for same b-jet efficiency of CSVv2IVFL on ttbar MC, jet pt > 30
    "CMVAM": ("pfCombinedMVABJetTags", 0.732), # for same b-jet efficiency of CSVv2IVFM on ttbar MC, jet pt > 30
    "CMVAT": ("pfCombinedMVABJetTags", 0.813), # for same b-jet efficiency of CSVv2IVFT on ttbar MC, jet pt > 30
    "CMVAv2M": ("pfCombinedMVAV2BJetTags", 0.185), # for same b-jet efficiency of CSVv2IVFM on ttbar MC, jet pt > 30
###https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80X
    "CSVv2IVFL": ("pfCombinedInclusiveSecondaryVertexV2BJetTags", 0.460),
    "CSVv2IVFM": ("pfCombinedInclusiveSecondaryVertexV2BJetTags", 0.800),
    "CSVv2IVFT": ("pfCombinedInclusiveSecondaryVertexV2BJetTags", 0.935),
    "CMVAv2L": ("pfCombinedMVAV2BJetTags", -0.715), # for same b-jet efficiency of CSVv2IVFL on ttbar MC, jet pt > 30
    "CMVAv2M": ("pfCombinedMVAV2BJetTags", 0.185),  # for same b-jet efficiency of CSVv2IVFM on ttbar MC, jet pt > 30
    "CMVAv2T": ("pfCombinedMVAV2BJetTags", 0.875),  # for same b-jet efficiency of CSVv2IVFT on ttbar MC, jet pt > 30
###https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation94X
    "CSVv2IVF94XL": ("pfCombinedInclusiveSecondaryVertexV2BJetTags", 0.5803),
    "CSVv2IVF94XM": ("pfCombinedInclusiveSecondaryVertexV2BJetTags", 0.8838),
    "CSVv2IVF94XT": ("pfCombinedInclusiveSecondaryVertexV2BJetTags", 0.9693),
    "DeepCSVL": ("pfDeepCSVJetTags:probb + pfDeepCSVJetTags:probbb", 0.1522),
    "DeepCSVM": ("pfDeepCSVJetTags:probb + pfDeepCSVJetTags:probbb", 0.4941),
    "DeepCSVT": ("pfDeepCSVJetTags:probb + pfDeepCSVJetTags:probbb", 0.8001),
### Full run 2, year-by-year WPs:  
 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation2016Legacy
 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation102X
    "DeepCSV_2016_L": ("pfDeepCSVJetTags:probb + pfDeepCSVJetTags:probbb", 0.2217),
    "DeepCSV_2016_M": ("pfDeepCSVJetTags:probb + pfDeepCSVJetTags:probbb", 0.6321),
    "DeepCSV_2016_T": ("pfDeepCSVJetTags:probb + pfDeepCSVJetTags:probbb", 0.8953),
    "DeepCSV_2017_L": ("pfDeepCSVJetTags:probb + pfDeepCSVJetTags:probbb", 0.1522),
    "DeepCSV_2017_M": ("pfDeepCSVJetTags:probb + pfDeepCSVJetTags:probbb", 0.4941),
    "DeepCSV_2017_T": ("pfDeepCSVJetTags:probb + pfDeepCSVJetTags:probbb", 0.8001),
    "DeepCSV_2018_L": ("pfDeepCSVJetTags:probb + pfDeepCSVJetTags:probbb", 0.1241),
    "DeepCSV_2018_M": ("pfDeepCSVJetTags:probb + pfDeepCSVJetTags:probbb", 0.4184),
    "DeepCSV_2018_T": ("pfDeepCSVJetTags:probb + pfDeepCSVJetTags:probbb", 0.7527),
    "DeepFlav_2016_L": ("pfDeepFlavourJetTags:probb + pfDeepFlavourJetTags:probbb + pfDeepFlavourJetTags:problepb", 0.0614),
    "DeepFlav_2016_M": ("pfDeepFlavourJetTags:probb + pfDeepFlavourJetTags:probbb + pfDeepFlavourJetTags:problepb", 0.3093),
    "DeepFlav_2016_T": ("pfDeepFlavourJetTags:probb + pfDeepFlavourJetTags:probbb + pfDeepFlavourJetTags:problepb", 0.7221),
    "DeepFlav_2017_L": ("pfDeepFlavourJetTags:probb + pfDeepFlavourJetTags:probbb + pfDeepFlavourJetTags:problepb", 0.0521),
    "DeepFlav_2017_M": ("pfDeepFlavourJetTags:probb + pfDeepFlavourJetTags:probbb + pfDeepFlavourJetTags:problepb", 0.3033),
    "DeepFlav_2017_T": ("pfDeepFlavourJetTags:probb + pfDeepFlavourJetTags:probbb + pfDeepFlavourJetTags:problepb", 0.7489),
    "DeepFlav_2018_L": ("pfDeepFlavourJetTags:probb + pfDeepFlavourJetTags:probbb + pfDeepFlavourJetTags:problepb", 0.0494),
    "DeepFlav_2018_M": ("pfDeepFlavourJetTags:probb + pfDeepFlavourJetTags:probbb + pfDeepFlavourJetTags:problepb", 0.2770),
    "DeepFlav_2018_T": ("pfDeepFlavourJetTags:probb + pfDeepFlavourJetTags:probbb + pfDeepFlavourJetTags:problepb", 0.7264),
}
