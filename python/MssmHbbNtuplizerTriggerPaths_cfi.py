import FWCore.ParameterSet.Config as cms

MssmHbbNtuplizerTriggerPaths = cms.PSet(
    TriggerPaths    = cms.vstring  (
    ## I recommend using the version number explicitly to be able to compare 
    ## however for production one has to be careful that all versions are included.
    ## Thinking of a better solution...
# physics triggers
                                     'HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v', 
                                     'HLT_Mu12_DoublePFJets40MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v',
                                     # csvv2
                                     'HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTagCSV_p79_v', 
                                     'HLT_Mu12_DoublePFJets40MaxDeta1p6_DoubleCaloBTagCSV_p79_v',
# backup triggers                                     
                                     'HLT_DoublePFJets128MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v', 
                                     'HLT_Mu12_DoublePFJets54MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v', 
                                     'HLT_Mu12_DoublePFJets62MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v',
                                     # csvv2
                                     'HLT_DoublePFJets128MaxDeta1p6_DoubleCaloBTagCSV_p79_v', 
                                     'HLT_Mu12_DoublePFJets54MaxDeta1p6_DoubleCaloBTagCSV_p79_v', 
                                     'HLT_Mu12_DoublePFJets62MaxDeta1p6_DoubleCaloBTagCSV_p79_v',
                                     
# addictional triggers
                                     'HLT_AK8PFJet360_TrimMass30_v',
                                     'HLT_AK8PFJet380_TrimMass30_v',
                                     'HLT_AK8PFJet400_TrimMass30_v',
                                     'HLT_AK8PFJet420_TrimMass30_v',
                                     'HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17_v',
                                     'HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1_v',
                                     # csvv2
                                     'HLT_AK8PFJet330_TrimMass30_PFAK8BTagCSV_p17_v',
                                     'HLT_AK8PFJet330_TrimMass30_PFAK8BTagCSV_p1_v',
                                     'HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_p02_v',


# control triggers
### btag                             
                                     'HLT_SingleJet30_Mu12_SinglePFJet40_v', 
                                     'HLT_DoublePFJets40_CaloBTagDeepCSV_p71_v', 
                                     'HLT_DoublePFJets100_CaloBTagDeepCSV_p71_v', 
                                     'HLT_DoublePFJets200_CaloBTagDeepCSV_p71_v', 
                                     'HLT_DoublePFJets350_CaloBTagDeepCSV_p71_v', 
                                     'HLT_Mu12_DoublePFJets40_CaloBTagDeepCSV_p71_v', 
                                     'HLT_Mu12_DoublePFJets100_CaloBTagDeepCSV_p71_v', 
                                     'HLT_Mu12_DoublePFJets200_CaloBTagDeepCSV_p71_v', 
                                     'HLT_Mu12_DoublePFJets350_CaloBTagDeepCSV_p71_v',
                                     # csvv2
                                     'HLT_DoublePFJets40_CaloBTagCSV_p79_v', 
                                     'HLT_DoublePFJets100_CaloBTagCSV_p79_v', 
                                     'HLT_DoublePFJets200_CaloBTagCSV_p79_v', 
                                     'HLT_DoublePFJets350_CaloBTagCSV_p79_v', 
                                     'HLT_Mu12_DoublePFJets40_CaloBTagCSV_p79_v', 
                                     'HLT_Mu12_DoublePFJets100_CaloBTagCSV_p79_v', 
                                     'HLT_Mu12_DoublePFJets200_CaloBTagCSV_p79_v', 
                                     'HLT_Mu12_DoublePFJets350_CaloBTagCSV_p79_v',
### jet triggers
                                     'HLT_PFJet40_v', 
                                     'HLT_PFJet60_v', 
                                     'HLT_PFJet80_v', 
                                     'HLT_PFJet140_v', 
                                     'HLT_PFJet200_v', 
                                     'HLT_PFJet260_v', 
                                     'HLT_PFJet320_v', 
                                     'HLT_PFJet400_v', 
                                     'HLT_PFJet450_v', 
                                     'HLT_PFJet500_v', 
                                     'HLT_PFJet550_v',
                                     'HLT_DiPFJetAve40_v',
                                     'HLT_DiPFJetAve60_v',
                                     'HLT_DiPFJetAve80_v',
                                     'HLT_DiPFJetAve140_v',
                                     'HLT_DiPFJetAve200_v',
                                     'HLT_DiPFJetAve260_v',
                                     'HLT_DiPFJetAve320_v',
                                     'HLT_DiPFJetAve400_v',
                                     'HLT_DiPFJetAve500_v',
                                      

### muon triggers
                                     'HLT_Mu8_v', 
                                     'HLT_Mu17_v', 
                                     'HLT_Mu19_v', 
                                     'HLT_Mu20_v', 
                                     'HLT_Mu27_v', 
                                     'HLT_Mu50_v',
                                     'HLT_Mu55_v',
                                     'HLT_Mu3_PFJet40_v', 
### zerobias trigger                                     
                                     'HLT_ZeroBias_v',
                                     
### additional
                                     'HLT_AK8PFJet320_v',
                                     'HLT_AK8PFJet400_v',
                                     'HLT_AK8PFJet450_v',
                                     'HLT_AK8PFJet500_v',
                                     'HLT_AK8PFJet550_v',


                                     
    ),
)

