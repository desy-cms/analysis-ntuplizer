# To be used with the following installation
#
# git clone git@github.com:robervalwalsh/analysis-ntuplizer.git Analysis/Ntuplizer
# scram b -j4
#________________________________________________________________________________________________________________________________________________

from __future__ import print_function
import os
import sys

# Initialize the config file, get the command line options
python_config_name = os.path.basename(__file__)
cmssw_base = os.getenv("CMSSW_BASE")
## Get parameters from command line
from Analysis.Ntuplizer.utils.ntuplizer_parser import ntuplizer_parser
command_line_options = ntuplizer_parser()

# If the output file already exists, remove it so ROOT/TFileService can recreate it
# problems with files in EOS
if hasattr(command_line_options, 'outputFile') and command_line_options.outputFile:
    try:
        if os.path.exists(command_line_options.outputFile):
            os.remove(command_line_options.outputFile)
    except Exception as e:
        print('Warning: could not remove existing output file:', e)

# General CMS stuff
import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras
from Configuration.AlCa.GlobalTag import GlobalTag

## Let it begin
process = cms.Process('MssmHbb',eras.Run3_2024)
# # process options
process.options = cms.untracked.PSet()
process.options.numberOfThreads=cms.untracked.uint32(4) # execution with 4cores
process.options.numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(1)  # requirement for the nFilteredEvents counter to work properly

# general configurations
process.load('FWCore.MessageService.MessageLogger_cfi')
# process.MessageLogger.cerr.threshold = cms.untracked.string("WARNING")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(command_line_options.logReportEvery)
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag = GlobalTag(process.GlobalTag, command_line_options.globalTag)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(command_line_options.maxEvents) )

## TFileService - output file for the ntuple
process.TFileService = cms.Service('TFileService',
   fileName = cms.string(command_line_options.outputFile)
)

## Filter counter (maybe more useful for MC)
process.nTotalEvents    = cms.EDProducer('EventCountProducer')
process.nFilteredEvents = cms.EDProducer('EventCountProducer')

## Trigger information
from Analysis.Ntuplizer.utils.trigger_info import trigger_info_reader
trigger_info = trigger_info_reader(command_line_options.triggerInfo)

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

# Apply JES corrections
process.load('Analysis.Ntuplizer.jet_corrections_cff')

# from Analysis.Ntuplizer.btag_algorithms_cfi import BTagAlgorithms_AK4CHS

## Ntuplizer
process.MssmHbb     = cms.EDAnalyzer('Ntuplizer',
    # Imported settings (always at the beginning???)
    #BTagAlgorithms_AK4CHS,
    trigger_info['ntuplizerTriggerPaths'],
    trigger_info['ntuplizerL1Seeds'],
    trigger_info['ntuplizerTriggerObjects'],
    MonteCarlo      = cms.bool(command_line_options.type == 'mc'),
    ReadPrescale    = cms.bool(True),
    TotalEvents     = cms.InputTag ('nTotalEvents'),
    FilteredEvents  = cms.InputTag ('nFilteredEvents'),
    TriggerResults  = cms.VInputTag(
                                    cms.InputTag('TriggerResults','','HLT'), ),
    TriggerObjectStandAlone = cms.VInputTag(
                                    cms.InputTag('slimmedPatTrigger'), ),
    PatJets         = cms.VInputTag( 
                                    cms.InputTag('updatedPatJetsAK4Puppi'),
                                    cms.InputTag('slimmedJetsPuppi'),),
    JECRecords      = cms.vstring  (
                                    'AK4PFPuppi',
                                    'AK4PFPuppi',), # for the JEC uncertainties
    JERRecords      = cms.vstring  (
                                    'AK4PFPuppi',
                                    'AK4PFPuppi',), # for the JER uncertainties
    PatMuons        = cms.VInputTag(
                                    cms.InputTag('slimmedMuons'), ),
    PrimaryVertices = cms.VInputTag(
                                    cms.InputTag('offlineSlimmedPrimaryVertices'), ),
    L1TJets         = cms.VInputTag(
                                    cms.InputTag('caloStage2Digis','Jet','RECO'), ),
    L1TMuons        = cms.VInputTag(
                                    cms.InputTag('gmtStage2Digis','Muon','RECO'), ),
)

   ## MC only
if command_line_options.type == 'mc':
   process.MssmHbb.CrossSection        = cms.double(command_line_options.xsection)  # in pb
   process.MssmHbb.GenFilterInfo       = cms.InputTag("genFilterEfficiencyProducer")
   process.MssmHbb.GenRunInfo          = cms.InputTag("generator")
   process.MssmHbb.GenEventInfo        = cms.InputTag("generator")
   process.MssmHbb.GenJets             = cms.VInputTag(cms.InputTag("slimmedGenJets"))
   process.MssmHbb.GenParticles        = cms.VInputTag(cms.InputTag("prunedGenParticles"))
   process.MssmHbb.PileupSummaryInfo   = cms.InputTag("slimmedAddPileupInfo")


## !!! Do the stuff!
process.p = cms.Path(
                    process.nTotalEvents +
                    process.triggerSelection +
                    process.nFilteredEvents +
                    process.MssmHbb,
                    process.AK4PuppiJets,
                    process.AK4Jets,
                    process.AK8Jets
                )



# process.p = cms.Path(
#                      process.nTotalEvents +
#                      process.triggerSelection +
#                      process.nFilteredEvents,
#                      process.AK4Jets
#                     )


## Inputs
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()
processingMode=cms.untracked.string('RunsLumisAndEvents')
process.source = cms.Source ('PoolSource',fileNames = readFiles)
# process.source = cms.Source ('PoolSource',fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend(command_line_options.inputFiles)
secFiles.extend( [] )

## ! ============ JSON Certified data ===============   BE CAREFUL!!!
## !!! Don't use with CRAB!!!
#if command_line_options.json != '':
#   import FWCore.PythonUtilities.LumiList as LumiList
#   import FWCore.ParameterSet.Types as CfgTypes
#   process.source.lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange())
#   JSONfile = command_line_options.json
#   myLumis = LumiList.LumiList(filename = JSONfile).getCMSSWString().split(',')
#   process.source.lumisToProcess.extend(myLumis)

## ============ Output MiniAOD ======================
## !!! Produces a large file!
# process.out = cms.OutputModule("PoolOutputModule",
#                                fileName = cms.untracked.string('patTuple.root'),
#                                outputCommands = cms.untracked.vstring('keep *_*_*_MssmHbb' )
#                                )
# process.outpath = cms.EndPath(process.out)
