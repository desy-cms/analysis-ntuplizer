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

from __future__ import print_function
import os
import sys

import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

from Configuration.StandardSequences.Eras import eras
from Configuration.Eras.Modifier_run2_jme_2017_cff import run2_jme_2017
from Configuration.AlCa.GlobalTag import GlobalTag
from Analysis.Ntuplizer.NtuplizerBTag_cfi import *
from Analysis.Ntuplizer.TriggerInfo_cfi import *

config_name = os.path.basename(sys.argv[1])

# command line options parsing
options = VarParsing.VarParsing()

options.register('maxEvents',
                 100,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "maximum number of events")

options.register('globalTag',
                 '',
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "condition global tag for the job (\"auto:run2_data\" is default)")
                 
options.register('year',
                 2017,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "year of data taking")

options.register('type',
                 'data',
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "data or mc")

options.register('xsection',
                 -1.,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.float,
                 "MC cross section")

options.register('triggerInfo',
                 '',
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Trigger info")

options.register('outputFile',
                 "ntuple.root",
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "name for the output root file (\"ntuple.root\" is default)")

options.register('inputFiles',
                 '',
                 VarParsing.VarParsing.multiplicity.list,
                 VarParsing.VarParsing.varType.string,
                 "files to process")

options.register('json',
                 '',
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "JSON file (do not use with CRAB!)")

options.parseArguments()

# default inputFiles (examples)
input_files = {}
input_files['data']= {}
input_files['data'][2017]='/store/data/Run2017D/BTagCSV/MINIAOD/UL2017_MiniAODv2-v1/270000/3A3DF494-008A-1D49-9A95-0D9E334783A2.root'
input_files['data'][2018]='/store/data/Run2018D/JetHT/MINIAOD/UL2018_MiniAODv2-v1/270000/0DEEC71E-980C-F945-8DB6-7CC0CFE862E2.root'
input_files['mc']= {}
input_files['mc'][2017]='/store/mc/RunIISummer20UL17MiniAOD/SUSYGluGluToBBHToBB_M-450_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/270000/8B35023B-84E7-4D41-9DD8-613FE001C07C.root'
input_files['mc'][2018]='/store/mc/RunIISummer20UL18MiniAODv2/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/100000/01F9363E-5BB5-534B-AF6A-B771B601FFA3.root'

# default triggerInfo
trigger_info = {}
trigger_info[2017]='/afs/desy.de/user/w/walsh/cms/ntuplizer/run2_ul/CMSSW_10_6_20/src/Analysis/Ntuplizer/data/ntuples/2017/v5/trigger_info.yml'
trigger_info[2018]='/afs/desy.de/user/w/walsh/cms/ntuplizer/run2_ul/CMSSW_10_6_20/src/Analysis/Ntuplizer/data/ntuples/2017/v5/trigger_info.yml'


# default globaTag
global_tag = {}
global_tag['data'] = {2017:'106X_dataRun2_v33'        , 2018:'106X_dataRun2_v33'}
global_tag['mc']   = {2017:'106X_mc2017_realistic_v9' , 2018:'106X_upgrade2018_realistic_v16_L1v1'}

# set defaults
if not options.inputFiles:
   options.setDefault('inputFiles',input_files[options.type][options.year])
if not options.globalTag:
   options.setDefault('globalTag',global_tag[options.type][options.year])
if not options.triggerInfo:
   options.setDefault('triggerInfo',trigger_info[options.year])

##
print('Python Configuration Options')
print('----------------------------')
print("globalTag         : ", options.globalTag)
print("maxEvents         : ", options.maxEvents)
print("year              : ", options.year)
print("type              : ", options.type)
if options.type == 'mc':
   print("xsection          : ", options.xsection)
print("inputFiles        : ", options.inputFiles)
print("outputFile        : ", options.outputFile)
print("triggerInfo       : ", options.triggerInfo)
if options.json:
   print("json              : ", options.json)
print('----------------------------')
print

## Let it begin
if options.year == 2017:
   process = cms.Process('MssmHbb',eras.Run2_2017)
else:
   process = cms.Process('MssmHbb')

process.options = cms.untracked.PSet()

# general configurations
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100000)
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag = GlobalTag(process.GlobalTag, options.globalTag)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

# execution with 4cores
process.options.numberOfThreads=cms.untracked.uint32(4)

## TFileService
process.TFileService = cms.Service('TFileService',
   fileName = cms.string(options.outputFile)
)

## Trigger information
triggerInfo = triggerInfo(options.triggerInfo)

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
                     process.FilteredEvents +
                     process.MssmHbb,
                     process.BJetRegression,
                     process.AK4Jets,
                    )

## Inputs
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()
process.source = cms.Source ('PoolSource',fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend(options.inputFiles)
secFiles.extend( [] )


## ============ JSON Certified data ===============   BE CAREFUL!!!
## Don't use with CRAB!!!
if options.json != '':
   import FWCore.PythonUtilities.LumiList as LumiList
   import FWCore.ParameterSet.Types as CfgTypes
   process.source.lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange())
   JSONfile = options.json
   myLumis = LumiList.LumiList(filename = JSONfile).getCMSSWString().split(',')
   process.source.lumisToProcess.extend(myLumis)
