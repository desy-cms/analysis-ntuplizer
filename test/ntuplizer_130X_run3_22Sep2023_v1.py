# To be used with the following installation
#
# git clone git@github.com:robervalwalsh/analysis-ntuplizer.git Analysis/Ntuplizer
# scram b -j4
#________________________________________________________________________________________________________________________________________________

from __future__ import print_function
import os
import sys

import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras
from Configuration.AlCa.GlobalTag import GlobalTag

from Analysis.Ntuplizer.BTagAlgorithms_cfi import BTagAlgorithms_AK4CHS

from Analysis.Ntuplizer.utils.trigger_info import trigger_info_reader
from Analysis.Ntuplizer.utils.ntuplizer_parser import ntuplizer_parser

python_config_name = os.path.basename(__file__)
cmssw_base = os.getenv("CMSSW_BASE")

## Get options from command line
command_line_options = ntuplizer_parser()

## Let it begin
process = cms.Process('MssmHbb',eras.Run3_2023)

process.options = cms.untracked.PSet()
# execution with 4cores
process.options.numberOfThreads=cms.untracked.uint32(4)

# general configurations
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(command_line_options.logReportEvery)
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag = GlobalTag(process.GlobalTag, command_line_options.globalTag)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(command_line_options.maxEvents) )

## TFileService
process.TFileService = cms.Service('TFileService',
   fileName = cms.string(command_line_options.outputFile)
)

## Trigger information
trigger_info = trigger_info_reader(command_line_options.triggerInfo)

# Apply JES corrections
process.load('Analysis.Ntuplizer.JetCorrections_cff')

# # Retrieve b jet regression correction factors
# process.load('Analysis.Ntuplizer.BJetRegression_cff')

## Event extras
# process.load('Analysis.Ntuplizer.EventExtras_cff')

# Trigger filter: FOR DATA ONLY!!!
process.triggerSelection = cms.EDFilter( 'TriggerResultsFilter',
    trigger_info['triggerResultsFilter'],
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

## Ntuplizer
process.MssmHbb     = cms.EDAnalyzer('Ntuplizer',
    # Imported settings (always at the beginning???)
    BTagAlgorithms_AK4CHS,
    trigger_info['ntuplizerTriggerPaths'],
    trigger_info['ntuplizerL1Seeds'],
    trigger_info['ntuplizerTriggerObjects'],
    stageL1Trigger = cms.uint32(2),
    FixedGridRhoAll = cms.InputTag ('fixedGridRhoAll'),
    TriggerResults  = cms.VInputTag(cms.InputTag('TriggerResults','','HLT') ),
    TriggerObjectStandAlone = cms.VInputTag(cms.InputTag('slimmedPatTrigger'), ),
   #  TotalEvents     = cms.InputTag ('TotalEvents'),
   #  FilteredEvents  = cms.InputTag ('FilteredEvents'),
    PatJets         = cms.VInputTag( cms.InputTag('updatedPatJets'), ),
    JECRecords      = cms.vstring  (              'AK4PFchs', ), # for the JEC uncertainties
    JERRecords      = cms.vstring  (              'AK4PFchs', ), # for the JER uncertainties
    PatMuons        = cms.VInputTag(cms.InputTag('slimmedMuons') ),
    PrimaryVertices = cms.VInputTag(cms.InputTag('offlineSlimmedPrimaryVertices') ),
#    L1TJets         = cms.VInputTag(cms.InputTag('caloStage2Digis','Jet','RECO'), ),
#    L1TMuons        = cms.VInputTag(cms.InputTag('gmtStage2Digis','Muon','RECO'), ),
)

   ## MC only
if command_line_options.type == 'mc':
   process.MssmHbb.MonteCarlo      = cms.bool(True)
   process.MssmHbb.CrossSection    = cms.double(command_line_options.xsection)  # in pb
   process.MssmHbb.GenFilterInfo   = cms.InputTag("genFilterEfficiencyProducer")
   process.MssmHbb.GenRunInfo      = cms.InputTag("generator")
   process.MssmHbb.GenEventInfo    = cms.InputTag("generator")
   process.MssmHbb.GenJets         = cms.VInputTag(cms.InputTag("slimmedGenJets"))
   process.MssmHbb.GenParticles    = cms.VInputTag(cms.InputTag("prunedGenParticles"))
   process.MssmHbb.PileupInfo      = cms.InputTag("slimmedAddPileupInfo")
else:
   process.MssmHbb.MonteCarlo      = cms.bool(False)


#########

## Do the stuff!
# process.p = cms.Path(process.TotalEvents +
#                      process.triggerSelection +
#                      process.FilteredEvents +
#                      process.MssmHbb,
#                      process.BJetRegression,
#                      process.AK4Jets,
#                     )

# process.p = cms.Path(process.triggerSelection +
#                      process.MssmHbb,
#                      process.BJetRegression,
#                      process.AK4Jets,
#                     )

process.p = cms.Path(
                     # process.TotalEvents +
                     process.triggerSelection +
                     # process.FilteredEvents +
                     process.MssmHbb,
                     process.AK4Jets
                    )


## Inputs
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()
process.source = cms.Source ('PoolSource',fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend(command_line_options.inputFiles)
secFiles.extend( [] )


## ============ JSON Certified data ===============   BE CAREFUL!!!
## Don't use with CRAB!!!
if command_line_options.json != '':
   import FWCore.PythonUtilities.LumiList as LumiList
   import FWCore.ParameterSet.Types as CfgTypes
   process.source.lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange())
   JSONfile = command_line_options.json
   myLumis = LumiList.LumiList(filename = JSONfile).getCMSSWString().split(',')
   process.source.lumisToProcess.extend(myLumis)

# ## ============ Output MiniAOD ======================
# process.out = cms.OutputModule("PoolOutputModule",
#                                fileName = cms.untracked.string('patTuple.root'),
#                                outputCommands = cms.untracked.vstring('keep *' )
#                                )
# process.outpath = cms.EndPath(process.out)