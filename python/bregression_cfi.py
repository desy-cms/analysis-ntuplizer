import FWCore.ParameterSet.Config as cms

# https://btv-wiki.docs.cern.ch/ScaleFactors/#taggers-and-definitions-of-discriminators

# Also see: https://github.com/cms-sw/cmssw/blob/CMSSW_15_0_X/PhysicsTools/NanoAOD/python/jetsAK4_Puppi_cff.py


BRegression_AK4PFPuppi = cms.PSet(
    BRegression = cms.VPSet(
        cms.PSet(
            discriminator = cms.string('pfParticleNetFromMiniAODAK4PuppiCentralJetTags:ptcorr'),
            alias     = cms.string('breg_pnet_ptcorr'),
        ),
        cms.PSet(
            discriminator = cms.string('pfParticleNetFromMiniAODAK4PuppiCentralJetTags:ptnu'),
            alias     = cms.string('breg_pnet_ptnu'),
        ),
        cms.PSet(
            discriminator = cms.string('pfParticleNetFromMiniAODAK4PuppiCentralJetTags:ptreshigh'),
            alias     = cms.string('breg_pnet_ptreshigh'),
        ),
        cms.PSet(
            discriminator = cms.string('pfParticleNetFromMiniAODAK4PuppiCentralJetTags:ptreslow'),
            alias     = cms.string('breg_pnet_ptreslow'),
        ),
        cms.PSet(
            discriminator = cms.string('pfParticleNetFromMiniAODAK4PuppiForwardJetTags:ptreshigh'),
            alias     = cms.string('breg_pnet_fw_ptreshigh'),
        ),
        cms.PSet(
            discriminator = cms.string('pfParticleNetFromMiniAODAK4PuppiForwardJetTags:ptreslow'),
            alias     = cms.string('breg_pnet_fw_ptreslow'),
        ),

        cms.PSet(
            discriminator = cms.string('pfUnifiedParticleTransformerAK4JetTags:ptcorr'),
            alias     = cms.string('breg_upart_ptcorr'),
        ),
        cms.PSet(
            discriminator = cms.string('pfUnifiedParticleTransformerAK4JetTags:ptnu'),
            alias     = cms.string('breg_upart_ptnu'),
        ),
        cms.PSet(
            discriminator = cms.string('pfUnifiedParticleTransformerAK4JetTags:ptreshigh'),
            alias     = cms.string('breg_upart_ptreshigh'),
        ),
        cms.PSet(
            discriminator = cms.string('pfUnifiedParticleTransformerAK4JetTags:ptreslow'),
            alias     = cms.string('breg_upart_ptreslow'),
        ),

        cms.PSet(
            discriminator = cms.string('pfUnifiedParticleTransformerAK4V1JetTags:ptcorr'),
            alias     = cms.string('breg_upartv1_ptcorr'),
        ),
        cms.PSet(
            discriminator = cms.string('pfUnifiedParticleTransformerAK4V1JetTags:ptnu'),
            alias     = cms.string('breg_upartv1_ptnu'),
        ),
        cms.PSet(
            discriminator = cms.string('pfUnifiedParticleTransformerAK4V1JetTags:ptreshigh'),
            alias     = cms.string('breg_upartv1_ptreshigh'),
        ),
        cms.PSet(
            discriminator = cms.string('pfUnifiedParticleTransformerAK4V1JetTags:ptreslow'),
            alias     = cms.string('breg_upartv1_ptreslow'),
        ),

    ),

)

# Provide a mapping so callers can access algorithms by jet type
BRegression = {
    'AK4PFPuppi': BRegression_AK4PFPuppi,
}


