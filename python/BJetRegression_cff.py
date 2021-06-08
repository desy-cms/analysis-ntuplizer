import FWCore.ParameterSet.Config as cms

from PhysicsTools.NanoAOD.jets_cff import bJetVars,updatedJetsWithUserData,bjetNN


bJetVars = bJetVars.clone(
    src = cms.InputTag("updatedPatJets"),    
)
updatedJetsWithUserData = updatedJetsWithUserData.clone(
    src = cms.InputTag("updatedPatJets"),
    userFloats = cms.PSet(
         leadTrackPt = cms.InputTag("bJetVars:leadTrackPt"),
         leptonPtRel = cms.InputTag("bJetVars:leptonPtRel"),
         leptonPtRatio = cms.InputTag("bJetVars:leptonPtRatio"),
         leptonPtRelInv = cms.InputTag("bJetVars:leptonPtRelInv"),
         leptonPtRelv0 = cms.InputTag("bJetVars:leptonPtRelv0"),
         leptonPtRatiov0 = cms.InputTag("bJetVars:leptonPtRatiov0"),
         leptonPtRelInvv0 = cms.InputTag("bJetVars:leptonPtRelInvv0"),
         leptonDeltaR = cms.InputTag("bJetVars:leptonDeltaR"),
         leptonPt = cms.InputTag("bJetVars:leptonPt"),
         vtxPt = cms.InputTag("bJetVars:vtxPt"),
         vtxMass = cms.InputTag("bJetVars:vtxMass"),
         vtx3dL = cms.InputTag("bJetVars:vtx3dL"),
         vtx3deL = cms.InputTag("bJetVars:vtx3deL"),
         ptD = cms.InputTag("bJetVars:ptD"),
         genPtwNu = cms.InputTag("bJetVars:genPtwNu"),
         ),
    userInts = cms.PSet(
        vtxNtrk = cms.InputTag("bJetVars:vtxNtrk"),
        leptonPdgId = cms.InputTag("bJetVars:leptonPdgId"),
    ),
)
bjetNN = bjetNN.clone(
    src = cms.InputTag("updatedJetsWithUserData"),
)
updatedJets = cms.EDProducer("PATJetUserDataEmbedder",
     src = cms.InputTag("updatedJetsWithUserData"),
     userFloats = cms.PSet(
         bJetRegCorr = cms.InputTag("bjetNN:corr"),
         bJetRegRes = cms.InputTag("bjetNN:res"),
         ),
)

BJetRegression = cms.Task()
BJetRegression.add(bJetVars)
BJetRegression.add(updatedJetsWithUserData)
BJetRegression.add(bjetNN)
BJetRegression.add(updatedJets)
