import FWCore.ParameterSet.Config as cms

MssmHbbTriggerResultsFilter = cms.PSet(
    triggerConditions = cms.vstring(
# physics triggers
                                     'HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTag*CSV_p*_v*', 
                                     'HLT_Mu12_DoublePFJets40MaxDeta1p6_DoubleCaloBTag*CSV_p*_v*',
# backup triggers                                     
                                     'HLT_DoublePFJets128MaxDeta1p6_DoubleCaloBTag*CSV_p*_v*', 
                                     'HLT_Mu12_DoublePFJets54MaxDeta1p6_DoubleCaloBTag*CSV_p*_v*', 
                                     'HLT_Mu12_DoublePFJets62MaxDeta1p6_DoubleCaloBTag*CSV_p*_v*',
                                     
# addictional triggers
                                     'HLT_AK8PFJet360_TrimMass30_v*',
                                     'HLT_AK8PFJet380_TrimMass30_v*',
                                     'HLT_AK8PFJet400_TrimMass30_v*',
                                     'HLT_AK8PFJet420_TrimMass30_v*',
                                     'HLT_AK8PFJet330_TrimMass30_PFAK8BTag*CSV_p17_v*',
                                     'HLT_AK8PFJet330_TrimMass30_PFAK8BTag*CSV_p1_v*',
                                     'HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_p02_v*',


# control triggers
### btag                             
                                     'HLT_SingleJet30_Mu12_SinglePFJet40_v*', 
                                     'HLT_DoublePFJets40_CaloBTag*CSV_p*_v*', 
                                     'HLT_DoublePFJets100_CaloBTag*CSV_p*_v*', 
                                     'HLT_DoublePFJets200_CaloBTag*CSV_p*_v*', 
                                     'HLT_DoublePFJets350_CaloBTag*CSV_p*_v*', 
                                     'HLT_Mu12_DoublePFJets40_CaloBTag*CSV_p*_v*', 
                                     'HLT_Mu12_DoublePFJets100_CaloBTag*CSV_p*_v*', 
                                     'HLT_Mu12_DoublePFJets200_CaloBTag*CSV_p*_v*', 
                                     'HLT_Mu12_DoublePFJets350_CaloBTag*CSV_p*_v*',
### jet triggers
                                     'HLT_PFJet40_v*', 
                                     'HLT_PFJet60_v*', 
                                     'HLT_PFJet80_v*', 
                                     'HLT_PFJet140_v*', 
                                     'HLT_PFJet200_v*', 
                                     'HLT_PFJet260_v*', 
                                     'HLT_PFJet320_v*', 
                                     'HLT_PFJet400_v*', 
                                     'HLT_PFJet450_v*', 
                                     'HLT_PFJet500_v*', 
                                     'HLT_PFJet550_v*',
                                     'HLT_DiPFJetAve40_v*',
                                     'HLT_DiPFJetAve80_v*',
                                     'HLT_DiPFJetAve200_v*',
                                     'HLT_DiPFJetAve320_v*',
                                     'HLT_DiPFJetAve500_v*',
                                      

### muon triggers
                                     'HLT_Mu8_v*', 
                                     'HLT_Mu50_v*',
                                     'HLT_Mu55_v*',
                                     'HLT_Mu3_PFJet40_v*', 
### zerobias trigger                                     
                                     'HLT_ZeroBias_v*',
                                     
### additional
                                     'HLT_AK8PFJet320_v*',
                                     'HLT_AK8PFJet400_v*',
                                     'HLT_AK8PFJet450_v*',
                                     'HLT_AK8PFJet500_v*',
                                     'HLT_AK8PFJet550_v*',
                     
    )
)
