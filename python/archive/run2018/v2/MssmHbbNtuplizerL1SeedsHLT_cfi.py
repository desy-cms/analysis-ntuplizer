import FWCore.ParameterSet.Config as cms

MssmHbbNtuplizerL1SeedsHLT = cms.PSet(
   L1Seeds    = cms.vstring  (
                                     'L1_ZeroBias',
                                     'L1_Mu3_Jet16er2p7_dEta_Max0p4_dPhi_Max0p4',
                                     'L1_Mu12er2p3_Jet40er2p3_dR_Max0p4_DoubleJet40er2p3_dEta_Max1p6',
                                     'L1_DoubleJet40er2p7',
                                     'L1_DoubleJet100er2p7',
                                     'L1_DoubleJet100er2p3_dEta_Max1p6',
                                     'L1_DoubleJet112er2p3_dEta_Max1p6',
                                     'L1_Mu3_Jet16er2p7_dEta_Max0p4_dPhi_Max0p4',
                                     'L1_SingleMu3',
                                     'L1_SingleMu5',
                                     'L1_SingleMu7',
                                     'L1_Mu3_Jet30er2p5',
   ),
)
