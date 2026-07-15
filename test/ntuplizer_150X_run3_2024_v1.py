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
            print('Removing existing output file:', command_line_options.outputFile)
            os.remove(command_line_options.outputFile)
    except Exception as e:
        print('Warning: could not remove existing output file:', e)


# General CMS stuff
import FWCore.ParameterSet.Config as cms
from Configuration.AlCa.GlobalTag import GlobalTag

# Modifiers
from Configuration.StandardSequences.Eras import eras
from Analysis.Ntuplizer.modifiers_per_year_cff import run2022, run2023, run2024, run2025, run2026
year_modifiers = {
    2022: run2022,
    2023: run2023,
    2024: run2024,
    2025: run2025,
    2026: run2026
}
year_modifier = year_modifiers.get(command_line_options.year)
modifiers = []
if year_modifier is not None:
    modifiers.append(year_modifier)

## Let it begin
process = cms.Process("MssmHbb", *modifiers)
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
TriggerInfo = trigger_info_reader(command_line_options.triggerInfo)
# Trigger filter: FOR DATA ONLY!!!
process.triggerSelection = cms.EDFilter( 'TriggerResultsFilter',
    triggerConditions = TriggerInfo['TriggerConditions'],
    hltResults = cms.InputTag( 'TriggerResults', '', 'HLT' ),
    l1tResults = cms.InputTag( '' ),
    l1tIgnoreMask = cms.bool( False ),
    l1techIgnorePrescales = cms.bool( False ),
    daqPartitions = cms.uint32( 1 ),
    throw = cms.bool( False )
)

# Apply JES corrections
process.load('Analysis.Ntuplizer.jet_corrections_cff')

# BTagging
from Analysis.Ntuplizer.btagging_cfi import BTagging, AllBTagging
BTagging_AK4PFPuppi = cms.VPSet(
    *BTagging['AK4PFPuppi']['ParticleNet'],
    *BTagging['AK4PFPuppi']['ParticleTransformer'],
    *BTagging['AK4PFPuppi']['UnifiedParticleTransformer'],
    *BTagging['AK4PFPuppi']['DeepFlavour']
)
BTagging_AK8PF = cms.VPSet(
    *BTagging['AK8PF']['ParticleNet'],
    *BTagging['AK8PF']['GlobalParticleTransformer'],
)

# BRegression
from Analysis.Ntuplizer.bregression_cfi import BRegression, AllBRegression


## Ntuplizer
process.MssmHbb                 = cms.EDAnalyzer('Ntuplizer',
    MonteCarlo                  = cms.bool(command_line_options.type == 'mc'),
    StorePrescale               = cms.bool(True),
    TotalEvents                 = cms.InputTag ('nTotalEvents'),
    FilteredEvents              = cms.InputTag ('nFilteredEvents'),
    TriggerResults              = cms.VInputTag(
                                                    cms.InputTag('TriggerResults','','HLT'), ),
    TriggerObjectStandAlone     = cms.VInputTag(
                                                    cms.InputTag('slimmedPatTrigger'), ),
    JetCollections              = cms.VPSet(
                                                cms.PSet(
                                                    collection    = cms.InputTag('updatedJetsPuppi'),
                                                    # original      = cms.InputTag('slimmedJetsPuppi'),
                                                    btagging      = BTagging_AK4PFPuppi,
                                                    bregression   = AllBRegression['AK4PFPuppi'],
                                                    pileupJetId   = cms.string('pileupJetIdPuppi:fullDiscriminant'),
                                                    jecRecord     = cms.string('AK4PFPuppi'),
                                                    jerRecord     = cms.string('AK4PFPuppi'),
                                                    ),
                                                cms.PSet(
                                                    collection    = cms.InputTag('updatedJetsAK8'),
                                                    # original      = cms.InputTag('slimmedJetsAK8'),
                                                    btagging      = BTagging['AK8PF']['ParticleNet'],
                                                    jecRecord     = cms.string('AK8PFPuppi'),
                                                    jerRecord     = cms.string('AK8PFPuppi'),
                                                    ),         
                                                ),
    PatMuons                    = cms.VInputTag(
                                                    cms.InputTag('slimmedMuons'),
                                                    ),
    PrimaryVertices             = cms.VInputTag(
                                                    cms.InputTag('offlineSlimmedPrimaryVertices'),
                                                    ),
    L1TJets                     = cms.VInputTag(
                                                    cms.InputTag('caloStage2Digis','Jet','RECO'),
                                                    ),
    L1TMuons                    = cms.VInputTag(
                                                    cms.InputTag('gmtStage2Digis','Muon','RECO'), 
                                                    ),
    TriggerPaths                = TriggerInfo['TriggerPaths'],
    L1Seeds                     = TriggerInfo['L1Seeds'],    
    TriggerObjectLabels         = TriggerInfo['TriggerObjectLabels'],
    TriggerObjectSplits         = TriggerInfo['TriggerObjectSplits'],
    TriggerObjectSplitsTypes    = TriggerInfo['TriggerObjectSplitsTypes'],
    MetFiltersResults           = cms.InputTag('TriggerResults', '', 'RECO'),
    FixedGridRhoAll             = cms.InputTag ('fixedGridRhoAll'),
)
# to modify according to year
run2022.toModify(process.MssmHbb, MetFiltersResults=cms.InputTag('TriggerResults', '', 'PAT'))
run2023.toModify(process.MssmHbb, MetFiltersResults=cms.InputTag('TriggerResults', '', 'PAT'))


## MC only
if command_line_options.type == 'mc':
   process.MssmHbb.CrossSection        = cms.double(command_line_options.xsection)  # in pb
   process.MssmHbb.PileupSummaryInfo   = cms.InputTag("slimmedAddPileupInfo")
   process.MssmHbb.GenFilterInfo       = cms.InputTag("genFilterEfficiencyProducer")
   process.MssmHbb.GenRunInfo          = cms.InputTag("generator")
   process.MssmHbb.GenEventInfo        = cms.InputTag("generator")
   process.MssmHbb.GenJets             = cms.VInputTag(
                                                        cms.InputTag("slimmedGenJets"),
                                                        cms.InputTag("slimmedGenJetsAK8"),
                                                        )
   process.MssmHbb.GenParticles        = cms.VInputTag(
                                                        cms.InputTag("prunedGenParticles"),
                                                        )

## !!! Do the stuff!
path = process.nTotalEvents
if command_line_options.type != 'mc':
    path += process.triggerSelection
path += ( process.nFilteredEvents +
            process.MssmHbb
)
process.p = cms.Path(path)
process.p.associate(process.jetPuppiTask)
process.p.associate(process.jetAK4Task)
process.p.associate(process.jetAK8Task)

## Inputs
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()
process.source = cms.Source ('PoolSource',fileNames = readFiles, secondaryFileNames = secFiles)
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
# output_pattuple = "patTuple.root"
# try:
#     if os.path.exists(output_pattuple):
#         print('Removing existing patTuple file:', output_pattuple)
#         os.remove(output_pattuple)
# except Exception as e:
#     print('Warning: could not remove existing patTuple file:', e)
# process.out = cms.OutputModule("PoolOutputModule",
#                                fileName = cms.untracked.string(output_pattuple),
#                                outputCommands = cms.untracked.vstring('keep *_*_*_MssmHbb' )
#                                )
# process.outpath = cms.EndPath(process.out)
