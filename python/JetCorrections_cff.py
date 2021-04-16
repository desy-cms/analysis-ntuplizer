import FWCore.ParameterSet.Config as cms

from  PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
# Note: Safe to always add 'L2L3Residual' as MC contains dummy L2L3Residual corrections (always set to 1)
#      (cf. https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections#CMSSW_7_6_4_and_above )

from  PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cfi import *

## AK4 Jets
jetCorrFactors = patJetCorrFactors.clone(src='slimmedJets',
    levels = cms.vstring(
        'L1FastJet',
        'L2Relative',
        'L3Absolute',
	     'L2L3Residual'),
    payload = cms.string('AK4PFchs'),
    primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
)

updatedPatJets = updatedPatJets.clone(
	addBTagInfo=False,
	jetSource='slimmedJets',
	jetCorrFactorsSource=cms.VInputTag(cms.InputTag("jetCorrFactors") ),
)

AK4Jets = cms.Task()
AK4Jets.add(jetCorrFactors)
AK4Jets.add(updatedPatJets)


## AK8 Jets
jetCorrFactorsAK8 = patJetCorrFactors.clone(src='slimmedJetsAK8',
    levels = cms.vstring(
        'L1FastJet',
        'L2Relative',
        'L3Absolute',
	     'L2L3Residual'),
    payload = cms.string('AK8PFchs'),
    primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
)

updatedPatJetsAK8 = updatedPatJets.clone(
	addBTagInfo=False,
	jetSource='slimmedJetsAK8',
	jetCorrFactorsSource=cms.VInputTag(cms.InputTag("jetCorrFactorsAK8") ),
)

AK8Jets = cms.Task()
AK8Jets.add(jetCorrFactorsAK8)
AK8Jets.add(updatedPatJetsAK8)


## Puppi Jets
jetCorrFactorsPuppi = patJetCorrFactors.clone(src='slimmedJetsPuppi',
    levels = cms.vstring(
        'L1FastJet',
        'L2Relative',
        'L3Absolute',
	     'L2L3Residual'),
    payload = cms.string('AK4PFPuppi'),
    primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
)

updatedPatJetsPuppi = updatedPatJets.clone(
	addBTagInfo=False,
	jetSource='slimmedJetsPuppi',
	jetCorrFactorsSource=cms.VInputTag(cms.InputTag("jetCorrFactorsPuppi") ),
)

PuppiJets = cms.Task()
PuppiJets.add(jetCorrFactorsPuppi)
PuppiJets.add(updatedPatJetsPuppi)


