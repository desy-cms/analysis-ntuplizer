import FWCore.ParameterSet.Config as cms

from  PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
# Note: Safe to always add 'L2L3Residual' as MC contains dummy L2L3Residual corrections (always set to 1)
#      (cf. https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections#CMSSW_7_6_4_and_above )

from  PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cfi import *

## AK4 Jets
correctionFactorsJets = patJetCorrFactors.clone(src='slimmedJets',
    levels = cms.vstring(
        'L1FastJet',
        'L2Relative',
        'L3Absolute',
	    'L2L3Residual'),
    payload = cms.string('AK4PFchs'),
    primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
)

correctedJets = updatedPatJets.clone(
	addBTagInfo=False,
	jetSource='slimmedJets',
	jetCorrFactorsSource=cms.VInputTag(cms.InputTag("correctionFactorJets") ),
)

jecJets = cms.Task()
jecJets.add(correctionFactorsJets)
jecJets.add(correctedJets)


## AK8 Jets
correctionFactorsJetsAK8 = patJetCorrFactors.clone(src='slimmedJetsAK8',
    levels = cms.vstring(
        'L1FastJet',
        'L2Relative',
        'L3Absolute',
	    'L2L3Residual'),
    payload = cms.string('AK8PFchs'),
    primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
)

correctedJetsAK8 = updatedPatJets.clone(
	addBTagInfo=False,
	jetSource='slimmedJetsAK8',
	jetCorrFactorsSource=cms.VInputTag(cms.InputTag("correctionFactorsJetsAK8") ),
)

jecJetsAK8 = cms.Task()
jecJetsAK8.add(correctionFactorsJetsAK8)
jecJetsAK8.add(correctedJetsAK8)


## Puppi Jets
correctionFactorsJetsPuppi = patJetCorrFactors.clone(src='slimmedJetsPuppi',
    levels = cms.vstring(
        'L1FastJet',
        'L2Relative',
        'L3Absolute',
	    'L2L3Residual'),
    payload = cms.string('AK4PFPuppi'),
    primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
)

correctedJetsPuppi = updatedPatJets.clone(
	addBTagInfo=False,
	jetSource='slimmedJetsPuppi',
	jetCorrFactorsSource=cms.VInputTag(cms.InputTag("correctionFactorsJetsPuppi") ),
)

jecJetsPuppi = cms.Task()
jecJetsPuppi.add(correctionFactorsJetsPuppi)
jecJetsPuppi.add(correctedJetsPuppi)
