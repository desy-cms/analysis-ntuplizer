import FWCore.ParameterSet.Config as cms

MssmHbbNtuplizerBtag = cms.PSet(
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
    ),
    BTagAlgorithmsAlias = cms.vstring   (
                'btag_deeplight',
                'btag_deepc',
                'btag_deepcc',
                'btag_deepb',
                'btag_deepbb',
                'btag_dflight',
                'btag_dfg',
                'btag_dfc',
                'btag_dfb',
                'btag_dfbb',
                'btag_dflepb',
    ),
)
