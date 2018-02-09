# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step2 --step=L1REPACK:Full,HLT:MssmHbb18 --conditions=92X_dataRun2_HLT_v7 --custom_conditions=L1Menu_Collisions2017_v4,L1TUtmTriggerMenuRcd --filein=/store/data/Run2017E/ZeroBias/MINIAOD/PromptReco-v1/000/303/825/00000/E6E9912B-7BA4-E711-85D5-02163E01A570.root --secondfilein=/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/B4BFA35E-FFA0-E711-86EC-02163E019BB2.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/BE88665C-02A1-E711-BC02-02163E011F1B.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/C03F9BCA-00A1-E711-BF30-02163E01465A.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/CA1126DC-00A1-E711-94E3-02163E012B11.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/CAE7BDDA-02A1-E711-B8D4-02163E0128FB.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/CED45FBA-03A1-E711-8487-02163E019D30.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/D03A5C04-05A1-E711-9070-02163E01444E.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/E8E8A257-FFA0-E711-B037-02163E019DAC.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/ECF7CB33-05A1-E711-97DE-02163E019CBE.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/EE5F1FDB-FFA0-E711-92D8-02163E01A583.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/EE7922D6-00A1-E711-BD43-02163E01465E.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/F0A51665-FFA0-E711-AD3D-02163E01A45E.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/F6D4465F-FFA0-E711-A500-02163E014145.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/AE668314-05A1-E711-8A06-02163E019CFE.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/AC311454-02A1-E711-8602-02163E014747.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/A0D742B9-01A1-E711-A5DE-02163E0143E5.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/8EF5B163-FFA0-E711-AD81-02163E01A2B1.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/8A66C15A-FFA0-E711-ABC9-02163E01A648.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/88814D71-02A1-E711-BB84-02163E01A20D.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/7EBA0D02-00A1-E711-8EB1-02163E01462A.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/741C2960-01A1-E711-95C1-02163E01410D.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/662E8F61-FFA0-E711-9AA4-02163E011EBB.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/62AA6CFC-04A1-E711-9240-02163E011E54.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/62A1840B-05A1-E711-9B60-02163E013914.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/36F2F6D5-02A1-E711-8154-02163E014145.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/14AB9FBA-01A1-E711-BC43-02163E011B4D.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/146975A2-03A1-E711-8FC4-02163E01A739.root,/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/107801B1-03A1-E711-9537-02163E01A525.root --number=10 --data --no_exec --datatier RAW --eventcontent=RAW --customise=HLTrigger/Configuration/CustomConfigs.L1THLT --era=Run2_2017 --customise= --scenario=pp --python_filename=rerun-hlt_mssmhbb_ntuplizer.py --processName=HLT2 --no_output
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('HLT2',eras.Run2_2017)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.SimL1EmulatorRepack_Full_cff')
process.load('HLTrigger.Configuration.HLT_MssmHbb18Physics_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')


process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('/store/data/Run2017E/ZeroBias/MINIAOD/PromptReco-v1/000/303/825/00000/E6E9912B-7BA4-E711-85D5-02163E01A570.root'),
    secondaryFileNames = cms.untracked.vstring('/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/B4BFA35E-FFA0-E711-86EC-02163E019BB2.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/BE88665C-02A1-E711-BC02-02163E011F1B.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/C03F9BCA-00A1-E711-BF30-02163E01465A.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/CA1126DC-00A1-E711-94E3-02163E012B11.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/CAE7BDDA-02A1-E711-B8D4-02163E0128FB.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/CED45FBA-03A1-E711-8487-02163E019D30.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/D03A5C04-05A1-E711-9070-02163E01444E.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/E8E8A257-FFA0-E711-B037-02163E019DAC.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/ECF7CB33-05A1-E711-97DE-02163E019CBE.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/EE5F1FDB-FFA0-E711-92D8-02163E01A583.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/EE7922D6-00A1-E711-BD43-02163E01465E.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/F0A51665-FFA0-E711-AD3D-02163E01A45E.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/F6D4465F-FFA0-E711-A500-02163E014145.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/AE668314-05A1-E711-8A06-02163E019CFE.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/AC311454-02A1-E711-8602-02163E014747.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/A0D742B9-01A1-E711-A5DE-02163E0143E5.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/8EF5B163-FFA0-E711-AD81-02163E01A2B1.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/8A66C15A-FFA0-E711-ABC9-02163E01A648.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/88814D71-02A1-E711-BB84-02163E01A20D.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/7EBA0D02-00A1-E711-8EB1-02163E01462A.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/741C2960-01A1-E711-95C1-02163E01410D.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/662E8F61-FFA0-E711-9AA4-02163E011EBB.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/62AA6CFC-04A1-E711-9240-02163E011E54.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/62A1840B-05A1-E711-9B60-02163E013914.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/36F2F6D5-02A1-E711-8154-02163E014145.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/14AB9FBA-01A1-E711-BC43-02163E011B4D.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/146975A2-03A1-E711-8FC4-02163E01A739.root', 
        '/store/data/Run2017E/ZeroBias/RAW/v1/000/303/825/00000/107801B1-03A1-E711-9537-02163E01A525.root')
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
process.GlobalTag = GlobalTag(process.GlobalTag, '92X_dataRun2_HLT_v7', 'L1Menu_Collisions2017_v4,L1TUtmTriggerMenuRcd')

from Analysis.Ntuplizer.TriggerFilter_cfi import triggerFilter
process.triggerFilter = triggerFilter
process.triggerFilter.hltResults = cms.InputTag( "TriggerResults", "", "HLT2" )
process.triggerFilter.triggerConditions = cms.vstring(
                   'HLT_ZeroBias_v*',
                   'HLT_Mu12_DoublePFJets40_CaloBTagCSV_p33_v*',
                   'HLT_Mu12_DoublePFJets40_CaloBTagCSV0p80_px_v*',
                   'HLT_Mu12_DoublePFJets40_CaloBTagCSV0p84_px_v*',
                   'HLT_Mu12_DoublePFJets40_CaloBTagCSV0p88_px_v*',
                   'HLT_Mu12_DoublePFJets40MaxDeta1p6_DoubleCaloBTagCSV_p33_v*',
                   'HLT_Mu12_DoublePFJets40MaxDeta1p6_DoubleCaloBTagCSV0p80_px_v*',
                   'HLT_Mu12_DoublePFJets40MaxDeta1p6_DoubleCaloBTagCSV0p84_px_v*',
                   'HLT_Mu12_DoublePFJets40MaxDeta1p6_DoubleCaloBTagCSV0p88_px_v*',
                   'HLT_DoublePFJets40_CaloBTagCSV_p33_v*',
                   'HLT_DoublePFJets40_CaloBTagCSV0p80_px_v*',
                   'HLT_DoublePFJets40_CaloBTagCSV0p84_px_v*',
                   'HLT_DoublePFJets40_CaloBTagCSV0p88_px_v*',
                   'HLT_DoublePFJets100_CaloBTagCSV_p33_v*',
                   'HLT_DoublePFJets100_CaloBTagCSV0p80_px_v*',
                   'HLT_DoublePFJets100_CaloBTagCSV0p84_px_v*',
                   'HLT_DoublePFJets100_CaloBTagCSV0p88_px_v*',
                   'HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_p33_v*',
                   'HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV0p80_px_v*',
                   'HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV0p84_px_v*',
                   'HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV0p88_px_v*',
                   'HLT_SingleJet30_Mu12_SinglePFJet40_v*',
                   'HLT_PFJet40_v*',
                   'HLT_Mu8_v*',
                   'HLT_Mu3_PFJet40_v*',
                   'HLT_DoublePFJets40_v*',
                   'HLT_Mu12_v*',
                   'HLT_Mu12_PFJet40_v*',
)

## ============ EVENT FILTER COUNTER ===============
## Filter counter (maybe more useful for MC)
process.TotalEvents    = cms.EDProducer('EventCountProducer')
process.FilteredEvents = cms.EDProducer('EventCountProducer')

# Path and EndPath definitions
process.L1RePack_step = cms.Path(process.SimL1Emulator)
process.endjob_step = cms.EndPath(process.endOfProcess)

from Analysis.Ntuplizer.NtuplizerHLT_cfi import TFileService
process.TFileService = TFileService
from Analysis.Ntuplizer.NtuplizerHLT_cfi import ntuplizer
process.MssmHbb = ntuplizer
process.MssmHbb.TriggerResults  = cms.VInputTag(cms.InputTag('TriggerResults','','HLT2') )
process.MssmHbb.TriggerEvent    = cms.VInputTag(cms.InputTag('hltTriggerSummaryAOD','','HLT2'), )
process.MssmHbb.ReadPrescale    = cms.bool(False)

process.Ntuplizer = cms.Sequence(process.TotalEvents + process.triggerFilter + process.FilteredEvents + process.MssmHbb )
process.ntuplizer_step = cms.EndPath(process.Ntuplizer)


# Schedule definition
process.schedule = cms.Schedule(process.L1RePack_step)
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.endjob_step,process.ntuplizer_step])
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from HLTrigger.Configuration.CustomConfigs
from HLTrigger.Configuration.CustomConfigs import L1THLT 

#call to customisation function L1THLT imported from HLTrigger.Configuration.CustomConfigs
process = L1THLT(process)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
