import FWCore.ParameterSet.Config as cms

# if long list, use + cms.vstring or extend
# see https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideAboutPythonConfigFile#Modifying_Parameters
MssmHbbNtuplizerTriggerObjects = cms.PSet(
   TriggerObjectLabels    = ( cms.vstring  (  
# physics triggers
# HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTag*CSV_p*_v
                                             'hltL1DoubleJet112er2p3dEtaMax1p6',
                                             'hltDoubleCaloBJets100eta2p3',
                                             'hltBTagCaloDeepCSV0p71Double6Jets80',
                                             'hltDoublePFJets116Eta2p3',
                                             'hltDoublePFJets116Eta2p3MaxDeta1p6',
                                             # csvv2
                                             'hltL1DoubleJet112er2p3dEtaMax1p6',
                                             'hltDoubleCaloBJets100eta2p3',
                                             'hltBTagCalo80x6CSVp79DoubleWithMatching',
                                             'hltDoublePFJets116Eta2p3',
                                             'hltDoublePFJets116Eta2p3MaxDeta1p6',
# HLT_Mu12_DoublePFJets40MaxDeta1p6_DoubleCaloBTag*CSV_p*_v   
                                             'hltL1Mu12er2p3Jet40er2p3dRMax0p4DoubleJet40er2p3dEtaMax1p6',
                                             'hltL1fL1sMu12Dijet40L1Filtered0',
                                             'hltDoubleCaloBJets30eta2p3',
                                             'hltBTagCaloDeepCSV0p71Double8Jets30',
                                             'hltL3fL1sMu12Dijet40L1f0L2f8L3Filtered12',
                                             'hltDoublePFBJets40Eta2p3',
                                             'hltDoublePFJets40Eta2p3MaxDeta1p6',
                                             'hltBSoftMuonDiJet40Mu12L3FilterByDR',
                                             # csvv2
                                             'hltL1Mu12er2p3Jet40er2p3dRMax0p4DoubleJet40er2p3dEtaMax1p6',
                                             'hltL1fL1sMu12Dijet40L1Filtered0',
                                             'hltDoubleCaloBJets30eta2p3',
                                             'hltBTagCalo30x8CSVp0p87DoubleWithMatching',
                                             'hltL3fL1sMu12Dijet40L1f0L2f8L3Filtered12',
                                             'hltDoublePFBJets40Eta2p3',
                                             'hltDoublePFJets40Eta2p3MaxDeta1p6',
                                             'hltBSoftMuonDiJet40Mu12L3FilterByDR',
# backup triggers                                     
# HLT_DoublePFJets128MaxDeta1p6_DoubleCaloBTag*CSV_p*_v
                                             'hltL1DoubleJet112er2p3dEtaMax1p6',
                                             'hltDoubleCaloBJets100eta2p3',
                                             'hltBTagCaloDeepCSV0p71Double6Jets80',
                                             'hltDoublePFJets128Eta2p3',
                                             'hltDoublePFJets128Eta2p3MaxDeta1p6',
                                             # csvv2
                                             'hltL1DoubleJet112er2p3dEtaMax1p6',
                                             'hltDoubleCaloBJets100eta2p3',
                                             'hltBTagCalo80x6CSVp79DoubleWithMatching',
                                             'hltDoublePFJets128Eta2p3',
                                             'hltDoublePFJets128Eta2p3MaxDeta1p6',                                             
# HLT_Mu12_DoublePFJets54MaxDeta1p6_DoubleCaloBTag*CSV_p*_v
                                             'hltL1Mu12er2p3Jet40er2p3dRMax0p4DoubleJet40er2p3dEtaMax1p6',
                                             'hltL1fL1sMu12Dijet40L1Filtered0',
                                             'hltDoubleCaloBJets30eta2p3',
                                             'hltBTagCaloDeepCSV0p71Double8Jets30',
                                             'hltL3fL1sMu12Dijet40L1f0L2f8L3Filtered12',
                                             'hltDoublePFBJets54Eta2p3',
                                             'hltDoublePFJets54Eta2p3MaxDeta1p6',
                                             'hltBSoftMuonDiJet54Mu12L3FilterByDR',
                                             # csvv2
                                             'hltL1Mu12er2p3Jet40er2p3dRMax0p4DoubleJet40er2p3dEtaMax1p6',
                                             'hltL1fL1sMu12Dijet40L1Filtered0',
                                             'hltDoubleCaloBJets30eta2p3',
                                             'hltBTagCalo30x8CSVp0p87DoubleWithMatching',
                                             'hltL3fL1sMu12Dijet40L1f0L2f8L3Filtered12',
                                             'hltDoublePFBJets54Eta2p3',
                                             'hltDoublePFJets54Eta2p3MaxDeta1p6',
                                             'hltBSoftMuonDiJet54Mu12L3FilterByDR',
# HLT_Mu12_DoublePFJets62MaxDeta1p6_DoubleCaloBTag*CSV_p*_v
                                             'hltL1Mu12er2p3Jet40er2p3dRMax0p4DoubleJet40er2p3dEtaMax1p6',
                                             'hltL1fL1sMu12Dijet40L1Filtered0',
                                             'hltDoubleCaloBJets30eta2p3',
                                             'hltBTagCaloDeepCSV0p71Double8Jets30',
                                             'hltL3fL1sMu12Dijet40L1f0L2f8L3Filtered12',
                                             'hltDoublePFBJets62Eta2p3',
                                             'hltDoublePFJets62Eta2p3MaxDeta1p6',
                                             'hltBSoftMuonDiJet62Mu12L3FilterByDR',
                                             # csvv2
                                             'hltL1Mu12er2p3Jet40er2p3dRMax0p4DoubleJet40er2p3dEtaMax1p6',
                                             'hltL1fL1sMu12Dijet40L1Filtered0',
                                             'hltDoubleCaloBJets30eta2p3',
                                             'hltBTagCalo30x8CSVp0p87DoubleWithMatching',
                                             'hltL3fL1sMu12Dijet40L1f0L2f8L3Filtered12',
                                             'hltDoublePFBJets62Eta2p3',
                                             'hltDoublePFJets62Eta2p3MaxDeta1p6',
                                             'hltBSoftMuonDiJet62Mu12L3FilterByDR',
# additional triggers
# HLT_AK8PFJet360_TrimMass30_v
                                             'hltL1sSingleJet180',
                                             'hltAK8SingleCaloJet260',
                                             'hltAK8SinglePFJet360',
                                             'hltAK8SinglePFJetTrimModMass30',
# HLT_AK8PFJet380_TrimMass30_v                                             
                                             'hltL1sSingleJet180',
                                             'hltAK8SingleCaloJet280',
                                             'hltAK8SinglePFJet380',
                                             'hltAK8SinglePFJetTrimModMass30',
# HLT_AK8PFJet400_TrimMass30_v                                             
                                             'hltL1sSingleJet180',
                                             'hltAK8SingleCaloJet300',
                                             'hltAK8SinglePFJet400',
                                             'hltAK8SinglePFJetTrimModMass30',
# HLT_AK8PFJet420_TrimMass30_v                                             
                                             'hltL1sSingleJet180',
                                             'hltAK8SingleCaloJet320',
                                             'hltAK8SinglePFJet420',
                                             'hltAK8SinglePFJetTrimModMass30',
# HLT_AK8PFJet330_TrimMass30_PFAK8BTag*CSV_p17_v
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltAK8SingleCaloJet300',
                                             'hltSinglePFJet330AK8',
                                             'hltAK8SinglePFJetTrimModMass30',
                                             'hltPFJetForBtagSelectorAK8',
                                             'hltBTagAK8PFDeepCSV16p1Single',
                                             # csvv2
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltAK8SingleCaloJet300',
                                             'hltSinglePFJet330AK8',
                                             'hltAK8SinglePFJetTrimModMass30',
                                             'hltPFJetForBtagSelectorAK8',
                                             'hltBTagPFCSVp3Single',
# HLT_AK8PFJet330_TrimMass30_PFAK8BTag*CSV_p1_v
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltAK8SingleCaloJet300',
                                             'hltSinglePFJet330AK8',
                                             'hltAK8SinglePFJetTrimModMass30',
                                             'hltPFJetForBtagSelectorAK8',
                                             'hltBTagAK8PFDeepCSV10p3Single',
                                             # csvv2
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltAK8SingleCaloJet300',
                                             'hltSinglePFJet330AK8',
                                             'hltAK8SinglePFJetTrimModMass30',
                                             'hltPFJetForBtagSelectorAK8',
                                             'hltBTagPFCSVp4Single',
# HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_p02_v                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltAK8SingleCaloJet300',
                                             'hltSinglePFJet330AK8',
                                             'hltSinglePFJet330AK8ForDB',
                                             'hltPFJetForDBtagSelectorAK8',
                                             'hltBTagPFBoostedDoubleSecondaryVertexpZSingle',
# control triggers
### btag                                             
# HLT_SingleJet30_Mu12_SinglePFJet40_v                                             
                                             'hltL1sMu3JetC16dEtaMax0p4dPhiMax0p4',
                                             'hltL1fL1sMu3Jet16L1Filtered0',
                                             'hltSingleCaloBJets30eta2p3',
                                             'hltL3fL1sMu3Jet16L1f0L2f8L3Filtered12',
                                             'hltSinglePFBJets40Eta2p3',
                                             'hltBSoftMuonJet40Mu12L3FilterByDR',
# HLT_DoublePFJets40_CaloBTag*CSV_p*_v         
                                             'hltL1DoubleJet40er3p0',
                                             'hltDoubleCaloBJets30eta2p3',
                                             'hltBTagCaloDeepCSV0p71Single8Jets30',
                                             'hltDoublePFJets40Eta2p3',
                                             # csvv2
                                             'hltL1DoubleJet40er3p0',
                                             'hltDoubleCaloBJets30eta2p3',
                                             'hltBTagCalo30x8CSVp79SingleWithMatching',
                                             'hltDoublePFJets40Eta2p3',
# HLT_DoublePFJets100_CaloBTag*CSV_p*_v                        
                                             'hltL1DoubleJet100er3p0',
                                             'hltDoubleCaloBJets100eta2p3',
                                             'hltBTagCaloDeepCSV0p71Single6Jets80',
                                             'hltDoublePFJets100Eta2p3',
                                             # csvv2
                                             'hltL1DoubleJet100er3p0',
                                             'hltDoubleCaloBJets100eta2p3',
                                             'hltBTagCalo80x6CSVp79SingleWithMatching',
                                             'hltDoublePFJets100Eta2p3',                                            
# HLT_DoublePFJets200_CaloBTag*CSV_p*_v
                                             'hltL1DoubleJet120er3p0',
                                             'hltDoubleCaloBJets100eta2p3',
                                             'hltBTagCaloDeepCSV0p71Single6Jets80',
                                             'hltDoublePFJets200Eta2p3',
                                             # csvv2
                                             'hltL1DoubleJet120er3p0',
                                             'hltDoubleCaloBJets100eta2p3',
                                             'hltBTagCalo80x6CSVp79SingleWithMatching',
                                             'hltDoublePFJets200Eta2p3',
# HLT_DoublePFJets350_CaloBTag*CSV_p*_v     
                                             'hltL1DoubleJet120er3p0',
                                             'hltDoubleCaloBJets100eta2p3',
                                             'hltBTagCaloDeepCSV0p71Single6Jets80',
                                             'hltDoublePFJets350Eta2p3',
                                             # csvv2
                                             'hltL1DoubleJet120er3p0',
                                             'hltDoubleCaloBJets100eta2p3',
                                             'hltBTagCalo80x6CSVp79SingleWithMatching',
                                             'hltDoublePFJets350Eta2p3',
# HLT_Mu12_DoublePFJets40_CaloBTag*CSV_p*_v
                                             'hltL1sMu3JetC16dEtaMax0p4dPhiMax0p4',
                                             'hltL1fL1sMu3Jet16L1Filtered0',
                                             'hltDoubleCaloBJets30eta2p3',
                                             'hltBTagCaloDeepCSV0p71Single8Jets30',
                                             'hltL3fL1sMu3Jet16L1f0L2f8L3Filtered12',
                                             'hltDoublePFBJets40Eta2p3',
                                             'hltBSoftMuonDiJet40Mu12L3FilterByDR',
                                             # csvv2
                                             'hltL1sMu3JetC16dEtaMax0p4dPhiMax0p4',
                                             'hltL1fL1sMu3Jet16L1Filtered0',
                                             'hltDoubleCaloBJets30eta2p3',
                                             'hltBTagCalo30x8CSVp79SingleWithMatching',
                                             'hltL3fL1sMu3Jet16L1f0L2f8L3Filtered12',
                                             'hltDoublePFBJets40Eta2p3',
                                             'hltBSoftMuonDiJet40Mu12L3FilterByDR',
# HLT_Mu12_DoublePFJets100_CaloBTag*CSV_p*_v
                                             'hltL1sMu3JetC60dEtaMax0p4dPhiMax0p4',
                                             'hltL1fL1sMu3Jet60L1Filtered0',
                                             'hltDoubleCaloBJets30eta2p3',
                                             'hltBTagCaloDeepCSV0p71Single8Jets30',
                                             'hltL3fL1sMu3Jet60L1f0L2f8L3Filtered12',
                                             'hltDoublePFBJets100Eta2p3',
                                             'hltBSoftMuonDiJet100Mu12L3FilterByDR',
                                             # csvv2
                                             'hltL1sMu3JetC60dEtaMax0p4dPhiMax0p4',
                                             'hltL1fL1sMu3Jet60L1Filtered0',
                                             'hltDoubleCaloBJets30eta2p3',
                                             'hltBTagCalo30x8CSVp79SingleWithMatching',
                                             'hltL3fL1sMu3Jet60L1f0L2f8L3Filtered12',
                                             'hltDoublePFBJets100Eta2p3',
                                             'hltBSoftMuonDiJet100Mu12L3FilterByDR',
# HLT_Mu12_DoublePFJets200_CaloBTag*CSV_p*_v
                                             'hltL1sMu3JetC120dEtaMax0p4dPhiMax0p4',
                                             'hltL1fL1sMu3Jet120L1Filtered0',
                                             'hltDoubleCaloBJets30eta2p3',
                                             'hltBTagCaloDeepCSV0p71Single8Jets30',
                                             'hltL3fL1sMu3Jet120L1f0L2f8L3Filtered12',
                                             'hltDoublePFBJets200Eta2p3',
                                             'hltBSoftMuonDiJet200Mu12L3FilterByDR',
                                             # csvv2
                                             'hltL1sMu3JetC120dEtaMax0p4dPhiMax0p4',
                                             'hltL1fL1sMu3Jet120L1Filtered0',
                                             'hltDoubleCaloBJets30eta2p3',
                                             'hltBTagCalo30x8CSVp79SingleWithMatching',
                                             'hltL3fL1sMu3Jet120L1f0L2f8L3Filtered12',
                                             'hltDoublePFBJets200Eta2p3',
                                             'hltBSoftMuonDiJet200Mu12L3FilterByDR',
# HLT_Mu12_DoublePFJets350_CaloBTag*CSV_p*_v
                                             'hltL1sMu3JetC120dEtaMax0p4dPhiMax0p4',
                                             'hltL1fL1sMu3Jet120L1Filtered0',
                                             'hltDoubleCaloBJets30eta2p3',
                                             'hltBTagCaloDeepCSV0p71Single8Jets30',
                                             'hltL3fL1sMu3Jet120L1f0L2f8L3Filtered12',
                                             'hltDoublePFBJets350Eta2p3',
                                             'hltBSoftMuonDiJet350Mu12L3FilterByDR',
                                             # csvv2
                                             'hltL1sMu3JetC120dEtaMax0p4dPhiMax0p4',
                                             'hltL1fL1sMu3Jet120L1Filtered0',
                                             'hltDoubleCaloBJets30eta2p3',
                                             'hltBTagCalo30x8CSVp79SingleWithMatching',
                                             'hltL3fL1sMu3Jet120L1f0L2f8L3Filtered12',
                                             'hltDoublePFBJets350Eta2p3',
                                             'hltBSoftMuonDiJet350Mu12L3FilterByDR',
                                             
                                              )
                            + cms.vstring  (  
# jet triggers                                           
# HLT_PFJet40_v                                         
                                             'hltL1sZeroBias',
                                             'hltSingleCaloJet10',
                                             'hltSinglePFJet40',
# HLT_PFJet60_v                                             
                                             'hltL1sSingleJet35',
                                             'hltSingleCaloJet40',
                                             'hltSinglePFJet60',
# HLT_PFJet80_v                                             
                                             'hltL1sSingleJet60',
                                             'hltSingleCaloJet50',
                                             'hltSinglePFJet80',
# HLT_PFJet140_v                                             
                                             'hltL1sSingleJet90',
                                             'hltSingleCaloJet110',
                                             'hltSinglePFJet140',
# HLT_PFJet200_v                                             
                                             'hltL1sSingleJet120',
                                             'hltSingleCaloJet170',
                                             'hltSinglePFJet200',
# HLT_PFJet260_v                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltSingleCaloJet210',
                                             'hltSinglePFJet260',
# HLT_PFJet320_v                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltSingleCaloJet270',
                                             'hltSinglePFJet320',
# HLT_PFJet400_v                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltSingleCaloJet350',
                                             'hltSinglePFJet400',
# HLT_PFJet450_v                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltSingleCaloJet400',
                                             'hltSinglePFJet450',
# HLT_PFJet500_v                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltSingleCaloJet450',
                                             'hltSinglePFJet500',
# HLT_PFJet550_v                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltSingleCaloJet450',
                                             'hltSinglePFJet550',
# HLT_DiPFJetAve40_v                                             
                                             'hltL1sZeroBias',
                                             'hltDiCaloJetAve30',
                                             'hltDiPFJetAve40',
# HLT_DiPFJetAve60_v                                             
                                             'hltL1sZeroBias',
                                             'hltDiCaloJetAve45',
                                             'hltDiPFJetAve60',
# HLT_DiPFJetAve80_v                                             
                                             'hltL1sSingleJet60',
                                             'hltDiCaloJetAve60',
                                             'hltDiPFJetAve80',
# HLT_DiPFJetAve200_v                                             
                                             'hltL1sSingleJet120',
                                             'hltDiCaloJetAve170',
                                             'hltDiPFJetAve200',
# HLT_DiPFJetAve320_v                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltDiCaloJetAve270',
                                             'hltDiPFJetAve320',
# HLT_DiPFJetAve500_v                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltDiCaloJetAve450',
                                             'hltDiPFJetAve500',
# muon triggers
# HLT_Mu8_v                                            
                                             'hltL1sSingleMu3IorSingleMu5IorSingleMu7',
                                             'hltL1fL1sMu3or5or7L1Filtered0',
                                             'hltL3fL1sMu5L1f0L2f5L3Filtered8',
# HLT_Mu50_v                                             
                                             'hltL1sSingleMu22or25',
                                             'hltL1fL1sMu22or25L1Filtered0',
                                             'hltL3fL1sMu22Or25L1f0L2f10QL3Filtered50Q',
# HLT_Mu55_v                                             
                                             'hltL1sSingleMu22or25',
                                             'hltL1fL1sMu22or25L1Filtered0',
                                             'hltL3fL1sMu22Or25L1f0L2f10QL3Filtered55Q',
# HLT_Mu3_PFJet40_v                                             
                                             
                                             'hltL1sSingleMu3IorMu3Jet30er2p5',
                                             'hltL1fL1sMu3Jet30L1Filtered0',
                                             'hltL1sSingleJet35ObjectMap',
                                             'hltL3fL1sMu3L1f0L2f0L3Filtered3',
                                             'hltMu3PFJet40MuCleaned',
# zerobias trigger                                             
# HLT_ZeroBias_v                                             
                                             'hltL1sZeroBias',
# additional
# HLT_AK8PFJet320_v                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltSingleCaloJet270AK8',
                                             'hltSinglePFJet320AK8',
# HLT_AK8PFJet400_v                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltSingleCaloJet350AK8',
                                             'hltSinglePFJet400AK8',
# HLT_AK8PFJet450_v                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltSingleCaloJet400AK8',
                                             'hltSinglePFJet450AK8',
# HLT_AK8PFJet500_v                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltSingleCaloJet450AK8',
                                             'hltSinglePFJet500AK8',
# HLT_AK8PFJet550_v                                               
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltSingleCaloJet500AK8',
                                             'hltSinglePFJet550AK8',
                                             
   ) 
                            + cms.vstring  (  
# muon triggers
# HLT_Mu17_v                                            
                                             'hltL1sSingleMu10LowQ',
                                             'hltL1fL1sMu10lqL1Filtered0',
                                             'hltL3fL1sMu10lqL1f0L2f10L3Filtered17',
                                             #
                                             'hltL1sSingleMu10er1p5',
                                             #
                                             'hltL1sSingleMu15DQ',
                                             'hltL1fL1sMu15DQlqL1Filtered0',
                                             'hltL3fL1sMu15DQlqL1f0L2f10L3Filtered17',
# HLT_Mu19_v                                            
                                             'hltL1sSingleMu10LowQ',
                                             'hltL1fL1sMu10lqL1Filtered0',
                                             'hltL3fL1sMu10lqL1f0L2f10L3Filtered19',
                                             #
                                             'hltL1sSingleMu10er1p5',
                                             #
                                             'hltL1sSingleMu15DQ',
                                             'hltL1fL1sMu15DQlqL1Filtered0',
                                             'hltL3fL1sMu15DQlqL1f0L2f10L3Filtered19',
# HLT_Mu20_v                                            
                                             'hltL1sSingleMu18',
                                             'hltL1fL1sMu18L1Filtered0',
                                             'hltL3fL1sMu18L1f0L2f10QL3Filtered20Q',
# HLT_Mu27_v                                            
                                             'hltL1sSingleMu22or25',
                                             'hltL1fL1sMu22or25L1Filtered0',
                                             'hltL3fL1sMu22Or25L1f0L2f10QL3Filtered27Q',
# jet triggers
# HLT_DiPFJetAve140_v                                             
                                             'hltL1sSingleJet90',
                                             'hltDiCaloJetAve110',
                                             'hltDiPFJetAve140',
# HLT_DiPFJetAve260_v                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltDiCaloJetAve210',
                                             'hltDiPFJetAve260',
# HLT_DiPFJetAve400_v                                             
                                             'hltL1sSingleJet170IorSingleJet180IorSingleJet200',
                                             'hltDiCaloJetAve350',
                                             'hltDiPFJetAve400',


                                             
   )
   ),
   TriggerObjectSplits         = cms.vstring  (
                                             'hltL1Mu12er2p3Jet40er2p3dRMax0p4DoubleJet40er2p3dEtaMax1p6',
                                             'hltL1sSingleMu3IorMu3Jet30er2p5',
                                             'hltL1sMu3JetC16dEtaMax0p4dPhiMax0p4',
                                             'hltL1sMu3JetC60dEtaMax0p4dPhiMax0p4',
                                             'hltL1sMu3JetC120dEtaMax0p4dPhiMax0p4',
   ),
   TriggerObjectSplitsTypes    = cms.vstring  (
                                             'l1muon:l1jet',
                                             'l1muon:l1jet',
                                             'l1muon:l1jet',
                                             'l1muon:l1jet',
                                             'l1muon:l1jet',
   ),
)
