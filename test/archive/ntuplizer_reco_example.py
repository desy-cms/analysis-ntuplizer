# For the ntuple production
import FWCore.ParameterSet.Config as cms

process = cms.Process('Example')

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100000)

##  Using MINIAOD. GlobalTag just in case jet re-clustering, L1 trigger filter  etc is needed to be done
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '101X_dataRun2_Prompt_v9')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

## TFileService
output_file = 'ntuple.root'
process.TFileService = cms.Service('TFileService',
   fileName = cms.string(output_file)
)

## ============ TRIGGER FILTER =============== 
## Enable below at cms.Path if needed - DATA ONLY!!!
process.triggerSelection = cms.EDFilter( 'TriggerResultsFilter',
    triggerConditions = cms.vstring('HLT_ZeroBias_v*'),
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

## ============ PRIMARY VERTEX FILTER ===============   NEED TO MODIFY FOR RECO
# process.primaryVertexFilter = cms.EDFilter('VertexSelector',
#    src = cms.InputTag('offlinePrimaryVerticesWithBS'), # primary vertex collection name
#    cut = cms.string('!isFake && ndof > 4 && abs(z) <= 24 && position.Rho <= 2'), # ndof>thr=4 corresponds to sum(track_weigths) > (thr+3)/2 = 3.5 so typically 4 good tracks
#    filter = cms.bool(True),   # otherwise it won't filter the events, just produce an empty vertex collection.
# )
# 

## ============  THE NTUPLIZER!!!  ===============
process.RecoNtuple     = cms.EDAnalyzer('Ntuplizer',
    
    MonteCarlo             = cms.bool(False),
    ###################
    TotalEvents            = cms.InputTag ('TotalEvents'),
    FilteredEvents         = cms.InputTag ('FilteredEvents'),
#    PrimaryVertices        = cms.VInputTag(cms.InputTag('offlinePrimaryVerticesWithBS') ),
    RecoMuons              = cms.VInputTag(cms.InputTag('muons1Leg','','RECO') ), 
    RecoTracks             = cms.VInputTag(cms.InputTag('ALCARECOTkAlCosmicsCTF0T','','RECO') ), 
#    TriggerResults         = cms.VInputTag(cms.InputTag('TriggerResults','','HLT') ),
#    L1Seeds                = cms.vstring  ('L1_ZeroBias'),
#    TriggerPaths           = cms.vstring  ('HLT_ZeroBias_v'),
#    L1TMuons               = cms.VInputTag(cms.InputTag('gmtStage2Digis','Muon','RECO'), ),   # may not work with some ALCA dataset, collection not available
#    TriggerEvent           = cms.VInputTag(cms.InputTag('hltTriggerSummaryAOD','','HLT'), ),  # collection with trigger objects in RECO
#    TriggerObjectLabels    = cms.vstring  ('hltL1sZeroBias')                                  # list of trigger objects in RECO to be stored in ntuple

)

process.p = cms.Path(
          process.TotalEvents *
          process.triggerSelection *
          process.FilteredEvents *
          process.RecoNtuple
            )


readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
process.source = cms.Source ('PoolSource',fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend( [
#   '/store/data/Run2018A/ZeroBias/RAW-RECO/LogError-PromptReco-v2/000/316/239/00000/0012D71D-5159-E811-984D-FA163E94BBA0.root',
   '/store/mc/RunIISpring18CosmicDR/TKCosmics_38T/ALCARECO/TkAlCosmics0T-PEAK_100X_mc2017cosmics_realistic_peak_v3-v1/30000/7CF568B9-E433-E811-BA8F-02163E019F9F.root',
] );


secFiles.extend( [
       ] )

