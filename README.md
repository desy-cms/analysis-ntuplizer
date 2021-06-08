# Analysis/Ntuplizer

Ntuple production for CMS data analysis

## Contents

* [RunII Legacy Production v5](#RunII-Legacy-Production-v5)

## RunII Legacy Production v5

### Installation

#### CMSSW

Recommended CMSSW release is CMSSW_10_6_X (X=20, maybe higher)

```bash
export SCRAM_ARCH='slc7_amd64_gcc700'
cmsrel CMSSW_10_6_20
cd CMSSW_10_6_20/src
cmsenv
```

#### Ntuplizer and Ntuples info

The resulting ntuples location as well as information used by the ntuplizer are stored in the analysis-ntuples repository (https://github.com/desy-cms/analysis-ntuples). Therefore it is required its installation. The directory structured must be followed.

```bash
cd $CMSSW_BASE/src
git clone https://github.com/desy-cms/analysis-ntuplizer Analysis/Ntuplizer
git clone https://github.com/desy-cms/analysis-ntuples Analysis/Ntuplizer/data/ntuples
scram b -j4
```

#### Configuration

The CMSRun python configuration file used in this production is

[ntuplizer_106X_run2legacy_v5.py](/test/ntuplizer_106X_run2legacy_v5.py)

