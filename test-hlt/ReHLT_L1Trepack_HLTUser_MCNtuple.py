# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step2 --step=L1REPACK:FullSimHcalTP,HLT:User --conditions=90X_upgrade2017_TSG_Hcal_V2 --filein=/store/mc/PhaseIFall16DR/SUSYGluGluToBBHToBB_NarrowWidth_M-300_TuneCUETP8M1_13TeV-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v1/50000/003C6E24-2415-E711-8D09-D067E5F91B8A.root --secondfilein= --custom_conditions= --number=100 --mc --no_exec --datatier RAW --eventcontent=RAW --customise=HLTrigger/Configuration/CustomConfigs.L1THLT --era=Run2_2016 --customise= --scenario=pp --python_filename=ReHLT_L1Trepack_HLTUser_MCNtuple.py --processName=HLT2 --no_output
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('HLT2',eras.Run2_2016)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.SimL1EmulatorRepack_FullSimHcalTP_cff')
process.load('HLTrigger.Configuration.HLT_User_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("PoolSource",
 #   fileNames = cms.untracked.vstring('/store/mc/PhaseIFall16DR/SUSYGluGluToBBHToBB_NarrowWidth_M-300_TuneCUETP8M1_13TeV-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v1/50000/003C6E24-2415-E711-8D09-D067E5F91B8A.root'),
    fileNames = cms.untracked.vstring('/store/mc/PhaseIFall16DR/SUSYGluGluToBBHToBB_NarrowWidth_M-120_TuneCUETP8M1_13TeV-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v1/00000/02C6F273-9115-E711-AF44-FA163E441C41.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step2 nevts:100'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

# Additional output definition

# Other statements
from HLTrigger.Configuration.CustomConfigs import ProcessName
process = ProcessName(process)

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '90X_upgrade2017_TSG_Hcal_V2', '')

# Path and EndPath definitions
process.L1RePack_step = cms.Path(process.SimL1Emulator)
process.endjob_step = cms.EndPath(process.endOfProcess)

#_______________________________________________________________

# include ntuplizer (+ filters) within cmsDriver config
#_______________ Addition to cmsDriver - begin

isMC = True

## Filter counter (maybe more useful for MC)
process.TotalEvents    = cms.EDProducer("EventCountProducer")
process.FilteredEvents = cms.EDProducer("EventCountProducer")

# pileup filter MC
process.RemovePileUpDominatedEventsGen = cms.EDFilter("RemovePileUpDominatedEventsGen",
     generatorInfo = cms.InputTag("generator"),
     pileupSummaryInfos = cms.InputTag("addPileupInfo"),
     )

# Trigger filter (HLT config)
from Analysis.Ntuplizer.TriggerFilter_cfi import triggerFilter

# =========================
# Trigger config modifications
process.triggerFilter = triggerFilter.clone()
process.triggerFilter.hltResults = cms.InputTag( 'TriggerResults', '', 'HLT' )
process.triggerFilter.triggerConditions  = cms.vstring  ('HLT_ZeroBias_v*')
# =========================                                  
# Filtering the trigger sequence                                  
# comment or modified the lines below if no filter or other filters are required
if isMC:
   process.triggerFilter.hltResults = cms.InputTag( 'TriggerResults', '', 'HLT2' )
   process.triggerFilter.triggerConditions  = cms.vstring('HLT_ZeroBias_v*','HLT_Mu_CaloJets_CaloBTagCSV_PFJets_v*')
   process.HLTBeginSequence.insert(-1,process.RemovePileUpDominatedEventsGen)   # qcd MC
else:
   process.HLTBeginSequence.insert(-1,process.triggerFilter)                    # data
# =========================


# Ntuplizer
from Analysis.Ntuplizer.Ntuplizer_cfi import TFileService
process.TFileService = TFileService.clone()

from Analysis.Ntuplizer.Ntuplizer_cfi import ntuplizer
process.MssmHbbTrigger = ntuplizer.clone()
process.MssmHbbTrigger.MonteCarlo        = cms.bool(isMC)
process.MssmHbbTrigger.TotalEvents       = cms.InputTag("TotalEvents")
process.MssmHbbTrigger.FilteredEvents    = cms.InputTag("FilteredEvents")
process.MssmHbbTrigger.PrimaryVertices   = cms.VInputTag(cms.InputTag('hltFastPrimaryVertex'),cms.InputTag('hltFastPVPixelVertices'))
process.MssmHbbTrigger.L1TJets           = cms.VInputTag(cms.InputTag('hltGtStage2Digis','Jet'))
process.MssmHbbTrigger.L1TMuons          = cms.VInputTag(cms.InputTag('hltGtStage2Digis','Muon'))
process.MssmHbbTrigger.ChargedCandidates = cms.VInputTag(cms.InputTag('hltL2MuonCandidates'),cms.InputTag('hltL3MuonCandidates') )
process.MssmHbbTrigger.CaloJets          = cms.VInputTag(cms.InputTag('hltAK4CaloJetsCorrectedIDPassed') )
process.MssmHbbTrigger.JetsTags          = cms.VInputTag(cms.InputTag('hltCombinedSecondaryVertexBJetTagsCalo'))
process.MssmHbbTrigger.PFJets            = cms.VInputTag(cms.InputTag('hltAK4PFJets'),cms.InputTag('hltAK4PFJetsLooseIDCorrected'),cms.InputTag('hltAK4PFJetsTightIDCorrected'))
process.MssmHbbTrigger.TriggerResults    = cms.VInputTag(cms.InputTag('TriggerResults','','HLT2'))
if isMC:
   # MC specific
   process.MssmHbbTrigger.PileupInfo        = cms.InputTag("addPileupInfo","","HLT")
   process.MssmHbbTrigger.GenFilterInfo     = cms.InputTag("genFilterEfficiencyProducer")
   process.MssmHbbTrigger.GenRunInfo        = cms.InputTag("generator")

process.Ntuplizer = cms.Sequence( process.TotalEvents + process.triggerFilter  + process.FilteredEvents + process.MssmHbbTrigger)
   
process.ntuplizer_step = cms.EndPath(process.Ntuplizer)

#_______________ Addition to cmsDriver - end


# Schedule definition
process.schedule = cms.Schedule(process.L1RePack_step)
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.endjob_step,process.ntuplizer_step]) # Modified wrt cmsDriver 

# customisation of the process.

# Automatic addition of the customisation function from HLTrigger.Configuration.CustomConfigs
from HLTrigger.Configuration.CustomConfigs import L1THLT 

#call to customisation function L1THLT imported from HLTrigger.Configuration.CustomConfigs
process = L1THLT(process)

# Automatic addition of the customisation function from HLTrigger.Configuration.customizeHLTforMC
from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforMC 

#call to customisation function customizeHLTforMC imported from HLTrigger.Configuration.customizeHLTforMC
process = customizeHLTforMC(process)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
