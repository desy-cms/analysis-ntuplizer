import FWCore.ParameterSet.Config as cms

TFileService = cms.Service("TFileService",
	fileName = cms.string('ntuple.root')
)

## ============  THE NTUPLIZER!!!  ===============
ntuplizer           = cms.EDAnalyzer("Ntuplizer",
    MonteCarlo      = cms.bool(False),
    UseFullName     = cms.bool(False),
    ## Monte Carlo only
#     GenFilterInfo   = cms.InputTag("genFilterEfficiencyProducer"),
#     GenRunInfo      = cms.InputTag("generator"),
#     GenEventInfo    = cms.InputTag("generator"),
#     PileupInfo      = cms.InputTag("addPileupInfo","","HLT"),
    ###################
    TriggerResults  = cms.VInputTag(cms.InputTag('TriggerResults','','HLT2')),
    TriggerPaths    = cms.vstring  (
                                  'HLT_ZeroBias_v',
                                  'HLT_Mu8_v',
                                  'HLT_PFJet60_v',
                                  'HLT_DiPFJetAve60_v',
                                  'HLT_BTagMu_DiJet20_Mu5_v',
                                  'HLT_DoubleJetsC100_DoubleBTagCSV_p026_DoublePFJetsC160_v',
                                  'HLT_DoubleJetsC100_DoubleBTagCSV_p014_DoublePFJetsC100MaxDeta1p6_v',
                                  'HLT_Mu_CaloJets_CaloBTagCSV_PFJets_v',
               ),
    TriggerEvent  = cms.VInputTag(
                     cms.InputTag("hltTriggerSummaryAOD","","HLT2"),
                     ),
    TriggerObjectLabels    = cms.vstring  (
                                  'hltL1sZeroBias',
                                  'hltL1sSingleMu3IorSingleMu5IorSingleMu7',
                                  'hltL1fL1sMu5L1Filtered0',
                                  'hltL2fL1sMu5L1f0L2Filtered5',
                                  'hltL3fL1sMu5L1f0L2f5L3Filtered8',
                                  'hltL1sSingleJet35',
                                  'hltSingleCaloJet40',
                                  'hltSinglePFJet60',
                                  'hltL1sZeroBias',
                                  'hltDiCaloJetAve45',
                                  'hltDiPFJetAve60',
                                  'hltL1sMu3JetC16dEtaMax0p4dPhiMax0p4',
                                  'hltBDiJet20L1FastJetCentral',
                                  'hltBSoftMuonDiJet20L1FastJetL25FilterByDR',
                                  'hltBSoftMuonDiJet20L1FastJetMu5L3FilterByDR',
                                  'hltL1sDoubleJetC100',
                                  'hltDoubleJetsC100',
                                  'hltBTagCaloCSVp026DoubleWithMatching',
                                  'hltDoublePFJetsC160',
                                  'hltL1sDoubleJetC100',
                                  'hltDoubleJetsC100',
                                  'hltBTagCaloCSVp014DoubleWithMatching',
                                  'hltDoublePFJetsC100',
                                  'hltDoublePFJetsC100MaxDeta1p6',
               ),
)
