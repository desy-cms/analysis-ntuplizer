## Python configuration
### b-tagging and regression algorithms
To enable all the algorithms decalred in `btagging_cfi.py` and `bregression_cfi.py` in the ntuplizer use
```python
from Analysis.Ntuplizer.btagging_cfi import BTagging, AllBTagging
from Analysis.Ntuplizer.bregression_cfi import BRegression, AllBRegression

## Ntuplizer
process.MssmHbb                 = cms.EDAnalyzer('Ntuplizer',
    BTagging                    = AllBTagging['AK4PFPuppi'],
    BRegression                 = AllBRegression['AK4PFPuppi'],
```
If only some of the algorithms are to be enabled do the following:
```python
from Analysis.Ntuplizer.btagging_cfi import BTagging, AllBTagging
from Analysis.Ntuplizer.bregression_cfi import BRegression, AllBRegression

# Selection of the b-tagging algorithms to be used in the ntuplizer, or use AllBTagging to include all of them (see the ntuplizer below)
BTaggingAlgos = {}
BTaggingAlgos['AK4PFPuppi'] = cms.VPSet()
BTaggingAlgos['AK4PFPuppi'].extend(BTagging['AK4PFPuppi']['ParticleNet'])
BTaggingAlgos['AK4PFPuppi'].extend(BTagging['AK4PFPuppi']['UnifiedParticleTransformer'])

# Selection of the b-regression algorithms to be used in the ntuplizer, or use AllBRegression to include all of them (see the ntuplizer below)
BRegressionAlgos = {}
BRegressionAlgos['AK4PFPuppi'] = cms.VPSet()
BRegressionAlgos['AK4PFPuppi'].extend(BRegression['AK4PFPuppi']['ParticleNet'])

## Ntuplizer
process.MssmHbb                 = cms.EDAnalyzer('Ntuplizer',
    BTagging                    = BTaggingAlgos['AK4PFPuppi'],
    BRegression                 = BRegressionAlgos['AK4PFPuppi'],
```

