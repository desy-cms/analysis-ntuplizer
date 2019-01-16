import FWCore.ParameterSet.Config as cms

MssmHbbNtuplizerBtagHLT = cms.PSet(
    BTagAlgorithms = cms.vstring   (
                'pfCombinedInclusiveSecondaryVertexV2BJetTags',
                'pfJetProbabilityBJetTags',
                'pfCombinedMVAV2BJetTags',
                'pfDeepCSVJetTags:probudsg',
                'pfDeepCSVJetTags:probb',
                'pfDeepCSVJetTags:probc',
                'pfDeepCSVJetTags:probbb',
                'pfDeepCSVJetTags:probcc',
                'pfDeepCMVAJetTags:probudsg',
                'pfDeepCMVAJetTags:probb',
                'pfDeepCMVAJetTags:probc',
                'pfDeepCMVAJetTags:probbb',
                'pfDeepCMVAJetTags:probcc'    
    ),
    BTagAlgorithmsAlias = cms.vstring   (
                'btag_csvivf',
                'btag_jetprob',
                'btag_csvmva',
                'btag_deeplight',
                'btag_deepb',
                'btag_deepc',
                'btag_deepbb',
                'btag_deepcc',
                'btag_deepmvalight',
                'btag_deepmvab',
                'btag_deepmvac',
                'btag_deepmvabb',
                'btag_deepmvacc',
    ),
)
