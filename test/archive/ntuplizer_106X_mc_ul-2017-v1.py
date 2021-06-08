# To be used with the following installation
#
# cmsrel CMSSW_9_4_12
# cd CMSSW_9_4_12/src
# cmsenv
# 
# git cms-init
# 
# git cms-merge-topic cms-nanoAOD:master-94X
# git checkout -b nanoAOD cms-nanoAOD/master-94X
# git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
# 
# git cms-addpkg RecoBTag/TensorFlow
# git cherry-pick 94ceae257f846998c357fcad408986cc8a039152
# 
# git clone git@github.com:robervalwalsh/analysis-ntuplizer.git Analysis/Ntuplizer  ### latest commit 9fad3dd274a59394188b70d1984039c64f18f158
#________________________________________________________________________________________________________________________________________________


# For the ntuple production
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

#process = cms.Process('MssmHbb',eras.Run2_2017,eras.run2_nanoAOD_94XMiniAODv2)
# lack reference -PPD twiki???


#################### LOOK BELOW 

#process = cms.Process('MssmHbb',eras.Run2_2017,eras.run2_nanoAOD_94XMiniAODv2,eras.run2_miniAOD_94XFall17)
process = cms.Process('MssmHbb')

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100000)

##  Using MINIAOD. GlobalTag just in case jet re-clustering, L1 trigger filter  etc is needed to be done
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_mc2017_realistic_v9')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

## TFileService
output_file = 'ntuple_mc.root'
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



### ============ Jet energy correctiosn update ==============
## Update the slimmedJets in miniAOD: corrections from the chosen Global Tag are applied and the b-tag discriminators are re-evaluated
updateJetCollection(
    process,
    labelName = 'Tmp',
    jetSource = cms.InputTag('slimmedJetsWithUserDataWithReg'),
    pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
    svSource = cms.InputTag('slimmedSecondaryVertices'),
    jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']), 'None'),
    btagDiscriminators = bTagDiscriminators,
)
process.BtagDeepFlavour = cms.Task()
# corrections on slimmedJets with regresssion
process.BtagDeepFlavour.add(process.patJetCorrFactorsTmp)
process.BtagDeepFlavour.add(process.patJetCorrFactorsTransientCorrectedTmp)
process.BtagDeepFlavour.add(process.selectedUpdatedPatJetsTmp)
process.BtagDeepFlavour.add(process.updatedPatJetsTmp)
process.BtagDeepFlavour.add(process.updatedPatJetsTransientCorrectedTmp)
# deepFlavour on corrected slimmedJets with regression
process.BtagDeepFlavour.add(process.pfDeepCSVTagInfosTmp)
process.BtagDeepFlavour.add(process.pfDeepFlavourJetTagsTmp)
process.BtagDeepFlavour.add(process.pfDeepFlavourTagInfosTmp)
process.BtagDeepFlavour.add(process.pfImpactParameterTagInfosTmp)
process.BtagDeepFlavour.add(process.pfInclusiveSecondaryVertexFinderTagInfosTmp)
# tradition: using the default name for the jet collection  in the analysis
process.updatedPatJets = process.selectedUpdatedPatJetsTmp.clone()
process.BtagDeepFlavour.add(process.updatedPatJets)


### ============ Jet energy correctiosn update ==============
## Update the slimmedJetsPuppi in miniAOD: corrections from the chosen Global Tag are applied and the b-tag discriminators are re-evaluated
updateJetCollection(
    process,
    labelName = 'PuppiTmp',
    jetSource = cms.InputTag('updatedPatJetsPuppiJetSpecific'),
    pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
    svSource = cms.InputTag('slimmedSecondaryVertices'),
    jetCorrections = ('AK4PFPuppi', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']), 'None'),
    btagDiscriminators = bTagDiscriminators,
)
process.BtagDeepFlavourPuppi = cms.Task()
# corrections on slimmedJets with regresssion
process.BtagDeepFlavourPuppi.add(process.patJetCorrFactorsPuppiTmp)
process.BtagDeepFlavourPuppi.add(process.patJetCorrFactorsTransientCorrectedPuppiTmp)
process.BtagDeepFlavourPuppi.add(process.selectedUpdatedPatJetsPuppiTmp)
process.BtagDeepFlavourPuppi.add(process.updatedPatJetsPuppiTmp)
process.BtagDeepFlavourPuppi.add(process.updatedPatJetsTransientCorrectedPuppiTmp)
# deepFlavour on corrected slimmedJets with regression
process.BtagDeepFlavourPuppi.add(process.pfDeepCSVTagInfosPuppiTmp)
process.BtagDeepFlavourPuppi.add(process.pfDeepFlavourJetTagsPuppiTmp)
process.BtagDeepFlavourPuppi.add(process.pfDeepFlavourTagInfosPuppiTmp)
process.BtagDeepFlavourPuppi.add(process.pfImpactParameterTagInfosPuppiTmp)
process.BtagDeepFlavourPuppi.add(process.pfInclusiveSecondaryVertexFinderTagInfosPuppiTmp)
# tradition: using the default name for the jet collection  in the analysis
process.updatedPatJetsPuppi = process.selectedUpdatedPatJetsPuppiTmp.clone()
process.BtagDeepFlavourPuppi.add(process.updatedPatJetsPuppi)


### ============ Jet energy correctiosn update ==============
## Update the slimmedJetsAK8 in miniAOD: corrections from the chosen Global Tag are applied 
updateJetCollection(
    process,
    labelName = 'AK8',
    pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
    svSource = cms.InputTag('slimmedSecondaryVertices'),
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
    
    MonteCarlo      = cms.bool(True),
    ## Monte Carlo only
    CrossSection    = cms.double(1.),  # in pb
    GenFilterInfo   = cms.InputTag("genFilterEfficiencyProducer"),
    GenRunInfo      = cms.InputTag("generator"),
    GenEventInfo    = cms.InputTag("generator"),
    GenJets         = cms.VInputTag(cms.InputTag("slimmedGenJets")),
    GenParticles    = cms.VInputTag(cms.InputTag("prunedGenParticles")),
    PileupInfo      = cms.InputTag("slimmedAddPileupInfo"),    
    ###################
    TotalEvents     = cms.InputTag ('TotalEvents'),
    FilteredEvents  = cms.InputTag ('FilteredEvents'),
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


#process.p1 = cms.Path(process.task)

process.p = cms.Path(process.TotalEvents + 
#                     process.triggerSelection +
                     process.primaryVertexFilter +
                     process.FilteredEvents + 
                     process.MssmHbb,
                     process.PuppiJetSpecific,
                     process.BJetRegression,
                     process.BtagDeepFlavour,
                     process.BtagDeepFlavourPuppi,
                     process.AK8Jets,
                    )

readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
process.source = cms.Source ('PoolSource',fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend( [
#   '/store/mc/RunIIFall17MiniAOD/SUSYGluGluToBBHToBB_M-350_TuneCP5_13TeV-pythia8/MINIAODSIM/94X_mc2017_realistic_v11-v1/00000/02D5DD76-241B-E811-A02E-0CC47A2B0214.root',
#   '/store/mc/RunIIFall17MiniAODv2/SUSYGluGluToBBHToBB_NarrowWidth_M-350_TuneCP5_13TeV-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/20000/5CCCC2D7-BB41-E811-8AD3-FA163EF96190.root',
#   '/store/mc/RunIIFall17MiniAODv2/SUSYGluGluToBBHToBB_M-500_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/120000/0C677CBE-1FC5-E811-B002-0242AC1C0505.root',
   ' /store/mc/RunIISummer19UL17MiniAODv2/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v1/270000/0CFCAF86-DCC6-FE49-86F8-7339E3663BC8.root'   
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
# ## ============ JSON Certified data ===============   BE CAREFUL!!!
# ## Don't use with CRAB!!!
# import FWCore.PythonUtilities.LumiList as LumiList
# import FWCore.ParameterSet.Types as CfgTypes
# process.source.lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange())
# JSONfile = 'json.txt'
# myLumis = LumiList.LumiList(filename = JSONfile).getCMSSWString().split(',')
# process.source.lumisToProcess.extend(myLumis)
