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
                'pfDeepFlavourJetTags:probuds',
                'pfDeepFlavourJetTags:probg',                
                'pfDeepFlavourJetTags:probc',
                'pfDeepFlavourJetTags:probb',
                'pfDeepFlavourJetTags:probbb',
                'pfDeepFlavourJetTags:problepb',
    ),
    BTagAlgorithmsAlias = cms.vstring   (
                'btag_csvivf',
                'btag_jetprob',
                'btag_deeplight',
                'btag_deepb',
                'btag_deepc',
                'btag_deepbb',
                'btag_deepcc',
                'btag_dflight',
                'btag_dfg',
                'btag_dfc',
                'btag_dfb',
                'btag_dfbb',
                'btag_dflepb',
    ),
)
