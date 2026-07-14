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

updatedJets = updatedPatJets.clone(
	addBTagInfo=False,
	jetSource='slimmedJets',
	jetCorrFactorsSource=cms.VInputTag(cms.InputTag("jetCorrFactors") ),
)

## AK8 Jets
jetCorrFactorsAK8 = patJetCorrFactors.clone(src='slimmedJetsAK8',
    levels = cms.vstring(
        'L1FastJet',
        'L2Relative',
        'L3Absolute',
	    'L2L3Residual'),
    payload = cms.string('AK8PFPuppi'),
    primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
)

updatedJetsAK8 = updatedPatJets.clone(
	addBTagInfo=False,
	jetSource='slimmedJetsAK8',
	jetCorrFactorsSource=cms.VInputTag(cms.InputTag("jetCorrFactorsAK8") ),
)

## Puppi Jets
jetPuppiCorrFactors = patJetCorrFactors.clone(src='slimmedJetsPuppi',
    levels = cms.vstring(
        'L1FastJet',
        'L2Relative',
        'L3Absolute',
	    'L2L3Residual'),
    payload = cms.string('AK4PFPuppi'),
    primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
)

updatedJetsPuppi = updatedPatJets.clone(
	addBTagInfo=False,
	jetSource='slimmedJetsPuppi',
	jetCorrFactorsSource=cms.VInputTag(cms.InputTag("jetPuppiCorrFactors") ),
)

jetAK4Task = cms.Task()
jetAK4Task.add(jetCorrFactors)
jetAK4Task.add(updatedJets)

jetAK8Task = cms.Task()
jetAK8Task.add(jetCorrFactorsAK8)
jetAK8Task.add(updatedJetsAK8)

jetPuppiTask = cms.Task()
jetPuppiTask.add(jetPuppiCorrFactors)
jetPuppiTask.add(updatedJetsPuppi)
