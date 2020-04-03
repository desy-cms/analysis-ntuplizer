# To be used with the following installation
#
# cmsrel CMSSW_10_2_14
# cd CMSSW_10_2_14/src
# cmsenv
# 
# git cms-init
# 
# git cms-merge-topic cms-nanoAOD:master-102X
# git checkout -b nanoAOD cms-nanoAOD/master-102X
# git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
# 
# git clone git@github.com:robervalwalsh/analysis-ntuplizer.git Analysis/Ntuplizer  ### latest commit 2803c8cc21d9ff5e66652b9ee4165e4271c8e2da
#________________________________________________________________________________________________________________________________________________

# For the ntuple production
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

#process = cms.Process('MssmHbb')
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD?rev=48#Running_on_various_datasets_from
process = cms.Process('MssmHbb',eras.Run2_2018,eras.run2_nanoAOD_102Xv1)

process.options = cms.untracked.PSet(

)

# execution with 4cores
process.options.numberOfThreads=cms.untracked.uint32(4)

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

##  Using MINIAOD. GlobalTag just in case jet re-clustering, L1 trigger filter  etc is needed to be done
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '102X_dataRun2_v10')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

## TFileService
output_file = 'ntuple.root'
process.TFileService = cms.Service('TFileService',
   fileName = cms.string(output_file)
)

### ==== Analysis imports ==== ###
from PhysicsTools.PatAlgos.tools.jetTools import *
from Analysis.Ntuplizer.run2018.v2.MssmHbbTriggerResultsFilter_cfi import *
from Analysis.Ntuplizer.run2018.v2.MssmHbbNtuplizerTriggerPaths_cfi import *
from Analysis.Ntuplizer.run2018.v2.MssmHbbNtuplizerL1Seeds_cfi import *
from Analysis.Ntuplizer.run2018.v2.MssmHbbNtuplizerTriggerObjects_cfi import *
from Analysis.Ntuplizer.run2018.v2.MssmHbbNtuplizerBtag_cfi import *
process.load('Analysis.Ntuplizer.run2018.v2.BJetRegression_cff')

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


### ==== Puppi specific ==== ####
from PhysicsTools.PatAlgos.tools.helpers import getPatAlgosToolsTask
patAlgosToolsTask = getPatAlgosToolsTask(process)
from PhysicsTools.PatAlgos.patPuppiJetSpecificProducer_cfi import patPuppiJetSpecificProducer
process.patPuppiJetSpecificProducer = patPuppiJetSpecificProducer.clone(
   src=cms.InputTag("slimmedJetsPuppi"),
)
patAlgosToolsTask.add(process.patPuppiJetSpecificProducer)
updateJetCollection(
   process,
   labelName = 'PuppiJetSpecific',
   jetSource = cms.InputTag('slimmedJetsPuppi'),
)
process.updatedPatJetsPuppiJetSpecific.userData.userFloats.src = ['patPuppiJetSpecificProducer:puppiMultiplicity', 'patPuppiJetSpecificProducer:neutralPuppiMultiplicity', 'patPuppiJetSpecificProducer:neutralHadronPuppiMultiplicity', 'patPuppiJetSpecificProducer:photonPuppiMultiplicity', 'patPuppiJetSpecificProducer:HFHadronPuppiMultiplicity', 'patPuppiJetSpecificProducer:HFEMPuppiMultiplicity' ]
process.PuppiJetSpecific = cms.Task()
process.PuppiJetSpecific.add(process.patPuppiJetSpecificProducer)
process.PuppiJetSpecific.add(process.updatedPatJetsPuppiJetSpecific)



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
    jetSource = cms.InputTag('updatedPatJetsPuppiJetSpecific'),
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
    FixedGridRhoAll = cms.InputTag ('fixedGridRhoAll'),
    PatMuons        = cms.VInputTag(cms.InputTag('slimmedMuons') ), 
    PrimaryVertices = cms.VInputTag(cms.InputTag('offlineSlimmedPrimaryVertices') ),
    TriggerResults  = cms.VInputTag(cms.InputTag('TriggerResults','','HLT') ),
    L1TJets         = cms.VInputTag(cms.InputTag('caloStage2Digis','Jet','RECO'), ),
    L1TMuons        = cms.VInputTag(cms.InputTag('gmtStage2Digis','Muon','RECO'), ),
    TriggerObjectStandAlone = cms.VInputTag(cms.InputTag('slimmedPatTrigger'), ),

)

process.p = cms.Path(process.TotalEvents + 
                     process.triggerSelection +
                     process.primaryVertexFilter +
                     process.FilteredEvents + 
                     process.MssmHbb,
                     process.PuppiJetSpecific,
                     process.BJetRegression,
                     process.AK4Jets,
                     process.AK4PuppiJets,
                     process.AK8Jets,
                    )

readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
process.source = cms.Source ('PoolSource',fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend( [
#   '/store/data/Run2018A/JetHT/MINIAOD/17Sep2018-v1/00000/F769A2D8-AE75-DB46-AAD1-BE567B3D452F.root',
#   '/store/data/Run2018B/JetHT/MINIAOD/17Sep2018-v1/60000/DCBD418B-A67F-0A41-9C1C-EE32AB0C7296.root',
#   '/store/data/Run2018C/JetHT/MINIAOD/17Sep2018-v1/100000/9E3FD670-4672-BD4F-9E09-297E7CC77AD4.root',
   '/store/data/Run2018D/JetHT/MINIAOD/PromptReco-v2/000/325/172/00000/0E546AB1-677A-DD4B-BFFE-DF8419E0FAE3.root',
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
