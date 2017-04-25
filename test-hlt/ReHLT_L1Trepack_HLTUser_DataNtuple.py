# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step2 --step=L1REPACK:Full,HLT:UserBTagMu20 --conditions=auto:run2_hlt_GRun --filein=/store/data/Run2016H/BTagMu/RAW/v1/000/283/408/00000/78879B75-CC94-E611-BAE6-02163E0146EA.root --custom_conditions= --number=10 --data --no_exec --datatier RAW --eventcontent=RAW --customise=HLTrigger/Configuration/CustomConfigs.L1THLT --era=Run2_2016 --customise= --scenario=pp --python_filename=ReHLT_L1Trepack_HLTUserBtagMu20_Ntuple.py --processName=HLT2 --no_output
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('HLT2',eras.Run2_2016)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.SimL1EmulatorRepack_Full_cff')
process.load('HLTrigger.Configuration.HLT_User_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

# Input source
# Examples
# ('/store/data/Run2016H/BTagMu/RAW/v1/000/283/408/00000/78879B75-CC94-E611-BAE6-02163E0146EA.root'),
# ('/store/data/Run2016H/ZeroBiasBunchTrains0/RAW/v1/000/283/171/00000/2E41F4FF-EA91-E611-9DBB-02163E0145F1.root'),
# ('/store/data/Run2016H/ParkingZeroBias0/RAW/v1/000/283/885/00000/5453166E-DA9D-E611-A050-FA163EEEB45D.root'),
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('/store/data/Run2016H/BTagMu/RAW/v1/000/283/408/00000/78879B75-CC94-E611-BAE6-02163E0146EA.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step2 nevts:10'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

# Additional output definition

# Other statements
from HLTrigger.Configuration.CustomConfigs import ProcessName
process = ProcessName(process)

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_hlt_GRun', '')

# Path and EndPath definitions
process.L1RePack_step = cms.Path(process.SimL1Emulator)
process.endjob_step = cms.EndPath(process.endOfProcess)

#_______________ Addition to cmsDriver - begin

isMC = False

## Filter counter (maybe more useful for MC)
process.TotalEvents    = cms.EDProducer("EventCountProducer")
process.FilteredEvents = cms.EDProducer("EventCountProducer")

# pileup filter MC
process.RemovePileUpDominatedEventsGen = cms.EDFilter("RemovePileUpDominatedEventsGen")

# Trigger filter (HLT config)
from Analysis.Ntuplizer.TriggerFilter_cfi import triggerFilter

# =========================
# Trigger config modifications
# Example triggers
#                                  'HLT_BTagMu_DiJet20_Mu5_v*',
#                                  'HLT_ZeroBias_BunchTrains_part*',
#                                  'HLT_ZeroBias_part0_v*',
#                                  'HLT_DoubleJetsC100_DoubleBTagCSV_p014_DoublePFJetsC100MaxDeta1p6_v*',
process.triggerFilter = triggerFilter.clone()
process.triggerFilter.hltResults = cms.InputTag( 'TriggerResults', '', 'HLT' )
process.triggerFilter.triggerConditions  = cms.vstring  ('HLT_DoubleJetsC100_DoubleBTagCSV_p014_DoublePFJetsC100MaxDeta1p6_v*')
# =========================                                  
# Filtering the trigger sequence                                  
# comment or modified the lines below if no filter or other filters are required
if isMC:
   process.triggerFilter.hltResults = cms.InputTag( 'TriggerResults', '', 'HLT2' )
   process.triggerFilter.triggerConditions  = cms.vstring('HLT_ZeroBias_v*')
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
process.MssmHbbTrigger.L1TJets           = cms.VInputTag(cms.InputTag('hltCaloStage2Digis','Jet'))
process.MssmHbbTrigger.L1TMuons          = cms.VInputTag(cms.InputTag('hltGmtStage2Digis','Muon'))
process.MssmHbbTrigger.ChargedCandidates = cms.VInputTag(cms.InputTag('hltL2MuonCandidates'),cms.InputTag('hltL3MuonCandidates') )
process.MssmHbbTrigger.CaloJets          = cms.VInputTag(cms.InputTag('hltAK4CaloJetsCorrectedIDPassed') )
process.MssmHbbTrigger.JetsTags          = cms.VInputTag(cms.InputTag('hltCombinedSecondaryVertexBJetTagsCalo'))
process.MssmHbbTrigger.PFJets            = cms.VInputTag(cms.InputTag('hltAK4PFJets'),cms.InputTag('hltAK4PFJetsLooseIDCorrected'),cms.InputTag('hltAK4PFJetsTightIDCorrected'))
process.MssmHbbTrigger.TriggerResults    = cms.VInputTag(cms.InputTag('TriggerResults','','HLT2'))
process.MssmHbbTrigger.TriggerPaths      = cms.vstring ('HLT_ZeroBias_v','HLT_CaloJets_Muons_CaloBTagCSV_PFJets_v')
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

# End of customisation functions

