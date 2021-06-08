# For the ntuple production of prompt reco era Hv2

import FWCore.ParameterSet.Config as cms

process = cms.Process('MssmHbb')

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100000)

##  Using MINIAOD. GlobalTag just in case jet re-clustering, L1 trigger filter  etc is needed to be done
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '92X_dataRun2_Prompt_v10')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

output_file = 'ntuple.root'
## TFileService
process.TFileService = cms.Service('TFileService',
   fileName = cms.string(output_file)
)

## ============ TRIGGER FILTER =============== 
## Enable below at cms.Path if needed - DATA ONLY!!!
process.triggerSelection = cms.EDFilter( 'TriggerResultsFilter',
    triggerConditions = cms.vstring(
# physics triggers
                                     'HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_p33_v*', 
                                     'HLT_Mu12_DoublePFJets40MaxDeta1p6_DoubleCaloBTagCSV_p33_v*',
# backup triggers                                     
                                     'HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTagCSV_p33_v*', 
                                     'HLT_DoublePFJets128MaxDeta1p6_DoubleCaloBTagCSV_p33_v*', 
                                     'HLT_Mu12_DoublePFJets54MaxDeta1p6_DoubleCaloBTagCSV_p33_v*', 
                                     'HLT_Mu12_DoublePFJets62MaxDeta1p6_DoubleCaloBTagCSV_p33_v*',
# control triggers
### btag                             
                                     'HLT_SingleJet30_Mu12_SinglePFJet40_v*', 
                                     'HLT_DoublePFJets40_CaloBTagCSV_p33_v*', 
                                     'HLT_DoublePFJets100_CaloBTagCSV_p33_v*', 
                                     'HLT_DoublePFJets200_CaloBTagCSV_p33_v*', 
                                     'HLT_DoublePFJets350_CaloBTagCSV_p33_v*', 
                                     'HLT_Mu12_DoublePFJets40_CaloBTagCSV_p33_v*', 
                                     'HLT_Mu12_DoublePFJets100_CaloBTagCSV_p33_v*', 
                                     'HLT_Mu12_DoublePFJets200_CaloBTagCSV_p33_v*', 
                                     'HLT_Mu12_DoublePFJets350_CaloBTagCSV_p33_v*', 
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

### muon triggers
                                     'HLT_Mu8_v*', 
                                     'HLT_Mu3_PFJet40_v*', 
    ),
    hltResults = cms.InputTag( 'TriggerResults', '', 'HLT' ),
    l1tResults = cms.InputTag( '' ),
    l1tIgnoreMask = cms.bool( False ),
    l1techIgnorePrescales = cms.bool( False ),
    daqPartitions = cms.uint32( 1 ),
    throw = cms.bool( False )
)



## ============ EVENT FILTER COUNTER ===============
## Filter counter (maybe more useful for MC)
process.TotalEvents    = cms.EDProducer('EventCountProducer')
process.FilteredEvents = cms.EDProducer('EventCountProducer')

## ============ PRIMARY VERTEX FILTER ===============
process.primaryVertexFilter = cms.EDFilter('VertexSelector',
   src = cms.InputTag('offlineSlimmedPrimaryVertices'), # primary vertex collection name
   cut = cms.string('!isFake && ndof > 4 && abs(z) <= 24 && position.Rho <= 2'), # ndof>thr=4 corresponds to sum(track_weigths) > (thr+3)/2 = 3.5 so typically 4 good tracks
   filter = cms.bool(True),   # otherwise it won't filter the events, just produce an empty vertex collection.
)

## ============  THE NTUPLIZER!!!  ===============
process.MssmHbb     = cms.EDAnalyzer('Ntuplizer',
    MonteCarlo      = cms.bool(False),
    UseFullName     = cms.bool(False),
    ###################
    TotalEvents     = cms.InputTag('TotalEvents'),
    FilteredEvents  = cms.InputTag('FilteredEvents'),
    PatJets     = cms.VInputTag(  
                cms.InputTag('slimmedJets'),
                cms.InputTag('slimmedJetsPuppi'),
                ), 
    JECRecords      = cms.vstring  (           # for the JEC uncertainties
                'AK4PFchs',
                'AK4PFPuppi',
                ),
    JERRecords      = cms.vstring  (           # for the JER
                'AK4PFchs',
                'AK4PFPuppi',
                ),
    FixedGridRhoAll = cms.InputTag('fixedGridRhoAll'),
    PatMuons    = cms.VInputTag(
                cms.InputTag('slimmedMuons')
                ), 
    PrimaryVertices = cms.VInputTag(
                cms.InputTag('offlineSlimmedPrimaryVertices')
                ), 
    BTagAlgorithms = cms.vstring   (
                'pfCombinedInclusiveSecondaryVertexV2BJetTags',
                'pfJetProbabilityBJetTags',
                'pfCombinedMVAV2BJetTags',
                'pfDeepCSVJetTags:probudsg',
                'pfDeepCSVJetTags:probb',
                'pfDeepCSVJetTags:probc',
                'pfDeepCSVJetTags:probbb',
                'pfDeepCSVJetTags:probcc',
                'pfDeepCMVAJetTags:probudsg',
                'pfDeepCMVAJetTags:probb',
                'pfDeepCMVAJetTags:probc',
                'pfDeepCMVAJetTags:probbb',
                'pfDeepCMVAJetTags:probcc'    
               ),
    BTagAlgorithmsAlias = cms.vstring   (
                'btag_csvivf',
                'btag_jetprob',
                'btag_csvmva',
                'btag_deeplight',
                'btag_deepb',
                'btag_deepc',
                'btag_deepbb',
                'btag_deepcc',
                'btag_deepmvalight',
                'btag_deepmvab',
                'btag_deepmvac',
                'btag_deepmvabb',
                'btag_deepmvacc',
                    ),
    TriggerResults  = cms.VInputTag(cms.InputTag('TriggerResults','','HLT')),
    TriggerPaths    = cms.vstring  (
    ## I recommend using the version number explicitly to be able to compare 
    ## however for production one has to be careful that all versions are included.
    ## Thinking of a better solution...
# physics triggers
                                     'HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_p33_v', 
                                     'HLT_Mu12_DoublePFJets40MaxDeta1p6_DoubleCaloBTagCSV_p33_v',
# backup triggers                                     
                                     'HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTagCSV_p33_v', 
                                     'HLT_DoublePFJets128MaxDeta1p6_DoubleCaloBTagCSV_p33_v', 
                                     'HLT_Mu12_DoublePFJets54MaxDeta1p6_DoubleCaloBTagCSV_p33_v', 
                                     'HLT_Mu12_DoublePFJets62MaxDeta1p6_DoubleCaloBTagCSV_p33_v',
# control triggers
### btag                             
                                     'HLT_SingleJet30_Mu12_SinglePFJet40_v', 
                                     'HLT_DoublePFJets40_CaloBTagCSV_p33_v', 
                                     'HLT_DoublePFJets100_CaloBTagCSV_p33_v', 
                                     'HLT_DoublePFJets200_CaloBTagCSV_p33_v', 
                                     'HLT_DoublePFJets350_CaloBTagCSV_p33_v', 
                                     'HLT_Mu12_DoublePFJets40_CaloBTagCSV_p33_v', 
                                     'HLT_Mu12_DoublePFJets100_CaloBTagCSV_p33_v', 
                                     'HLT_Mu12_DoublePFJets200_CaloBTagCSV_p33_v', 
                                     'HLT_Mu12_DoublePFJets350_CaloBTagCSV_p33_v',
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

### muon triggers
                                     'HLT_Mu8_v', 
                                     'HLT_Mu3_PFJet40_v', 

                ),
    L1Seeds    = cms.vstring  (
                                     'L1_Mu3_JetC16_dEta_Max0p4_dPhi_Max0p4', 
                                     'L1_Mu3_JetC60_dEta_Max0p4_dPhi_Max0p4',
                                     'L1_Mu3_JetC120_dEta_Max0p4_dPhi_Max0p4',
                                     'L1_Mu12er2p3_Jet40er2p3_dR_Max0p4_DoubleJet40er2p3_dEta_Max1p6',
                                     'L1_DoubleJet40er3p0',
                                     'L1_DoubleJet100er3p0',
                                     'L1_DoubleJet112er3p0',
                                     'L1_DoubleJet120er3p0',
                                     'L1_DoubleJet100er2p3_dEta_Max1p6',
                                     'L1_DoubleJet112er2p3_dEta_Max1p6',
                                     'L1_ZeroBias',
                                     'L1_SingleJet35',
                                     'L1_SingleJet60',
                                     'L1_SingleJet90',
                                     'L1_SingleJet120',
                                     'L1_SingleJet170',
                                     'L1_SingleJet180',
                                     'L1_SingleJet200',
                                     'L1_SingleMu3',
                                     'L1_SingleMu5',
                                     'L1_SingleMu7',
                ),
    TriggerObjectStandAlone  = cms.VInputTag(
                     cms.InputTag('slimmedPatTrigger'),
                     ),
    TriggerObjectLabels    = cms.vstring  (

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
                                             'hltL1fL1sMu3L1Filtered0',
                                             'hltL1sSingleJet35ObjectMap',
                                             'hltL3fL1sMu3L1f0L2f0L3Filtered3',
                                             'hltMu3PFJet40MuCleaned',
                                             
                ),
    TriggerObjectSplits         = cms.vstring  (
                                             'hltL1Mu12er2p3Jet40er2p3dRMax0p4DoubleJet40er2p3dEtaMax1p6',
                ),
    TriggerObjectSplitsTypes    = cms.vstring  (
                                             'l1muon:l1jet',
                ),
)

process.p = cms.Path(
          process.TotalEvents *
          process.triggerSelection *
          process.primaryVertexFilter *
          process.FilteredEvents *
          process.MssmHbb
            )


readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
process.source = cms.Source ('PoolSource',fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend( [
   '/store/data/Run2017C/BTagCSV/MINIAOD/PromptReco-v1/000/299/368/00000/7ED71BDC-8D6D-E711-A6CE-02163E014491.root',
] );


secFiles.extend( [
       ] )

# ## ============ JSON Certified data ===============   BE CAREFUL!!!
# ## Don't use with CRAB!!!
# import FWCore.PythonUtilities.LumiList as LumiList
# import FWCore.ParameterSet.Types as CfgTypes
# process.source.lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange())
# JSONfile = 'json.txt'
# myLumis = LumiList.LumiList(filename = JSONfile).getCMSSWString().split(',')
# process.source.lumisToProcess.extend(myLumis)
