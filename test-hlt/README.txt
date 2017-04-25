#_________________________________#
#                                 #
#  CMSSW_9_0_X with 83X samples   #
#_________________________________#

### how to include ntuplizer (+ filters) within cmsDriver config
### cmsDriver commands

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
process.MssmHbbTrigger.PrimaryVertices   = cms.VInputTag(cms.InputTag('hltFastPrimaryVertex'),cms.InputTag('hltFastPVPixelVertices'),cms.InputTag('hltVerticesPF'))
process.MssmHbbTrigger.L1TJets           = cms.VInputTag(cms.InputTag('hltGtStage2Digis','Jet'))
process.MssmHbbTrigger.L1TMuons          = cms.VInputTag(cms.InputTag('hltGtStage2Digis','Muon'))
process.MssmHbbTrigger.ChargedCandidates = cms.VInputTag(cms.InputTag('hltL2MuonCandidates'),cms.InputTag('hltL3MuonCandidates') )
process.MssmHbbTrigger.CaloJets          = cms.VInputTag(cms.InputTag('hltAK4CaloJetsCorrectedIDPassed') )
process.MssmHbbTrigger.JetsTags          = cms.VInputTag(cms.InputTag('hltCombinedSecondaryVertexBJetTagsCalo'),cms.InputTag('hltCombinedSecondaryVertexBJetTagsPF'))
process.MssmHbbTrigger.PFJets            = cms.VInputTag(cms.InputTag('hltAK4PFJets'),cms.InputTag('hltAK4PFJetsLooseIDCorrected'),cms.InputTag('hltAK4PFJetsTightIDCorrected'))
process.MssmHbbTrigger.TriggerResults    = cms.VInputTag(cms.InputTag('TriggerResults','','HLT2'))
process.MssmHbbTrigger.TriggerPaths      = cms.vstring ('HLT_ZeroBias_v')
if isMC:
   # MC specific
   process.MssmHbbTrigger.PileupInfo        = cms.InputTag("addPileupInfo","","HLT")
   process.MssmHbbTrigger.GenFilterInfo     = cms.InputTag("genFilterEfficiencyProducer")
   process.MssmHbbTrigger.GenRunInfo        = cms.InputTag("generator")

process.Ntuplizer = cms.Sequence( process.TotalEvents + process.triggerFilter  + process.FilteredEvents + process.MssmHbbTrigger)
   
process.ntuplizer_step = cms.EndPath(process.Ntuplizer)

#_______________ Addition to cmsDriver - end

...
process.schedule.extend([process.endjob_step,process.ntuplizer_step]) # Modified wrt cmsDriver 

#_______________________________________________________________


# HLT_User_cff.py
# don't forget to remove the duplicated lines

hltGetConfiguration --cff --offline /dev/CMSSW_9_0_1/HLT/V26 --paths HLTriggerFirstPath,HLTriggerFinalPath --unprescale > HLT_User_cff.py
hltGetConfiguration --cff --offline /users/rwalsh/dev/CMSSW_9_0_X/MssmHbb/V7 >> HLT_User_cff.py

#_______________________________________________________________

# hlt.py with full output

hltGetConfiguration  /users/rwalsh/dev/CMSSW_9_0_X/MssmHbb/V7 \
--setup /dev/CMSSW_9_0_1/HLT/V26 \
--full \
--offline \
--mc \
--unprescale \
--process HLT2 \
--globaltag 90X_upgrade2017_TSG_Hcal_V2 \
--l1-emulator FullSimHcalTP \
--output full \
--input /store/mc/PhaseIFall16DR/SUSYGluGluToBBHToBB_NarrowWidth_M-300_TuneCUETP8M1_13TeV-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v1/50000/003C6E24-2415-E711-8D09-D067E5F91B8A.root \
--max-events 10 \
> hlt.py


#_______________________________________________________________


# cmsDriver commands

 MC
====

cmsDriver.py step2 \
--step=L1REPACK:FullSimHcalTP,HLT:User \
--conditions=90X_upgrade2017_TSG_Hcal_V2 \
--filein=/store/mc/PhaseIFall16DR/SUSYGluGluToBBHToBB_NarrowWidth_M-300_TuneCUETP8M1_13TeV-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v1/50000/003C6E24-2415-E711-8D09-D067E5F91B8A.root \
--secondfilein= \
--custom_conditions= \
--number=100 \
--mc\
--no_exec \
--datatier RAW\
--eventcontent=RAW\
--customise=HLTrigger/Configuration/CustomConfigs.L1THLT \
--era=Run2_2016 \
--customise= \
--scenario=pp \
--python_filename=ReHLT_L1Trepack_HLTUser_MCNtuple.py \
--processName=HLT2 \
--no_output


 DATA ( ***  NOT AVAILABLE YET!!! *** )
======

cmsDriver.py step2 \
--step=L1REPACK:Full,HLT:User \
--conditions=auto:run2_hlt_GRun \
--filein=/store/mc/PhaseIFall16DR/SUSYGluGluToBBHToBB_NarrowWidth_M-300_TuneCUETP8M1_13TeV-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v1/50000/003C6E24-2415-E711-8D09-D067E5F91B8A.root \
--custom_conditions= \
--number=10 \
--data \
--no_exec \
--datatier RAW\
--eventcontent=RAW\
--customise=HLTrigger/Configuration/CustomConfigs.L1THLT \
--era=Run2_2016 \
--customise= \
--scenario=pp \
--python_filename=ReHLT_L1Trepack_HLTUser80Xv35_DataNtuple.py \
--processName=HLT2 \
--no_output


