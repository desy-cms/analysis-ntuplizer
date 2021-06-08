# Analysis/Ntuplizer

Ntuple production for CMS data analysis

## Contents

* [RunII Legacy Production v5](#RunII-Legacy-Production-v5)
  * [Installation](#Installation)
  * [Execution](#Execution)
  * [Crab submission](#Crab-submission) 

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

### Execution

The CMSRun python configuration file used in this production is

[ntuplizer_106X_run2legacy_v5.py](/test/ntuplizer_106X_run2legacy_v5.py)

This configuration accepts parameters at the command line, e.g.

```bash
cmsRun ntuplizer_106X_run2legacy_v5.py \
       globalTag=106X_dataRun2_v33 \
       maxEvents=100 \
       year=2017 \
       type=data \
       inputFiles=/store/data/Run2017D/BTagCSV/MINIAOD/UL2017_MiniAODv2-v1/270000/3A3DF494-008A-1D49-9A95-0D9E334783A2.root \
       outputFile=ntuple.root \
       triggerInfo=/afs/desy.de/user/w/walsh/cms/ntuplizer/run2_ul/CMSSW_10_6_20/src/Analysis/Ntuplizer/data/ntuples/2017/v5/trigger_info.yml
```

It can also be executed with default parameters, which one can see in the configuration file, or from the output when running without passing any parameters
e.g.
```bash
cmsRun ntuplizer_106X_run2legacy_v5.py
```
yields in stdout
```
Python Configuration Options
----------------------------
globalTag         :  106X_dataRun2_v33
maxEvents         :  100
year              :  2017
type              :  data
inputFiles        :  ['/store/data/Run2017D/BTagCSV/MINIAOD/UL2017_MiniAODv2-v1/270000/3A3DF494-008A-1D49-9A95-0D9E334783A2.root']
outputFile        :  ntuple.root
triggerInfo       :  /afs/desy.de/user/w/walsh/cms/ntuplizer/run2_ul/CMSSW_10_6_20/src/Analysis/Ntuplizer/data/ntuples/2017/v5/trigger_info.yml
----------------------------
```
Notice that some parameters default values may depend on the year and type, e.g.
```bash
cmsRun ntuplizer_106X_run2legacy_v5.py year=2018 type=mc
```
has default parameters
```
Python Configuration Options
----------------------------
globalTag         :  106X_upgrade2018_realistic_v16_L1v1
maxEvents         :  100
year              :  2018
type              :  mc
xsection          :  -1.0
inputFiles        :  ['/store/mc/RunIISummer20UL18MiniAODv2/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/100000/01F9363E-5BB5-534B-AF6A-B771B601FFA3.root']
outputFile        :  ntuple.root
triggerInfo       :  /afs/desy.de/user/w/walsh/cms/ntuplizer/run2_ul/CMSSW_10_6_20/src/Analysis/Ntuplizer/data/ntuples/2018/v5/trigger_info.yml
----------------------------
```




