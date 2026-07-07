import FWCore.ParameterSet.Config as cms

from Analysis.Utils.config_utils import merge_vpsets

# https://btv-wiki.docs.cern.ch/ScaleFactors/#taggers-and-definitions-of-discriminators

# Also see: https://github.com/cms-sw/cmssw/blob/CMSSW_15_0_X/PhysicsTools/NanoAOD/python/jetsAK4_Puppi_cff.py


# Why these do not appear in the ntuple???
# pfParticleNetFromMiniAODAK4CHSCentralJetTags:probmu',
# pfParticleNetFromMiniAODAK4CHSCentralJetTags:probele',


AK4PFPuppi = {}
AK4PFPuppi['ParticleNet'] = cms.VPSet(
    cms.PSet(
        discriminator = cms.string('pfParticleNetFromMiniAODAK4PuppiCentralDiscriminatorsJetTags:BvsAll'),
        alias     = cms.string('btag_pnet_bvsall'),
    ),
    cms.PSet(
        discriminator = cms.string('pfParticleNetFromMiniAODAK4PuppiCentralDiscriminatorsJetTags:CvsL'),
        alias     = cms.string('btag_pnet_cvsl'),
    ),
    cms.PSet(
        discriminator = cms.string('pfParticleNetFromMiniAODAK4PuppiCentralDiscriminatorsJetTags:CvsB'),
        alias     = cms.string('btag_pnet_cvsb'),
    ),
    cms.PSet(
        discriminator = cms.string('pfParticleNetFromMiniAODAK4PuppiCentralJetTags:probb'),
        alias     = cms.string('btag_pnet_b'),
    ),
    cms.PSet(
        discriminator = cms.string('pfParticleNetFromMiniAODAK4PuppiCentralJetTags:probc'),
        alias     = cms.string('btag_pnet_c'),
    ),
    cms.PSet(
        discriminator = cms.string('pfParticleNetFromMiniAODAK4PuppiCentralJetTags:probg'),
        alias     = cms.string('btag_pnet_g'),
    ),
    cms.PSet(
        discriminator = cms.string('pfParticleNetFromMiniAODAK4PuppiCentralJetTags:probuds'),
        alias     = cms.string('btag_pnet_uds'),
    ),
)
AK4PFPuppi['ParticleTransformer'] = cms.VPSet(
    cms.PSet(
        discriminator = cms.string('pfParticleTransformerAK4JetTags:probb'),
        alias     = cms.string('btag_part_b'),
    ),
    cms.PSet(
        discriminator = cms.string('pfParticleTransformerAK4JetTags:probbb'),
        alias     = cms.string('btag_part_bb'),
    ),
    cms.PSet(
        discriminator = cms.string('pfParticleTransformerAK4JetTags:problepb'),
        alias     = cms.string('btag_part_lepb'),
    ),
    cms.PSet(
        discriminator = cms.string('pfParticleTransformerAK4JetTags:probc'),
        alias     = cms.string('btag_part_c'),
    ),
    cms.PSet(
        discriminator = cms.string('pfParticleTransformerAK4JetTags:probg'),
        alias     = cms.string('btag_part_g'),
    ),
    cms.PSet(
        discriminator = cms.string('pfParticleTransformerAK4JetTags:probuds'),
        alias     = cms.string('btag_part_uds'),
    ),
)
AK4PFPuppi['UnifiedParticleTransformer'] = cms.VPSet(
    cms.PSet(
        discriminator = cms.string('pfUnifiedParticleTransformerAK4DiscriminatorsJetTags:BvsAll'),
        alias     = cms.string('btag_upart_bvsall'),
    ),
    cms.PSet(
        discriminator = cms.string('pfUnifiedParticleTransformerAK4DiscriminatorsJetTags:CvsL'),
        alias     = cms.string('btag_upart_cvsl'),
    ),
    cms.PSet(
        discriminator = cms.string('pfUnifiedParticleTransformerAK4DiscriminatorsJetTags:CvsB'),
        alias     = cms.string('btag_upart_cvsb'),
    ),
    cms.PSet(
        discriminator = cms.string('pfUnifiedParticleTransformerAK4JetTags:probb'),
        alias     = cms.string('btag_upart_b'),
    ),
    cms.PSet(
        discriminator = cms.string('pfUnifiedParticleTransformerAK4JetTags:probbb'),
        alias     = cms.string('btag_upart_bb'),
    ),
    cms.PSet(
        discriminator = cms.string('pfUnifiedParticleTransformerAK4JetTags:problepb'),
        alias     = cms.string('btag_upart_lepb'),
    ),
    cms.PSet(
        discriminator = cms.string('pfUnifiedParticleTransformerAK4JetTags:probc'),
        alias     = cms.string('btag_upart_c'),
    ),
    cms.PSet(
        discriminator = cms.string('pfUnifiedParticleTransformerAK4JetTags:probg'),
        alias     = cms.string('btag_upart_g'),
    ),
    cms.PSet(
        discriminator = cms.string('pfUnifiedParticleTransformerAK4JetTags:probs'),
        alias     = cms.string('btag_upart_s'),
    ),
    cms.PSet(
        discriminator = cms.string('pfUnifiedParticleTransformerAK4JetTags:probd'),
        alias     = cms.string('btag_upart_d'),
    ),
    cms.PSet(
        discriminator = cms.string('pfUnifiedParticleTransformerAK4JetTags:probu'),
        alias     = cms.string('btag_upart_u'),
    ),
)
AK4PFPuppi['DeepFlavour'] = cms.VPSet(
    cms.PSet(
        discriminator = cms.string('pfDeepFlavourJetTags:probb'),
        alias     = cms.string('btag_deepflav_b'),
    ),
    cms.PSet(
        discriminator = cms.string('pfDeepFlavourJetTags:probbb'),
        alias     = cms.string('btag_deepflav_bb'),
    ),
    cms.PSet(
        discriminator = cms.string('pfDeepFlavourJetTags:problepb'),
        alias     = cms.string('btag_deepflav_lepb'),
    ),
    cms.PSet(
        discriminator = cms.string('pfDeepFlavourJetTags:probc'),
        alias     = cms.string('btag_deepflav_c'),
    ),
    cms.PSet(
        discriminator = cms.string('pfDeepFlavourJetTags:probg'),
        alias     = cms.string('btag_deepflav_g'),
    ),
    cms.PSet(
        discriminator = cms.string('pfDeepFlavourJetTags:probuds'),
        alias     = cms.string('btag_deepflav_uds'),
    ),        
)

# Provide a mapping so callers can access algorithms by jet type
BTagging = {
    'AK4PFPuppi': { 'ParticleNet': AK4PFPuppi['ParticleNet'],
                    'ParticleTransformer': AK4PFPuppi['ParticleTransformer'],
                    'UnifiedParticleTransformer': AK4PFPuppi['UnifiedParticleTransformer'],
                    'DeepFlavour': AK4PFPuppi['DeepFlavour'],
                  },
}

AllBTagging = {
    'AK4PFPuppi': merge_vpsets(
        AK4PFPuppi['ParticleNet'],
        AK4PFPuppi['ParticleTransformer'],
        AK4PFPuppi['UnifiedParticleTransformer'],
        AK4PFPuppi['DeepFlavour'],
    )
}