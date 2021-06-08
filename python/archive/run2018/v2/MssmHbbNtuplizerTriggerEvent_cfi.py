import FWCore.ParameterSet.Config as cms

MssmHbbNtuplizerTriggerEvent = cms.PSet(
   TriggerObjectLabels    = cms.vstring  (
                                             
                                           'hltL1sZeroBias',
                                           
                                           'hltL1sMu3JetC16dEtaMax0p4dPhiMax0p4',
                                           'hltL1fL1sMu3Jet16L1Filtered0',
                                           'hltDoubleCaloBJets30eta2p3',
                                           'hltBTagCalo30x8CSVp0p92SingleWithMatching',
                                           'hltL3fL1sMu3Jet16L1f0L2f8L3Filtered12',
                                           'hltDoublePFBJets40Eta2p3',
                                           'hltBSoftMuonDiJet40Mu12L3FilterByDR',
                                           
                                           'hltL1sMu3JetC16dEtaMax0p4dPhiMax0p4',
                                           'hltL1fL1sMu3Jet16L1Filtered0',
                                           'hltDoubleCaloBJets30eta2p3',
                                           'hltBTagCalo30x8CSVp0p80SingleWithMatching',
                                           'hltL3fL1sMu3Jet16L1f0L2f8L3Filtered12',
                                           'hltDoublePFBJets40Eta2p3',
                                           'hltBSoftMuonDiJet40Mu12L3FilterByDR',


                                           'hltL1sMu3JetC16dEtaMax0p4dPhiMax0p4',
                                           'hltL1fL1sMu3Jet16L1Filtered0',
                                           'hltDoubleCaloBJets30eta2p3',
                                           'hltBTagCalo30x8CSVp0p84SingleWithMatching',
                                           'hltL3fL1sMu3Jet16L1f0L2f8L3Filtered12',
                                           'hltDoublePFBJets40Eta2p3',
                                           'hltBSoftMuonDiJet40Mu12L3FilterByDR',


                                           'hltL1sMu3JetC16dEtaMax0p4dPhiMax0p4',
                                           'hltL1fL1sMu3Jet16L1Filtered0',
                                           'hltDoubleCaloBJets30eta2p3',
                                           'hltBTagCalo30x8CSVp0p88SingleWithMatching',
                                           'hltL3fL1sMu3Jet16L1f0L2f8L3Filtered12',
                                           'hltDoublePFBJets40Eta2p3',
                                           'hltBSoftMuonDiJet40Mu12L3FilterByDR',

                                           'hltL1Mu12er2p3Jet40er2p3dRMax0p4DoubleJet40er2p3dEtaMax1p6',
                                           'hltL1fL1sMu12Dijet40L1Filtered0',
                                           'hltDoubleCaloBJets30eta2p3',
                                           'hltBTagCalo30x8CSVp0p92DoubleWithMatching',
                                           'hltL3fL1sMu12Dijet40L1f0L2f8L3Filtered12',
                                           'hltDoublePFBJets40Eta2p3',
                                           'hltDoublePFJets40Eta2p3MaxDeta1p6',
                                           'hltBSoftMuonDiJet40Mu12L3FilterByDR',

                                           'hltL1Mu12er2p3Jet40er2p3dRMax0p4DoubleJet40er2p3dEtaMax1p6',
                                           'hltL1fL1sMu12Dijet40L1Filtered0',
                                           'hltDoubleCaloBJets30eta2p3',
                                           'hltBTagCalo30x8CSVp0p80DoubleWithMatching',
                                           'hltL3fL1sMu12Dijet40L1f0L2f8L3Filtered12',
                                           'hltDoublePFBJets40Eta2p3',
                                           'hltDoublePFJets40Eta2p3MaxDeta1p6',
                                           'hltBSoftMuonDiJet40Mu12L3FilterByDR',


                                           'hltL1Mu12er2p3Jet40er2p3dRMax0p4DoubleJet40er2p3dEtaMax1p6',
                                           'hltL1fL1sMu12Dijet40L1Filtered0',
                                           'hltDoubleCaloBJets30eta2p3',
                                           'hltBTagCalo30x8CSVp0p84DoubleWithMatching',
                                           'hltL3fL1sMu12Dijet40L1f0L2f8L3Filtered12',
                                           'hltDoublePFBJets40Eta2p3',
                                           'hltDoublePFJets40Eta2p3MaxDeta1p6',
                                           'hltBSoftMuonDiJet40Mu12L3FilterByDR',


                                           'hltL1Mu12er2p3Jet40er2p3dRMax0p4DoubleJet40er2p3dEtaMax1p6',
                                           'hltL1fL1sMu12Dijet40L1Filtered0',
                                           'hltDoubleCaloBJets30eta2p3',
                                           'hltBTagCalo30x8CSVp0p88DoubleWithMatching',
                                           'hltL3fL1sMu12Dijet40L1f0L2f8L3Filtered12',
                                           'hltDoublePFBJets40Eta2p3',
                                           'hltDoublePFJets40Eta2p3MaxDeta1p6',
                                           'hltBSoftMuonDiJet40Mu12L3FilterByDR',


                                           'hltL1DoubleJet40er3p0',
                                           'hltDoubleCaloBJets30eta2p3',
                                           'hltBTagCalo30x8CSVp0p92SingleWithMatching',
                                           'hltDoublePFJets40Eta2p3',


                                           'hltL1DoubleJet40er3p0',
                                           'hltDoubleCaloBJets30eta2p3',
                                           'hltBTagCalo30x8CSVp0p80SingleWithMatching',
                                           'hltDoublePFJets40Eta2p3',

                                           'hltL1DoubleJet40er3p0',
                                           'hltDoubleCaloBJets30eta2p3',
                                           'hltBTagCalo30x8CSVp0p84SingleWithMatching',
                                           'hltDoublePFJets40Eta2p3',


                                           'hltL1DoubleJet40er3p0',
                                           'hltDoubleCaloBJets30eta2p3',
                                           'hltBTagCalo30x8CSVp0p88SingleWithMatching',
                                           'hltDoublePFJets40Eta2p3',

                                           'hltL1DoubleJet100er3p0',
                                           'hltDoubleCaloBJets100eta2p3',
                                           'hltBTagCalo80x6CSVp0p92SingleWithMatching',
                                           'hltDoublePFJets100Eta2p3',

                                           'hltL1DoubleJet100er3p0',
                                           'hltDoubleCaloBJets100eta2p3',
                                           'hltBTagCalo80x6CSVp0p80SingleWithMatching',
                                           'hltDoublePFJets100Eta2p3',

                                           'hltL1DoubleJet100er3p0',
                                           'hltDoubleCaloBJets100eta2p3',
                                           'hltBTagCalo80x6CSVp0p84SingleWithMatching',
                                           'hltDoublePFJets100Eta2p3',

                                           'hltL1DoubleJet100er3p0',
                                           'hltDoubleCaloBJets100eta2p3',
                                           'hltBTagCalo80x6CSVp0p88SingleWithMatching',
                                           'hltDoublePFJets100Eta2p3',


                                           'hltL1DoubleJet100er2p3dEtaMax1p6Ior112er2p3dEtaMax1p6',
                                           'hltDoubleCaloBJets100eta2p3',
                                           'hltBTagCalo80x6CSVp0p92DoubleWithMatching',
                                           'hltDoublePFJets100Eta2p3',
                                           'hltDoublePFJets100Eta2p3MaxDeta1p6',


                                           'hltL1DoubleJet100er2p3dEtaMax1p6Ior112er2p3dEtaMax1p6',
                                           'hltDoubleCaloBJets100eta2p3',
                                           'hltBTagCalo80x6CSVp0p80DoubleWithMatching',
                                           'hltDoublePFJets100Eta2p3',
                                           'hltDoublePFJets100Eta2p3MaxDeta1p6',


                                           'hltL1DoubleJet100er2p3dEtaMax1p6Ior112er2p3dEtaMax1p6',
                                           'hltDoubleCaloBJets100eta2p3',
                                           'hltBTagCalo80x6CSVp0p84DoubleWithMatching',
                                           'hltDoublePFJets100Eta2p3',
                                           'hltDoublePFJets100Eta2p3MaxDeta1p6',


                                           'hltL1DoubleJet100er2p3dEtaMax1p6Ior112er2p3dEtaMax1p6',
                                           'hltDoubleCaloBJets100eta2p3',
                                           'hltBTagCalo80x6CSVp0p88DoubleWithMatching',
                                           'hltDoublePFJets100Eta2p3',
                                           'hltDoublePFJets100Eta2p3MaxDeta1p6',


                                           'hltL1sMu3JetC16dEtaMax0p4dPhiMax0p4',
                                           'hltL1fL1sMu3Jet16L1Filtered0',
                                           'hltSingleCaloBJets30eta2p3',
                                           'hltL3fL1sMu3Jet16L1f0L2f8L3Filtered12',
                                           'hltSinglePFBJets40Eta2p3',
                                           'hltBSoftMuonJet40Mu12L3FilterByDR',

                                           'hltL1sZeroBias',
                                           'hltSingleCaloJet10',
                                           'hltSinglePFJet40',

                                           'hltL1sSingleMu3IorSingleMu5IorSingleMu7',
                                           'hltL1fL1sMu5L1Filtered0',
                                           'hltL3fL1sMu5L1f0L2f5L3Filtered8',

                                           'hltL1sSingleMu3IorMu3Jet30er2p5',
                                           'hltL1fL1sMu3L1Filtered0',
                                           'hltL1sSingleJet35ObjectMap',
                                           'hltL3fL1sMu3L1f0L2f0L3Filtered3',
                                           'hltMu3PFJet40MuCleaned',


                                           'hltL1DoubleJet40er3p0',
                                           'hltDoubleCaloBJets30eta2p3',
                                           'hltDoublePFJets40Eta2p3',

                                           'hltL1sSingleMu3IorSingleMu5IorSingleMu7',
                                           'hltL1fL1sMu5L1Filtered0',
                                           'hltL3fL1sMu5L1f0L2f5L3Filtered12',

                                           'hltL1sSingleMu3IorMu3Jet30er2p5',
                                           'hltL1fL1sMu3L1Filtered0',
                                           'hltL1sSingleJet35ObjectMap',
                                           'hltL3fL1sMu3L1f0L2f0L3Filtered12',
                                           'hltMu12PFJet40MuCleaned',
                                             
                                             
   ),
)
