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
### other triggers                                     
                                     'HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0_v',
                                     'HLT_PFHT300PT30_QuadPFJet_75_60_45_40_v',

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
                                     'L1_HTT250er_QuadJet_70_55_40_35_er2p5',
                                     'L1_HTT280er_QuadJet_70_55_40_35_er2p5',
                                     'L1_HTT300er_QuadJet_70_55_40_35_er2p5',
                                     'L1_HTT320er_QuadJet_70_55_40_40_er2p4',
                                     'L1_HTT320er_QuadJet_70_55_40_40_er2p5',
                                     'L1_HTT340er_QuadJet_70_55_40_40_er2p5',
                                     'L1_QuadJet60er3p0',
                                     'L1_QuadJet50er3p0',
                                     'L1_HTT280er',
                                     'L1_HTT300er',
                                     'L1_HTT320er',
                                     'L1_HTT340er',
                                     'L1_HTT380er',
                                     'L1_HTT400er',
                                     'L1_HTT450er',
                                     'L1_HTT500er',

                                     
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
