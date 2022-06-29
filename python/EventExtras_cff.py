import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Modifier_run2_jme_2016_cff import run2_jme_2016
from Configuration.Eras.Modifier_run2_jme_2017_cff import run2_jme_2017

## L1 Prefiring
### https://twiki.cern.ch/twiki/bin/viewauth/CMS/L1PrefiringWeightRecipe
from PhysicsTools.PatUtils.l1PrefiringWeightProducer_cfi import l1PrefiringWeightProducer
prefiringweight = l1PrefiringWeightProducer.clone(
TheJets = cms.InputTag("updatedPatJets"), #this should be the slimmedJets collection with up to date JECs
DataEraECAL = cms.string("None"), #Use 2016BtoH for 2016
DataEraMuon = cms.string("20172018"), #Use 2016 for 2016
UseJetEMPt = cms.bool(False),
PrefiringRateSystematicUnctyECAL = cms.double(0.2),
PrefiringRateSystematicUnctyMuon = cms.double(0.2)
)

run2_jme_2017.toModify(prefiringweight,
                DataEraECAL = cms.string("2017BtoF"),
)


EventExtras = cms.Task()
EventExtras.add(prefiringweight)
