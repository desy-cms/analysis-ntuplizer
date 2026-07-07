import FWCore.ParameterSet.Config as cms

PNet_AK4PFPuppi = cms.VPSet(
    cms.PSet(
        discriminator = cms.string('testParticleNetFromMiniAODAK4PuppiCentralDiscriminatorsJetTags:BvsAll'),
        alias     = cms.string('test_pnet_bvsall'),
    ),
    cms.PSet(
        discriminator = cms.string('testParticleNetFromMiniAODAK4PuppiCentralDiscriminatorsJetTags:CvsL'),
        alias     = cms.string('test_pnet_cvsl'),
    ),
    cms.PSet(
        discriminator = cms.string('testParticleNetFromMiniAODAK4PuppiCentralDiscriminatorsJetTags:CvsB'),
        alias     = cms.string('test_pnet_cvsb'),
    ),
    cms.PSet(
        discriminator = cms.string('testParticleNetFromMiniAODAK4PuppiCentralJetTags:probb'),
        alias     = cms.string('test_pnet_b'),
    ),
    cms.PSet(
        discriminator = cms.string('testParticleNetFromMiniAODAK4PuppiCentralJetTags:probc'),
        alias     = cms.string('test_pnet_c'),
    ),
    cms.PSet(
        discriminator = cms.string('testParticleNetFromMiniAODAK4PuppiCentralJetTags:probg'),
        alias     = cms.string('test_pnet_g'),
    ),
    cms.PSet(
        discriminator = cms.string('testParticleNetFromMiniAODAK4PuppiCentralJetTags:probuds'),
        alias     = cms.string('test_pnet_uds'),
    ),
)
ParT_AK4PFPuppi = cms.VPSet(
    cms.PSet(
        discriminator = cms.string('testParticleTransformerAK4JetTags:probb'),
        alias     = cms.string('test_part_b'),
    ),
    cms.PSet(
        discriminator = cms.string('testParticleTransformerAK4JetTags:probbb'),
        alias     = cms.string('test_part_bb'),
    ),
    cms.PSet(
        discriminator = cms.string('testParticleTransformerAK4JetTags:problepb'),
        alias     = cms.string('test_part_lepb'),
    ),
    cms.PSet(
        discriminator = cms.string('testParticleTransformerAK4JetTags:probc'),
        alias     = cms.string('test_part_c'),
    ),
    cms.PSet(
        discriminator = cms.string('testParticleTransformerAK4JetTags:probg'),
        alias     = cms.string('test_part_g'),
    ),
    cms.PSet(
        discriminator = cms.string('testParticleTransformerAK4JetTags:probuds'),
        alias     = cms.string('test_part_uds'),
    ),
)

# Provide a mapping so callers can access algorithms by jet type
Testing = {
    'AK4PFPuppi': { 'ParticleNet': PNet_AK4PFPuppi,
                    'ParticleTransformer': ParT_AK4PFPuppi
                  },
}


