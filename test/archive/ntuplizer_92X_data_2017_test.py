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
process.GlobalTag = GlobalTag(process.GlobalTag, '92X_dataRun2_Prompt_v8')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

output_file = 'ntuple.root'
## TFileService
process.TFileService = cms.Service('TFileService',
   fileName = cms.string(output_file)
)


## ============  THE NTUPLIZER!!!  ===============
process.MssmHbb     = cms.EDAnalyzer('Ntuplizer',
    MonteCarlo      = cms.bool(False),
    UseFullName     = cms.bool(False),
    ###################
    TriggerResults  = cms.VInputTag(cms.InputTag('TriggerResults','','HLT')),
    TriggerPaths    = cms.vstring  (
    ## I recommend using the version number explicitly to be able to compare 
    ## however for production one has to be careful that all versions are included.
    ## Thinking of a better solution...
# physics triggers
                                     'HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_p33_v', 
                                     'HLT_Mu12_DoublePFJets40MaxDeta1p6_DoubleCaloBTagCSV_p33_v',
                ),
    L1Seeds    = cms.vstring  (
                                     'L1_Mu12er2p3_Jet40er2p3_dR_Max0p4_DoubleJet40er2p3_dEta_Max1p6',
                                     'L1_DoubleJet100er2p3_dEta_Max1p6',
                                     'L1_DoubleJet112er2p3_dEta_Max1p6',
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

                ),
    TriggerObjectSplits    = cms.vstring  (
                                             'hltL1Mu12er2p3Jet40er2p3dRMax0p4DoubleJet40er2p3dEtaMax1p6',
                ),
    TriggerObjectSplitsTypes    = cms.vstring  (
                                             'l1muon:l1jet',
                ),
               
                
)

process.p = cms.Path(
          process.MssmHbb
            )


readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
process.source = cms.Source ('PoolSource',fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend( [
#   'root://cms-xrd-global.cern.ch//store/data/Run2017F/BTagCSV/MINIAOD/PromptReco-v1/000/305/112/00000/02368BFC-A6B4-E711-AC9A-02163E01A4CB.root',  # LS = [70,90]
   'root://cms-xrd-global.cern.ch//store/data/Run2017F/BTagCSV/MINIAOD/PromptReco-v1/000/305/112/00000/F4D1DB92-50B4-E711-A8D2-02163E012205.root',  # LS = [250,269]
] );


secFiles.extend( [
       ] )

## ============ JSON Certified data ===============   BE CAREFUL!!!
## Don't use with CRAB!!!
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Types as CfgTypes
process.source.lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange())
#JSONfile = 'json_305112_70to90.txt'
JSONfile = 'json_305112_250to269.txt'
myLumis = LumiList.LumiList(filename = JSONfile).getCMSSWString().split(',')
process.source.lumisToProcess.extend(myLumis)
