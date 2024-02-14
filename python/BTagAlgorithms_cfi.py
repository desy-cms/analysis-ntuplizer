import FWCore.ParameterSet.Config as cms

# Why these do not appear in the ntuple???
# pfParticleNetFromMiniAODAK4CHSCentralJetTags:probmu',
# pfParticleNetFromMiniAODAK4CHSCentralJetTags:probele',

BTagAlgorithms_AK4CHS = cms.PSet(
    BTagAlgorithms = cms.vstring   (
                'pfDeepCSVJetTags:probudsg',
                'pfDeepCSVJetTags:probc',
                'pfDeepCSVJetTags:probcc',
                'pfDeepCSVJetTags:probb',
                'pfDeepCSVJetTags:probbb',
                'pfDeepFlavourJetTags:probuds',
                'pfDeepFlavourJetTags:probg',                
                'pfDeepFlavourJetTags:probc',
                'pfDeepFlavourJetTags:probb',
                'pfDeepFlavourJetTags:probbb',
                'pfDeepFlavourJetTags:problepb',
                'pfParticleNetFromMiniAODAK4CHSCentralJetTags:probb',
                'pfParticleNetFromMiniAODAK4CHSCentralJetTags:probc',
                'pfParticleNetFromMiniAODAK4CHSCentralJetTags:probuds',
                'pfParticleNetFromMiniAODAK4CHSCentralJetTags:probg',
                'pfParticleNetFromMiniAODAK4CHSCentralJetTags:probmu',
                'pfParticleNetFromMiniAODAK4CHSCentralJetTags:probele',
    ),
    BTagAlgorithmsAlias = cms.vstring   (
                'btag_deepcsv_light',
                'btag_deepcsv_c',
                'btag_deepcsv_cc',
                'btag_deepcsv_b',
                'btag_deepcsv_bb',
                'btag_deepjet_flight',
                'btag_deepjet_g',
                'btag_deepjet_c',
                'btag_deepjet_b',
                'btag_deepjet_bb',
                'btag_deepjet_lepb',
                'btag_pnet_b',
                'btag_pnet_c',
                'btag_pnet_uds',
                'btag_pnet_g',
                'btag_pnet_mu',
                'btag_pnet_ele',
    ),
)

BTagAlgorithms_AK4Puppi = cms.PSet(
    BTagAlgorithms = cms.vstring   (
                'pfParticleNetFromMiniAODAK4PuppiCentralJetTags:probb',
                'pfParticleNetFromMiniAODAK4PuppiCentralJetTags:probc',
                'pfParticleNetFromMiniAODAK4PuppiCentralJetTags:probuds',
                'pfParticleNetFromMiniAODAK4PuppiCentralJetTags:probg',
                'pfParticleNetFromMiniAODAK4PuppiCentralJetTags:probmu',
                'pfParticleNetFromMiniAODAK4PuppiCentralJetTags:probele',
    ),
    BTagAlgorithmsAlias = cms.vstring   (
                'btag_pnet_b',
                'btag_pnet_c',
                'btag_pnet_uds',
                'btag_pnet_g',
                'btag_pnet_mu',
                'btag_pnet_ele',
    ),
)


