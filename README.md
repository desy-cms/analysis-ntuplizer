# Installation

On an SLC6 machine

```bash
export SCRAM_ARCH='slc6_amd64_gcc700'
cmsrel CMSSW_10_2_22
cd CMSSW_10_2_22/src
cmsenv
git cms-init
```

## b-jet energy regression

*The branch **cms-nanoAOD:master-102X** has already been <u>fully merged</u> to **CMSSM_10_2_X**. The actions below are not needed. It will be kept for history.*
See [here](https://github.com/robervalwalsh/cmssw/compare/from-CMSSW_10_2_22-ntuplizer_2018_v3...cms-nanoAOD:master-102X) and [here](https://github.com/cms-sw/cmssw/compare/CMSSW_10_2_X...cms-nanoAOD:master-102X)

Last revision before UL: [Revision 55](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD?rev=55#Recipe_for_the_current_HEAD_of_N)

```bash
git cms-merge-topic cms-nanoAOD:master-102X
git checkout -b from-CMSSW_10_2_22_nanoAODrev55 cms-nanoAOD/master-102X
```
Optional
```bash
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
```

## Ntuplizer

```bash
git clone git@github.com:robervalwalsh/analysis-ntuplizer.git Analysis/Ntuplizer
cd Analysis/Ntuplizer
git checkout develop
git checkout -b develop-2018-v3
```

## Configuration

### Data

| Era  | Config  | GlobalTag  |
|---|---|---|
| ReReco17Sep 2018ABC  | [ntuplizer_102X_2018_rereco17Sep2018ABC-v3.py](test/ntuplizer_102X_2018_rereco17Sep2018ABC-v3.py)  | 102X_dataRun2_v12 |
| PromptReco 2018D     | [ntuplizer_102X_2018_promptreco2018D-v3.py](test/ntuplizer_102X_2018_promptreco2018D-v3.py)     | 102X_dataRun2_Prompt_v15 |

### Monte Carlo
| Campaign  | Config  | GlobalTag  |
|---|---|---|
| Autumn 2018  | [ntuplizer_102X_mc_2018_autumn18-v3.py](test/ntuplizer_102X_mc_2018_autumn18-v3.py)  | 102X_upgrade2018_realistic_v20 |
