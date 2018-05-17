# For the ntuple production
import FWCore.ParameterSet.Config as cms

process = cms.Process('MssmHbb')

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100000)

##  Using MINIAOD. GlobalTag just in case jet re-clustering, L1 trigger filter  etc is needed to be done
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '101X_dataRun2_Prompt_v9')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

## TFileService
output_file = 'ntuple.root'
process.TFileService = cms.Service('TFileService',
   fileName = cms.string(output_file)
)

from Analysis.Ntuplizer.MssmHbbTriggerResultsFilter_cfi import *

## ============ TRIGGER FILTER =============== 
## Enable below at cms.Path if needed - DATA ONLY!!!
process.triggerSelection = cms.EDFilter( 'TriggerResultsFilter',
    MssmHbbTriggerResultsFilter,
    hltResults = cms.InputTag( 'TriggerResults', '', 'HLT' ),
    l1tResults = cms.InputTag( '' ),
    l1tIgnoreMask = cms.bool( False ),
    l1techIgnorePrescales = cms.bool( False ),
    daqPartitions = cms.uint32( 1 ),
    throw = cms.bool( False )
)


# only need if discriminator is new or recommended not for JEC
bTagDiscriminators = [
    'pfCombinedInclusiveSecondaryVertexV2BJetTags',
    'pfJetProbabilityBJetTags',
    'pfDeepCSVJetTags:probudsg',
    'pfDeepCSVJetTags:probb',
    'pfDeepCSVJetTags:probc',
    'pfDeepCSVJetTags:probbb',
    'pfDeepCSVJetTags:probcc',
]


### ============ Jet energy correctiosn update ============== (not really running!???)
from PhysicsTools.PatAlgos.tools.jetTools import *
## Update the slimmedJets in miniAOD: corrections from the chosen Global Tag are applied and the b-tag discriminators are re-evaluated
updateJetCollection(
    process,
    jetSource = cms.InputTag('slimmedJets'),
    jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']), 'None'),
#    btagDiscriminators = bTagDiscriminators
)
updateJetCollection(
    process,
    labelName = 'Puppi',
    jetSource = cms.InputTag('slimmedJetsPuppi'),
    jetCorrections = ('AK4PFPuppi', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']), 'None'),
#    btagDiscriminators = bTagDiscriminators
)
updateJetCollection(
    process,
    labelName = 'AK8',
    jetSource = cms.InputTag('slimmedJetsAK8'),
    jetCorrections = ('AK8PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']), 'None'),
#    btagDiscriminators = bTagDiscriminators    
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

from Analysis.Ntuplizer.MssmHbbNtuplizerTriggerPaths_cfi import *
from Analysis.Ntuplizer.MssmHbbNtuplizerL1Seeds_cfi import *
from Analysis.Ntuplizer.MssmHbbNtuplizerTriggerObjects_cfi import *
from Analysis.Ntuplizer.MssmHbbNtuplizerBtag_cfi import *


## ============  THE NTUPLIZER!!!  ===============
process.MssmHbb     = cms.EDAnalyzer('Ntuplizer',
    # Imported settings (always at the beginning)
    MssmHbbNtuplizerBtag,
    MssmHbbNtuplizerTriggerPaths,
    MssmHbbNtuplizerL1Seeds,
    MssmHbbNtuplizerTriggerObjects,
    
    MonteCarlo      = cms.bool(False),
    ###################
    TotalEvents     = cms.InputTag ('TotalEvents'),
    FilteredEvents  = cms.InputTag ('FilteredEvents'),
#    PatJets         = cms.VInputTag( cms.InputTag('slimmedJets'), cms.InputTag('slimmedJetsPuppi'), cms.InputTag('slimmedJetsAK8'), ),
    PatJets         = cms.VInputTag( cms.InputTag('updatedPatJets'), cms.InputTag('updatedPatJetsPuppi'), cms.InputTag('updatedPatJetsAK8'), ),
    JECRecords      = cms.vstring  (              'AK4PFchs',                     'AK4PFPuppi',                        'AK8PFchs', ), # for the JEC uncertainties
    JERRecords      = cms.vstring  (              'AK4PFchs',                     'AK4PFPuppi',                        'AK8PFchs', ), # for the JER uncertainties
    FixedGridRhoAll = cms.InputTag ('fixedGridRhoAll'),
    PatMuons        = cms.VInputTag(cms.InputTag('slimmedMuons') ), 
    PrimaryVertices = cms.VInputTag(cms.InputTag('offlineSlimmedPrimaryVertices') ),
    TriggerResults  = cms.VInputTag(cms.InputTag('TriggerResults','','HLT') ),
    L1TJets         = cms.VInputTag(cms.InputTag('caloStage2Digis','Jet','RECO'), ),
    L1TMuons        = cms.VInputTag(cms.InputTag('gmtStage2Digis','Muon','RECO'), ),
    TriggerObjectStandAlone = cms.VInputTag(cms.InputTag('slimmedPatTrigger'), ),

)

process.p = cms.Path(
          process.TotalEvents *
          process.triggerSelection *
          process.primaryVertexFilter *
          process.FilteredEvents *
          process.patJetCorrFactors * process.updatedPatJets *
          process.patJetCorrFactorsPuppi * process.updatedPatJetsPuppi *
          process.patJetCorrFactorsAK8 * process.updatedPatJetsAK8 *
          process.MssmHbb
            )


readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
process.source = cms.Source ('PoolSource',fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend( [
   '/store/data/Run2018A/JetHT/MINIAOD/PromptReco-v1/000/315/257/00000/684ACF2A-5F4B-E811-AC83-02163E01A002.root',
   '/store/data/Run2018A/JetHT/MINIAOD/PromptReco-v1/000/315/974/00000/DA0A327E-B255-E811-968E-FA163E0B2F4D.root',
] );


secFiles.extend( [
       ] )

# ============ Output MiniAOD ======================
# process.out = cms.OutputModule("PoolOutputModule",
#                                fileName = cms.untracked.string('patTuple.root'),
#                                outputCommands = cms.untracked.vstring('keep *' )
#                                )
# process.outpath = cms.EndPath(process.out)

# ## ============ JSON Certified data ===============   BE CAREFUL!!!
# ## Don't use with CRAB!!!
# import FWCore.PythonUtilities.LumiList as LumiList
# import FWCore.ParameterSet.Types as CfgTypes
# process.source.lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange())
# JSONfile = 'json_DCSONLY.txt'
# myLumis = LumiList.LumiList(filename = JSONfile).getCMSSWString().split(',')
# process.source.lumisToProcess.extend(myLumis)
