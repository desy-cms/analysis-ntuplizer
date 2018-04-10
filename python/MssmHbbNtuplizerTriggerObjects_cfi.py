import FWCore.ParameterSet.Config as cms

# if long list, use + cms.vstring or extend
# see https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideAboutPythonConfigFile#Modifying_Parameters
MssmHbbNtuplizerTriggerObjects = cms.PSet(
   TriggerObjectLabels    = ( cms.vstring  (  

                                             'hltL1DoubleJet100er2p3dEtaMax1p6',
                                             'hltL1DoubleJet100er2p3dEtaMax1p6Ior112er2p3dEtaMax1p6',
                                             'hltDoubleCaloBJets100eta2p3',
                                             'hltBTagCalo80x6CSVp0p92DoubleWithMatching',
                                             'hltDoublePFJets100Eta2p3',
                                             'hltDoublePFJets100Eta2p3MaxDeta1p6',

                                             'hltL1Mu12er2p3Jet40er2p3dRMax0p4DoubleJet40er2p3dEtaMax1p6',
                                             'hltL1fL1sMu12Dijet40L1Filtered0',
                                             'hltDoubleCaloBJets30eta2p3',
                                             'hltBTagCalo30x8CSVp0p92DoubleWithMatching',
                                             'hltL3fL1sMu12Dijet40L1f0L2f8L3Filtered12',
                                             'hltDoublePFBJets40Eta2p3',
                                             'hltDoublePFJets40Eta2p3MaxDeta1p6',
                                             'hltBSoftMuonDiJet40Mu12L3FilterByDR',

                                             'hltL1DoubleJet100er2p3dEtaMax1p6',
                                             'hltL1DoubleJet100er2p3dEtaMax1p6Ior112er2p3dEtaMax1p6',
                                             'hltDoubleCaloBJets100eta2p3',
                                             'hltBTagCalo80x6CSVp0p92DoubleWithMatching',
                                             'hltDoublePFJets116Eta2p3',
                                             'hltDoublePFJets116Eta2p3MaxDeta1p6',

                                             'hltL1DoubleJet100er2p3dEtaMax1p6',
                                             'hltL1DoubleJet100er2p3dEtaMax1p6Ior112er2p3dEtaMax1p6',
                                             'hltDoubleCaloBJets100eta2p3',
                                             'hltBTagCalo80x6CSVp0p92DoubleWithMatching',
                                             'hltDoublePFJets128Eta2p3',
                                             'hltDoublePFJets128Eta2p3MaxDeta1p6',

                                             'hltL1Mu12er2p3Jet40er2p3dRMax0p4DoubleJet40er2p3dEtaMax1p6',
                                             'hltL1fL1sMu12Dijet40L1Filtered0',
                                             'hltDoubleCaloBJets30eta2p3',
                                             'hltBTagCalo30x8CSVp0p92DoubleWithMatching',
                                             'hltL3fL1sMu12Dijet40L1f0L2f8L3Filtered12',
                                             'hltDoublePFBJets54Eta2p3',
                                             'hltDoublePFJets54Eta2p3MaxDeta1p6',
                                             'hltBSoftMuonDiJet54Mu12L3FilterByDR',

                                             'hltL1Mu12er2p3Jet40er2p3dRMax0p4DoubleJet40er2p3dEtaMax1p6',
                                             'hltL1fL1sMu12Dijet40L1Filtered0',
                                             'hltDoubleCaloBJets30eta2p3',
                                             'hltBTagCalo30x8CSVp0p92DoubleWithMatching',
                                             'hltL3fL1sMu12Dijet40L1f0L2f8L3Filtered12',
                                             'hltDoublePFBJets62Eta2p3',
                                             'hltDoublePFJets62Eta2p3MaxDeta1p6',
                                             'hltBSoftMuonDiJet62Mu12L3FilterByDR',

                                             'hltL1sMu3JetC16dEtaMax0p4dPhiMax0p4',
                                             'hltL1fL1sMu3Jet16L1Filtered0',
                                             'hltSingleCaloBJets30eta2p3',
                                             'hltL3fL1sMu3Jet16L1f0L2f8L3Filtered12',
                                             'hltSinglePFBJets40Eta2p3',
                                             'hltBSoftMuonJet40Mu12L3FilterByDR',

                                             'hltL1DoubleJet40er3p0',
                                             'hltDoubleCaloBJets30eta2p3',
                                             'hltBTagCalo30x8CSVp0p92SingleWithMatching',
                                             'hltDoublePFJets40Eta2p3',

                                             'hltL1DoubleJet100er3p0',
                                             'hltDoubleCaloBJets100eta2p3',
                                             'hltBTagCalo80x6CSVp0p92SingleWithMatching',
                                             'hltDoublePFJets100Eta2p3',

                                             'hltL1DoubleJet112er3p0',
                                             'hltL1DoubleJet120er3p0',
                                             'hltDoubleCaloBJets100eta2p3',
                                             'hltBTagCalo80x6CSVp0p92SingleWithMatching',
                                             'hltDoublePFJets200Eta2p3',

                                             'hltL1DoubleJet112er3p0',
                                             'hltL1DoubleJet120er3p0',
                                             'hltDoubleCaloBJets100eta2p3',
                                             'hltBTagCalo80x6CSVp0p92SingleWithMatching',
                                             'hltDoublePFJets350Eta2p3',

                                             'hltL1sMu3JetC16dEtaMax0p4dPhiMax0p4',
                                             'hltL1fL1sMu3Jet16L1Filtered0',
                                             'hltDoubleCaloBJets30eta2p3',
                                             'hltBTagCalo30x8CSVp0p92SingleWithMatching',
                                             'hltL3fL1sMu3Jet16L1f0L2f8L3Filtered12',
                                             'hltDoublePFBJets40Eta2p3',
                                             'hltBSoftMuonDiJet40Mu12L3FilterByDR',

                                             'hltL1sMu3JetC60dEtaMax0p4dPhiMax0p4',
                                             'hltL1fL1sMu3Jet60L1Filtered0',
                                             'hltDoubleCaloBJets30eta2p3',
                                             'hltBTagCalo30x8CSVp0p92SingleWithMatching',
                                             'hltL3fL1sMu3Jet60L1f0L2f8L3Filtered12',
                                             'hltDoublePFBJets100Eta2p3',
                                             'hltBSoftMuonDiJet100Mu12L3FilterByDR',

                                             'hltL1sMu3JetC120dEtaMax0p4dPhiMax0p4',
                                             'hltL1fL1sMu3Jet120L1Filtered0',
                                             'hltDoubleCaloBJets30eta2p3',
                                             'hltBTagCalo30x8CSVp0p92SingleWithMatching',
                                             'hltL3fL1sMu3Jet120L1f0L2f8L3Filtered12',
                                             'hltDoublePFBJets200Eta2p3',
                                             'hltBSoftMuonDiJet200Mu12L3FilterByDR',

                                             'hltL1sMu3JetC120dEtaMax0p4dPhiMax0p4',
                                             'hltL1fL1sMu3Jet120L1Filtered0',
                                             'hltDoubleCaloBJets30eta2p3',
                                             'hltBTagCalo30x8CSVp0p92SingleWithMatching',
                                             'hltL3fL1sMu3Jet120L1f0L2f8L3Filtered12',
                                             'hltDoublePFBJets350Eta2p3',
                                             'hltBSoftMuonDiJet350Mu12L3FilterByDR',
                                             
                                             'hltL1sZeroBias',
                                             'hltSingleCaloJet10',
                                             'hltSinglePFJet40',
                                             
                                             'hltL1sSingleJet35',
                                             'hltSingleCaloJet40',
                                             'hltSinglePFJet60',
                                             
                                             'hltL1sSingleJet60',
                                             'hltSingleCaloJet50',
                                             'hltSinglePFJet80',
                                             
                                             'hltL1sSingleJet90',
                                             'hltSingleCaloJet110',
                                             'hltSinglePFJet140',
                                             
                                             'hltL1sSingleJet120',
                                             'hltSingleCaloJet170',
                                             'hltSinglePFJet200',
                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltSingleCaloJet210',
                                             'hltSinglePFJet260',
                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltSingleCaloJet270',
                                             'hltSinglePFJet320',
                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltSingleCaloJet350',
                                             'hltSinglePFJet400',
                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltSingleCaloJet400',
                                             'hltSinglePFJet450',
                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltSingleCaloJet450',
                                             'hltSinglePFJet500',
                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltSingleCaloJet450',
                                             'hltSinglePFJet550',
                                             
                                             'hltL1sSingleMu3IorSingleMu5IorSingleMu7',
                                             'hltL1fL1sMu5L1Filtered0',
                                             'hltL3fL1sMu5L1f0L2f5L3Filtered8',
                                             
                                             'hltL1sSingleMu3',
                                             'hltL1sSingleMu3IorMu3Jet30er2p5',
                                             'hltL1fL1sMu3L1Filtered0',
                                             'hltL1sSingleJet35ObjectMap',
                                             'hltL3fL1sMu3L1f0L2f0L3Filtered3',
                                             'hltMu3PFJet40MuCleaned',
                                             
                                             'hltL1sZeroBias',
                                             
                                             'hltL1sZeroBias',
                                             'hltDiCaloJetAve30',
                                             'hltDiPFJetAve40',
                                             
                                             'hltL1sSingleJet60',
                                             'hltDiCaloJetAve60',
                                             'hltDiPFJetAve80',
                                             
                                             'hltL1sSingleJet120',
                                             'hltDiCaloJetAve170',
                                             'hltDiPFJetAve200',
                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltDiCaloJetAve270',
                                             'hltDiPFJetAve320',
                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltDiCaloJetAve450',
                                             'hltDiPFJetAve500', )
                            + cms.vstring  (                 
                                             'hltL1sSingleJet180',
                                             'hltAK8SingleCaloJet260',
                                             'hltAK8SinglePFJet360',
                                             'hltAK8SinglePFJetTrimModMass30',
                                             
                                             'hltL1sSingleJet180',
                                             'hltAK8SingleCaloJet280',
                                             'hltAK8SinglePFJet380',
                                             'hltAK8SinglePFJetTrimModMass30',
                                             
                                             'hltL1sSingleJet180',
                                             'hltAK8SingleCaloJet300',
                                             'hltAK8SinglePFJet400',
                                             'hltAK8SinglePFJetTrimModMass30',
                                             
                                             'hltL1sSingleJet180',
                                             'hltAK8SingleCaloJet320',
                                             'hltAK8SinglePFJet420',
                                             'hltAK8SinglePFJetTrimModMass30',
                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltAK8SingleCaloJet300',
                                             'hltSinglePFJet330AK8',
                                             'hltPFJetForBtagSelectorAK8',
                                             'hltBTagPFCSVp3Single',
                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltAK8SingleCaloJet300',
                                             'hltSinglePFJet330AK8',
                                             'hltPFJetForBtagSelectorAK8',
                                             'hltBTagPFCSVp4Single',
                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltSingleCaloJet270AK8',
                                             'hltSinglePFJet320AK8',
                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltSingleCaloJet350AK8',
                                             'hltSinglePFJet400AK8',
                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltSingleCaloJet400AK8',
                                             'hltSinglePFJet450AK8',
                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltSingleCaloJet450AK8',
                                             'hltSinglePFJet500AK8',
                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltSingleCaloJet500AK8',
                                             'hltSinglePFJet550AK8',
                                             
                                             'hltL1sSingleMu22or25',
                                             'hltL1fL1sMu22or25L1Filtered0',
                                             'hltL3fL1sMu22Or25L1f0L2f10QL3Filtered50Q',
                                             
                                             'hltL1sSingleMu22or25',
                                             'hltL1fL1sMu22or25L1Filtered0',
                                             'hltL3fL1sMu22Or25L1f0L2f10QL3Filtered55Q',
                                             
   ) ),
   TriggerObjectSplits         = cms.vstring  (
                                             'hltL1Mu12er2p3Jet40er2p3dRMax0p4DoubleJet40er2p3dEtaMax1p6',
                                             'hltL1sSingleMu3IorMu3Jet30er2p5',
   ),
   TriggerObjectSplitsTypes    = cms.vstring  (
                                             'l1muon:l1jet',
                                             'l1muon:l1jet',
   ),
)
