import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.Config as cms

btagAlgorithms = cms.PSet(
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
    ),
)


