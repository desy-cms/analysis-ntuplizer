# To be used with the following installation
#
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVRun2LegacyAnalysis
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
from Analysis.Ntuplizer.Parser_cfi import parser

## Get options from command line
options = parser()


### Run2 Legacy specifics for cms.Process 
# need to find a better way to init cms.Process, outside this config
if options.year == 2017:
   process = cms.Process('MssmHbb',eras.Run2_2017)
else:
   process = cms.Process('MssmHbb')
###

## Inputs
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()
process.source = cms.Source ('PoolSource',fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend(options.inputFiles)
secFiles.extend( [] )

## process options
process.options = cms.untracked.PSet()
# execution with 4cores
process.options.numberOfThreads=cms.untracked.uint32(4)

## general configurations
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100000)
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag = GlobalTag(process.GlobalTag, options.globalTag)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )


## TFileService
process.TFileService = cms.Service('TFileService',
   fileName = cms.string(options.outputFile)
)

## Trigger information
triggerInfo = triggerInfo(options.triggerInfo)

## Apply JES corrections
process.load('Analysis.Ntuplizer.JetCorrections_cff')

## Retrieve b jet regression correction factors
process.load('Analysis.Ntuplizer.JetWithUserData_cff')

## Event extras
process.load('Analysis.Ntuplizer.EventExtras_cff')

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
    # Imported settings (always at the beginning???)
    ntuplizerBTag,
    triggerInfo['ntuplizerTriggerPaths'],
    triggerInfo['ntuplizerL1Seeds'],
    triggerInfo['ntuplizerTriggerObjects'],
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
    # this can also be done as VInputTag
    PrefiringWeight    =cms.InputTag('prefiringweight','nonPrefiringProb','MssmHbb'),
    PrefiringWeightUp  =cms.InputTag('prefiringweight','nonPrefiringProbUp','MssmHbb'),
    PrefiringWeightDown=cms.InputTag('prefiringweight','nonPrefiringProbDown','MssmHbb'),
)
process.MssmHbb.MonteCarlo      = cms.bool((options.type == 'mc'))

   ## MC only
if options.type == 'mc':
   process.MssmHbb.CrossSection    = cms.double(options.xsection)  # in pb
   process.MssmHbb.GenFilterInfo   = cms.InputTag("genFilterEfficiencyProducer")
   process.MssmHbb.GenRunInfo      = cms.InputTag("generator")
   process.MssmHbb.GenEventInfo    = cms.InputTag("generator")
   process.MssmHbb.GenJets         = cms.VInputTag(cms.InputTag("slimmedGenJets"))
   process.MssmHbb.GenParticles    = cms.VInputTag(cms.InputTag("prunedGenParticles"))
   process.MssmHbb.PileupInfo      = cms.InputTag("slimmedAddPileupInfo")



#########

## Do the stuff!
process.path_data = cms.Path(process.TotalEvents +
                     process.triggerSelection +
                     process.FilteredEvents +
                     process.MssmHbb,
                     process.EventExtras,
                     process.JetWithUserData,
                     process.AK4Jets,
                    )
process.path_mc   = cms.Path(process.TotalEvents +
                     process.FilteredEvents +
                     process.MssmHbb,
                     process.EventExtras,
                     process.JetWithUserData,
                     process.AK4Jets,
                    )

# 
# process.schedule = cms.Schedule(process.path_mc)
# if options.type == 'data':
#     process.schedule = cms.Schedule(process.path_data)

# ============ Output MiniAOD ======================
process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('patTuple.root'),
                               outputCommands = cms.untracked.vstring('keep *' )
                               )
process.outpath = cms.EndPath(process.out)

process.schedule = cms.Schedule(process.path_mc,process.outpath)
if options.type == 'data':
    process.schedule = cms.Schedule(process.path_data,process.outpath)



## ============ JSON Certified data ===============   BE CAREFUL!!!
## Don't use with CRAB!!!
if options.json != '':
   import FWCore.PythonUtilities.LumiList as LumiList
   import FWCore.ParameterSet.Types as CfgTypes
   process.source.lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange())
   JSONfile = options.json
   myLumis = LumiList.LumiList(filename = JSONfile).getCMSSWString().split(',')
   process.source.lumisToProcess.extend(myLumis)
