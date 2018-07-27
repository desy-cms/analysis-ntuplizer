import FWCore.ParameterSet.Config as cms

MssmHbbNtuplizerBtag = cms.PSet(
    BTagAlgorithms = cms.vstring   (
                'pfCombinedInclusiveSecondaryVertexV2BJetTags',
                'pfJetProbabilityBJetTags',
                'pfDeepCSVJetTags:probudsg',
                'pfDeepCSVJetTags:probb',
                'pfDeepCSVJetTags:probc',
                'pfDeepCSVJetTags:probbb',
                'pfDeepCSVJetTags:probcc',
                'pfDeepCSVDiscriminatorsJetTags:BvsAll',
    ),
    BTagAlgorithmsAlias = cms.vstring   (
                'btag_csvivf',
                'btag_jetprob',
                'btag_deeplight',
                'btag_deepb',
                'btag_deepc',
                'btag_deepbb',
                'btag_deepcc',
                'btag_deepbvsall',
    ),
)
