import FWCore.ParameterSet.Config as cms

MssmHbbNtuplizerTriggerPathsHLT = cms.PSet(
    TriggerPaths    = cms.vstring  (
    ## I recommend using the version number explicitly to be able to compare 
    ## however for production one has to be careful that all versions are included.
    ## Thinking of a better solution...
                   'HLT_ZeroBias_v',
                   'HLT_Mu12_DoublePFJets40_CaloBTagCSV_p33_v',
                   'HLT_Mu12_DoublePFJets40_CaloBTagCSV0p80_px_v',
                   'HLT_Mu12_DoublePFJets40_CaloBTagCSV0p84_px_v',
                   'HLT_Mu12_DoublePFJets40_CaloBTagCSV0p88_px_v',
                   'HLT_Mu12_DoublePFJets40MaxDeta1p6_DoubleCaloBTagCSV_p33_v',
                   'HLT_Mu12_DoublePFJets40MaxDeta1p6_DoubleCaloBTagCSV0p80_px_v',
                   'HLT_Mu12_DoublePFJets40MaxDeta1p6_DoubleCaloBTagCSV0p84_px_v',
                   'HLT_Mu12_DoublePFJets40MaxDeta1p6_DoubleCaloBTagCSV0p88_px_v',
                   'HLT_DoublePFJets40_CaloBTagCSV_p33_v',
                   'HLT_DoublePFJets40_CaloBTagCSV0p80_px_v',
                   'HLT_DoublePFJets40_CaloBTagCSV0p84_px_v',
                   'HLT_DoublePFJets40_CaloBTagCSV0p88_px_v',
                   'HLT_DoublePFJets100_CaloBTagCSV_p33_v',
                   'HLT_DoublePFJets100_CaloBTagCSV0p80_px_v',
                   'HLT_DoublePFJets100_CaloBTagCSV0p84_px_v',
                   'HLT_DoublePFJets100_CaloBTagCSV0p88_px_v',
                   'HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_p33_v',
                   'HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV0p80_px_v',
                   'HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV0p84_px_v',
                   'HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV0p88_px_v',
                   'HLT_SingleJet30_Mu12_SinglePFJet40_v',
                   'HLT_PFJet40_v',
                   'HLT_Mu8_v',
                   'HLT_Mu3_PFJet40_v',
                   'HLT_DoublePFJets40_v',
                   'HLT_Mu12_v',
                   'HLT_Mu12_PFJet40_v',
    ),
)

