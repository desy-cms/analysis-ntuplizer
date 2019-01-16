#####  ERROR: This JEC level L1FastJet does not exist. 
#####  somehow the regression cannot undo the JEC correction for Puppi jets because it does not use L1 correction

import FWCore.ParameterSet.Config as cms

### ==== Regression ==== ####
bJetVarsPuppi = cms.EDProducer("JetRegressionVarProducer",
    pvsrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
    src = cms.InputTag("updatedPatJetsPuppiJetSpecific"),    
    svsrc = cms.InputTag("slimmedSecondaryVertices"),
    gpsrc = cms.InputTag("prunedGenParticles"),
    #musrc = cms.InputTag("slimmedMuons"),
    #elesrc = cms.InputTag("slimmedElectrons")
)

slimmedJetsPuppiWithUserData = cms.EDProducer("PATJetUserDataEmbedder",
     src = cms.InputTag("updatedPatJetsPuppiJetSpecific"),
     userFloats = cms.PSet(
         leadTrackPt = cms.InputTag("bJetVarsPuppi:leadTrackPt"),
         leptonPtRel = cms.InputTag("bJetVarsPuppi:leptonPtRel"),
         leptonPtRatio = cms.InputTag("bJetVarsPuppi:leptonPtRatio"),
         leptonPtRelInv = cms.InputTag("bJetVarsPuppi:leptonPtRelInv"),
         leptonPtRelv0 = cms.InputTag("bJetVarsPuppi:leptonPtRelv0"),
         leptonPtRatiov0 = cms.InputTag("bJetVarsPuppi:leptonPtRatiov0"),
         leptonPtRelInvv0 = cms.InputTag("bJetVarsPuppi:leptonPtRelInvv0"),
         leptonDeltaR = cms.InputTag("bJetVarsPuppi:leptonDeltaR"),
         leptonPt = cms.InputTag("bJetVarsPuppi:leptonPt"),
         vtxPt = cms.InputTag("bJetVarsPuppi:vtxPt"),
         vtxMass = cms.InputTag("bJetVarsPuppi:vtxMass"),
         vtx3dL = cms.InputTag("bJetVarsPuppi:vtx3dL"),
         vtx3deL = cms.InputTag("bJetVarsPuppi:vtx3deL"),
         ptD = cms.InputTag("bJetVarsPuppi:ptD"),
         genPtwNu = cms.InputTag("bJetVarsPuppi:genPtwNu"),
         
         ),
     userInts = cms.PSet(
        vtxNtrk = cms.InputTag("bJetVarsPuppi:vtxNtrk"),
        leptonPdgId = cms.InputTag("bJetVarsPuppi:leptonPdgId"),
     ),
)

bjetNNPuppi = cms.EDProducer("BJetEnergyRegressionMVA",
    backend = cms.string("TF"),
    src = cms.InputTag("slimmedJetsPuppiWithUserData"),
    pvsrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
    svsrc = cms.InputTag("slimmedSecondaryVertices"),
    rhosrc = cms.InputTag("fixedGridRhoFastjetAll"),

    weightFile =  cms.FileInPath("PhysicsTools/NanoAOD/data/breg_training_2017.pb"),
    name = cms.string("JetRegNN"),
    isClassifier = cms.bool(False),
    variablesOrder = cms.vstring(["Jet_pt","Jet_eta","rho","Jet_mt","Jet_leadTrackPt","Jet_leptonPtRel","Jet_leptonDeltaR","Jet_neHEF","Jet_neEmEF","Jet_vtxPt","Jet_vtxMass","Jet_vtx3dL","Jet_vtxNtrk","Jet_vtx3deL","Jet_numDaughters_pt03","Jet_energyRing_dR0_em_Jet_rawEnergy","Jet_energyRing_dR1_em_Jet_rawEnergy","Jet_energyRing_dR2_em_Jet_rawEnergy","Jet_energyRing_dR3_em_Jet_rawEnergy","Jet_energyRing_dR4_em_Jet_rawEnergy","Jet_energyRing_dR0_neut_Jet_rawEnergy","Jet_energyRing_dR1_neut_Jet_rawEnergy","Jet_energyRing_dR2_neut_Jet_rawEnergy","Jet_energyRing_dR3_neut_Jet_rawEnergy","Jet_energyRing_dR4_neut_Jet_rawEnergy","Jet_energyRing_dR0_ch_Jet_rawEnergy","Jet_energyRing_dR1_ch_Jet_rawEnergy","Jet_energyRing_dR2_ch_Jet_rawEnergy","Jet_energyRing_dR3_ch_Jet_rawEnergy","Jet_energyRing_dR4_ch_Jet_rawEnergy","Jet_energyRing_dR0_mu_Jet_rawEnergy","Jet_energyRing_dR1_mu_Jet_rawEnergy","Jet_energyRing_dR2_mu_Jet_rawEnergy","Jet_energyRing_dR3_mu_Jet_rawEnergy","Jet_energyRing_dR4_mu_Jet_rawEnergy","Jet_chHEF","Jet_chEmEF","Jet_leptonPtRelInv","isEle","isMu","isOther","Jet_mass","Jet_ptd"]),
    variables = cms.PSet(
    Jet_pt = cms.string("pt*jecFactor('Uncorrected')"),
    Jet_mt = cms.string("mt*jecFactor('Uncorrected')"),
    Jet_eta = cms.string("eta"),
    Jet_mass = cms.string("mass*jecFactor('Uncorrected')"),
    Jet_ptd = cms.string("userFloat('ptD')"),
    Jet_leadTrackPt = cms.string("userFloat('leadTrackPt')"),
    Jet_vtxNtrk = cms.string("userInt('vtxNtrk')"),
    Jet_vtxMass = cms.string("userFloat('vtxMass')"),
    Jet_vtx3dL = cms.string("userFloat('vtx3dL')"),
    Jet_vtx3deL = cms.string("userFloat('vtx3deL')"),
    Jet_vtxPt = cms.string("userFloat('vtxPt')"),
    #Jet_leptonPt = cms.string("userFloat('leptonPt')"),
    Jet_leptonPtRel = cms.string("userFloat('leptonPtRelv0')"),
    Jet_leptonPtRelInv = cms.string("userFloat('leptonPtRelInvv0')*jecFactor('Uncorrected')"),
    Jet_leptonDeltaR = cms.string("userFloat('leptonDeltaR')"),
    #Jet_leptonPdgId = cms.string("userInt('leptonPdgId')"),
    Jet_neHEF = cms.string("neutralHadronEnergyFraction()"),
    Jet_neEmEF = cms.string("neutralEmEnergyFraction()"),
    Jet_chHEF = cms.string("chargedHadronEnergyFraction()"),
    Jet_chEmEF = cms.string("chargedEmEnergyFraction()"),
    isMu = cms.string("?abs(userInt('leptonPdgId'))==13?1:0"),
    isEle = cms.string("?abs(userInt('leptonPdgId'))==11?1:0"),
    isOther = cms.string("?userInt('leptonPdgId')==0?1:0"),
    ),
     inputTensorName = cms.string("ffwd_inp"),
     outputTensorName = cms.string("ffwd_out/BiasAdd"),
     outputNames = cms.vstring(["corr","res"]),
     outputFormulas = cms.vstring(["at(0)*0.28492164611816406+1.0596693754196167","0.5*(at(2)-at(1))*0.28492164611816406"]),
     nThreads = cms.uint32(1),
     singleThreadPool = cms.string("no_threads"),
)

slimmedJetsPuppiWithUserDataWithReg = cms.EDProducer("PATJetUserDataEmbedder",
     src = cms.InputTag("slimmedJetsPuppiWithUserData"),
     userFloats = cms.PSet(
         bJetRegCorr = cms.InputTag("bjetNNPuppi:corr"),
         bJetRegRes = cms.InputTag("bjetNNPuppi:res"),
         ),
)

BJetRegressionPuppi = cms.Task()
BJetRegressionPuppi.add(bJetVarsPuppi)
BJetRegressionPuppi.add(slimmedJetsPuppiWithUserData)
BJetRegressionPuppi.add(bjetNNPuppi)
BJetRegressionPuppi.add(slimmedJetsPuppiWithUserDataWithReg)



