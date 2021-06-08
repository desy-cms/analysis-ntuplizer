# To be used with the following installation
#
# cmsrel CMSSW_10_6_20
# cd CMSSW_10_6_20/src
# cmsenv
#
#
# git clone git@github.com:robervalwalsh/analysis-ntuplizer.git Analysis/Ntuplizer
# scram b -j4
#________________________________________________________________________________________________________________________________________________


# For the ntuple production
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

#process = cms.Process('MssmHbb',eras.Run2_2017,eras.run2_nanoAOD_94XMiniAODv2)
# lack reference -PPD twiki???
#process = cms.Process('MssmHbb',eras.Run2_2017,eras.run2_nanoAOD_94XMiniAODv2,eras.run2_miniAOD_94XFall17)

############# FIX ME?
process = cms.Process('MssmHbb')

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100000)

##  Using MINIAOD. GlobalTag just in case jet re-clustering, L1 trigger filter  etc is needed to be done
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_dataRun2_v33')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

## TFileService
output_file = 'ntuple.root'
process.TFileService = cms.Service('TFileService',
   fileName = cms.string(output_file)
)

### ==== Analysis imports ==== ###
from PhysicsTools.PatAlgos.tools.jetTools import *
from Analysis.Ntuplizer.run2017.v4.MssmHbbTriggerResultsFilter_cfi import *
from Analysis.Ntuplizer.run2017.v4.MssmHbbNtuplizerTriggerPaths_cfi import *
from Analysis.Ntuplizer.run2017.v4.MssmHbbNtuplizerL1Seeds_cfi import *
from Analysis.Ntuplizer.run2017.v4.MssmHbbNtuplizerTriggerObjects_cfi import *
from Analysis.Ntuplizer.run2017.v4.MssmHbbNtuplizerBtag_cfi import *
process.load('Analysis.Ntuplizer.run2017.v4.BJetRegression_cff')

### ==== btagging ==== ###
# only needed if discriminator is new or recommended not for JEC
bTagDiscriminators = [
    'pfDeepFlavourJetTags:probb',
    'pfDeepFlavourJetTags:probbb',
    'pfDeepFlavourJetTags:problepb',
    'pfDeepFlavourJetTags:probc',
    'pfDeepFlavourJetTags:probuds',
    'pfDeepFlavourJetTags:probg'
]

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

### ============ Jet energy correctiosn update ============== (not really running!???)
## Update the slimmedJets in miniAOD: corrections from the chosen Global Tag are applied
updateJetCollection(
    process,
    labelName = '',
#    jetSource = cms.InputTag('slimmedJets'),
    jetSource = cms.InputTag('slimmedJetsWithUserDataWithReg'),
    pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
    svSource = cms.InputTag('slimmedSecondaryVertices'),
    jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']), 'None'),
)
process.AK4Jets = cms.Task()
process.AK4Jets.add(process.patJetCorrFactors)
process.AK4Jets.add(process.updatedPatJets)


### ============ Jet energy correctiosn update ==============
## Update the slimmedJetsPuppi in miniAOD: corrections from the chosen Global Tag are applied
updateJetCollection(
    process,
    labelName = 'Puppi',
    jetSource = cms.InputTag('slimmedJetsPuppi'),
    pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
    svSource = cms.InputTag('slimmedSecondaryVertices'),
    jetCorrections = ('AK4PFPuppi', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']), 'None'),
)
process.AK4PuppiJets = cms.Task()
process.AK4PuppiJets.add(process.patJetCorrFactorsPuppi)
process.AK4PuppiJets.add(process.updatedPatJetsPuppi)


### ============ Jet energy correctiosn update ==============
## Update the slimmedJetsAK8 in miniAOD: corrections from the chosen Global Tag are applied
updateJetCollection(
    process,
    labelName = 'AK8',
    jetSource = cms.InputTag('slimmedJetsAK8'),
    jetCorrections = ('AK8PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']), 'None'),
)
process.AK8Jets = cms.Task()
process.AK8Jets.add(process.patJetCorrFactorsAK8)
process.AK8Jets.add(process.updatedPatJetsAK8)


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
#     PatJets         = cms.VInputTag( cms.InputTag('updatedPatJets'), ),
#     JECRecords      = cms.vstring  (              'AK4PFchs', ), # for the JEC uncertainties
#     JERRecords      = cms.vstring  (              'AK4PFchs', ), # for the JER uncertainties
    FixedGridRhoAll = cms.InputTag ('fixedGridRhoAll'),
    PatMuons        = cms.VInputTag(cms.InputTag('slimmedMuons') ),
    PrimaryVertices = cms.VInputTag(cms.InputTag('offlineSlimmedPrimaryVertices') ),
    TriggerResults  = cms.VInputTag(cms.InputTag('TriggerResults','','HLT') ),
    L1TJets         = cms.VInputTag(cms.InputTag('caloStage2Digis','Jet','RECO'), ),
    L1TMuons        = cms.VInputTag(cms.InputTag('gmtStage2Digis','Muon','RECO'), ),
    TriggerObjectStandAlone = cms.VInputTag(cms.InputTag('slimmedPatTrigger'), ),

)


#process.p1 = cms.Path(process.task)

process.p = cms.Path(process.TotalEvents +
                     process.triggerSelection +
                     process.primaryVertexFilter +
                     process.FilteredEvents +
                     process.MssmHbb,
                     process.BJetRegression,
                     process.AK4Jets,
                     process.AK4PuppiJets,
                     process.AK8Jets,
                    )

readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()
process.source = cms.Source ('PoolSource',fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend( [
#   '/store/data/Run2017F/BTagCSV/MINIAOD/17Nov2017-v1/00000/0202DCDF-4CFF-E711-8269-141877642F9D.root',
#   '/store/data/Run2017F/BTagCSV/MINIAOD/31Mar2018-v1/30000/78B5C4F9-3837-E811-A7DA-0025901D08B0.root'
#   '/store/data/Run2017D/BTagCSV/MINIAOD/UL2017_MiniAODv2-v1/270000/02CB91E3-67DD-D141-8CA5-23631C9DD58F.root',
# 302663
'/store/data/Run2017D/BTagCSV/MINIAOD/UL2017_MiniAODv2-v1/270000/3A3DF494-008A-1D49-9A95-0D9E334783A2.root',
'/store/data/Run2017D/BTagCSV/MINIAOD/UL2017_MiniAODv2-v1/270000/8D468225-570E-6946-B269-E4F496256B62.root',
'/store/data/Run2017D/BTagCSV/MINIAOD/UL2017_MiniAODv2-v1/270000/AED0DB9D-D7D5-8846-8E16-6742202A0298.root',
'/store/data/Run2017D/BTagCSV/MINIAOD/UL2017_MiniAODv2-v1/270000/F8EE18DA-4D95-C44C-87EE-B265360F78BB.root',
'/store/data/Run2017D/BTagCSV/MINIAOD/UL2017_MiniAODv2-v1/270000/F9C56F58-979D-7049-9DFD-B60E80F9F28A.root',
] );


secFiles.extend( [
       ] )

# ============ Output MiniAOD ======================
# process.out = cms.OutputModule("PoolOutputModule",
#                                fileName = cms.untracked.string('patTuple.root'),
#                                outputCommands = cms.untracked.vstring('keep *' )
#                                )
# process.outpath = cms.EndPath(process.out)
#
## ============ JSON Certified data ===============   BE CAREFUL!!!
## Don't use with CRAB!!!
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Types as CfgTypes
process.source.lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange())
JSONfile = 'json_302663_reference.txt'
myLumis = LumiList.LumiList(filename = JSONfile).getCMSSWString().split(',')
process.source.lumisToProcess.extend(myLumis)
