import FWCore.ParameterSet.Config as cms

from PhysicsTools.NanoAOD.jets_cff import bJetVars,updatedJetsWithUserData,bjetNN,looseJetId,tightJetId,tightJetIdLepVeto

looseJetId = looseJetId.clone(
    src = cms.InputTag("updatedPatJets"),    
)
tightJetId = tightJetId.clone(
    src = cms.InputTag("updatedPatJets"),    
)
tightJetIdLepVeto = tightJetIdLepVeto.clone(
    src = cms.InputTag("updatedPatJets"),    
)

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
        looseId = cms.InputTag("looseJetId"),
        tightId = cms.InputTag("tightJetId"),
        tightIdLepVeto = cms.InputTag("tightJetIdLepVeto"),
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

JetWithUserData = cms.Task()
JetWithUserData.add(looseJetId)
JetWithUserData.add(tightJetId)
JetWithUserData.add(tightJetIdLepVeto)
JetWithUserData.add(bJetVars)
JetWithUserData.add(updatedJetsWithUserData)
JetWithUserData.add(bjetNN)
JetWithUserData.add(updatedJets)
