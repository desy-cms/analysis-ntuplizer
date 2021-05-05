import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Modifier_run2_jme_2016_cff import run2_jme_2016
from Configuration.Eras.Modifier_run2_jme_2017_cff import run2_jme_2017

ntuplizerBTag = cms.PSet(
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

run2_jme_2017.toModify(ntuplizerBTag,
                BTagAlgorithms = ntuplizerBTag.BTagAlgorithms + cms.vstring   (
                'pfCombinedInclusiveSecondaryVertexV2BJetTags',
                'pfJetProbabilityBJetTags',
    )
)

    
run2_jme_2017.toModify(ntuplizerBTag,
                BTagAlgorithmsAlias = ntuplizerBTag.BTagAlgorithmsAlias + cms.vstring   (
                'btag_csvivf',
                'btag_jetprob',
    )
)
    
