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

import os

import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras
from Configuration.Eras.Modifier_run2_jme_2017_cff import run2_jme_2017

## Let it begin
process = cms.Process('MssmHbb',eras.Run2_2017)

process.options = cms.untracked.PSet(
)

# execution with 4cores
process.options.numberOfThreads=cms.untracked.uint32(4)


process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100000)

process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_dataRun2_v33')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

## TFileService
output_file = 'ntuple_test2-v5.root'
process.TFileService = cms.Service('TFileService',
   fileName = cms.string(output_file)
)

## b tag algorithms
from Analysis.Ntuplizer.NtuplizerBTag_cfi import *

## Trigger information
from Analysis.Ntuplizer.TriggerInfo_cfi import *
triggerInfo = triggerInfo('trigger_info.json')

# Apply JES corrections
process.load('Analysis.Ntuplizer.JetCorrections_cff')

# Retrieve b jet regression correction factors
process.load('Analysis.Ntuplizer.BJetRegression_cff')

## Trigger filter: FOR DATA ONLY!!!
process.triggerSelection = cms.EDFilter( 'TriggerResultsFilter',
    triggerInfo['triggerResultsFilter'],
    hltResults = cms.InputTag( 'TriggerResults', '', 'HLT' ),
    l1tResults = cms.InputTag( '' ),
    l1tIgnoreMask = cms.bool( False ),
    l1techIgnorePrescales = cms.bool( False ),
    daqPartitions = cms.uint32( 1 ),
    throw = cms.bool( False )
)

## Filter counter (maybe more useful for MC)
process.TotalEvents    = cms.EDProducer('EventCountProducer')
process.FilteredEvents = cms.EDProducer('EventCountProducer')

## Primary vertex
process.primaryVertexFilter = cms.EDFilter('VertexSelector',
   src = cms.InputTag('offlineSlimmedPrimaryVertices'), # primary vertex collection name
   cut = cms.string('!isFake && ndof > 4 && abs(z) <= 24 && position.Rho <= 2'), # ndof>thr=4 corresponds to sum(track_weigths) > (thr+3)/2 = 3.5 so typically 4 good tracks
   filter = cms.bool(True),   # otherwise it won't filter the events, just produce an empty vertex collection.
)


## Ntuplizer
process.MssmHbb     = cms.EDAnalyzer('Ntuplizer',
    # Imported settings (always at the beginning)
    ntuplizerBTag,
    triggerInfo['ntuplizerTriggerPaths'],
    triggerInfo['ntuplizerL1Seeds'],
    triggerInfo['ntuplizerTriggerObjects'],

    MonteCarlo      = cms.bool(False),
    ###################
    TotalEvents     = cms.InputTag ('TotalEvents'),
    FilteredEvents  = cms.InputTag ('FilteredEvents'),
    PatJets         = cms.VInputTag( cms.InputTag('updatedJets'), ),
    JECRecords      = cms.vstring  (              'AK4PFchs', ), # for the JEC uncertainties
    JERRecords      = cms.vstring  (              'AK4PFchs', ), # for the JER uncertainties
    FixedGridRhoAll = cms.InputTag ('fixedGridRhoAll'),
    PatMuons        = cms.VInputTag(cms.InputTag('slimmedMuons') ),
    PrimaryVertices = cms.VInputTag(cms.InputTag('offlineSlimmedPrimaryVertices') ),
    TriggerResults  = cms.VInputTag(cms.InputTag('TriggerResults','','HLT') ),
    L1TJets         = cms.VInputTag(cms.InputTag('caloStage2Digis','Jet','RECO'), ),
    L1TMuons        = cms.VInputTag(cms.InputTag('gmtStage2Digis','Muon','RECO'), ),
    TriggerObjectStandAlone = cms.VInputTag(cms.InputTag('slimmedPatTrigger'), ),

)

## Do the stuff!
process.p = cms.Path(process.TotalEvents +
                     process.triggerSelection +
                     process.primaryVertexFilter +
                     process.FilteredEvents +
                     process.MssmHbb,
                     process.BJetRegression,
                     process.AK4Jets,
                    )

## Inputs
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()
process.source = cms.Source ('PoolSource',fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend( [

# 302663
'/store/data/Run2017D/BTagCSV/MINIAOD/UL2017_MiniAODv2-v1/270000/3A3DF494-008A-1D49-9A95-0D9E334783A2.root',
#'/store/data/Run2017D/BTagCSV/MINIAOD/UL2017_MiniAODv2-v1/270000/8D468225-570E-6946-B269-E4F496256B62.root',
#'/store/data/Run2017D/BTagCSV/MINIAOD/UL2017_MiniAODv2-v1/270000/AED0DB9D-D7D5-8846-8E16-6742202A0298.root',
#'/store/data/Run2017D/BTagCSV/MINIAOD/UL2017_MiniAODv2-v1/270000/F8EE18DA-4D95-C44C-87EE-B265360F78BB.root',
#'/store/data/Run2017D/BTagCSV/MINIAOD/UL2017_MiniAODv2-v1/270000/F9C56F58-979D-7049-9DFD-B60E80F9F28A.root',
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
# import FWCore.PythonUtilities.LumiList as LumiList
# import FWCore.ParameterSet.Types as CfgTypes
# process.source.lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange())
# JSONfile = 'json_302663_reference.txt'
# myLumis = LumiList.LumiList(filename = JSONfile).getCMSSWString().split(',')
# process.source.lumisToProcess.extend(myLumis)
