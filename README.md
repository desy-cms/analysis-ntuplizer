# Analysis/Ntuplizer

Ntuple production for CMS data analysis

## Contents

* [RunII Legacy Production v6](#RunII-Legacy-Production-v6)
  * [Cheat sheet](#Cheat-sheet)
  * [Installation](#Installation)
  * [Execution](#Execution)
  * [CRAB submission](#CRAB-submission) 

## RunII Legacy Production v6

**For ntuple production of years 2017 and 2018**

:warning: 08.06.2021: The trigger information for the year 2018 is not ready yet. For the moment, please only run on 2017 data and monte carlo

:warning: 08.06.2021: Not all MINIAODv2 samples are ready for monte carlo, therefore the `datasets.yml` files are incomplete

### Cheat sheet

Before running make sure you did the [installation](#Installation).

#### crab submission (cs)

Don't forget to initialise crab and get a valid grid proxy

```bash
source /cvmfs/cms.cern.ch/common/crab-setup.sh
voms-proxy-init -rfc -valid 192:00 -voms cms:/cms/dcms
```

E.g., submitting BTagCSV 2017 datasets for ntuple production version 6

```bash
cd $CMSSW_BASE/src/Analysis/Ntuplizer/test
ntuples_production.py crab -y 2017 -t data -v 6 -d BTagCSV_UL2017 -c ntuplizer_106X_run2legacy.py
```
For other datasets, option `-d`, see the `datasets.yml` files in [analysis-ntuples](https://github.com/desy-cms/analysis-ntuples), e.g. for 2017, production v6
- [datasets.yml for data](https://github.com/desy-cms/analysis-ntuples/blob/master/2017/v6/data/datasets.yml)
- [datasets.yml for monte carlo](https://github.com/desy-cms/analysis-ntuples/blob/master/2017/v6/mc/datasets.yml)

#### preparing rootFileList.txt (cs)

Search for all directories like `crab_projects_<name>` in the `test` directory. List all directories inside `crab_projects_<name>`. Then run the `rootfilelist.py` script for each crab job. E.g.

```bash
rootfilelist.py crab_projects_BTagCSV_UL2017/crab_BTagCSV_Run2017C-UL2017_MiniAODv2-v1
```

### Installation

#### CMSSW

Recommended CMSSW release is CMSSW_10_6_29

```bash
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_6_29
cd CMSSW_10_6_29/src
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

[ntuplizer_106X_run2legacy.py](/test/ntuplizer_106X_run2legacy.py)

This configuration accepts parameters at the command line, e.g.

```bash
cmsRun ntuplizer_106X_run2legacy.py \
       version=6 \
       globalTag=106X_dataRun2_v35 \
       maxEvents=100 \
       year=2017 \
       type=data \
       inputFiles=/store/data/Run2017D/BTagCSV/MINIAOD/UL2017_MiniAODv2-v1/270000/3A3DF494-008A-1D49-9A95-0D9E334783A2.root \
       outputFile=ntuple.root \
       triggerInfo=/afs/desy.de/user/w/walsh/cms/ntuplizer/run2_ul/CMSSW_10_6_29/src/Analysis/Ntuplizer/data/ntuples/2017/v6/trigger_info.yml
```

It can also be executed with default parameters, which one can see in the configuration file, or from the output when running without passing any parameters
e.g.

⚠️ `version` is a required parameter!!! ⚠️

```bash
cmsRun ntuplizer_106X_run2legacy.py version=6
```

yields in stdout
```
Python Configuration Options
----------------------------
version           :  6
globalTag         :  106X_dataRun2_v35
maxEvents         :  100
year              :  2017
type              :  data
inputFiles        :  ['/store/data/Run2017D/BTagCSV/MINIAOD/UL2017_MiniAODv2-v1/270000/3A3DF494-008A-1D49-9A95-0D9E334783A2.root']
outputFile        :  ntuple.root
triggerInfo       :  /afs/desy.de/user/w/walsh/cms/ntuplizer/run2_ul/CMSSW_10_6_20/src/Analysis/Ntuplizer/data/ntuples/2017/v6/trigger_info.yml
----------------------------
```
Notice that some parameters default values, such as `inputFiles`, `globalTag` and `triggerInfo`, may depend on the given `version`, `year` and `type`, e.g.
```bash
cmsRun ntuplizer_106X_run2legacy.py version=6 year=2018 type=mc
```
has default parameters
```
Python Configuration Options
----------------------------
version           :  6
globalTag         :  106X_upgrade2018_realistic_v16_L1v1
maxEvents         :  100
year              :  2018
type              :  mc
xsection          :  -1.0
inputFiles        :  ['/store/mc/RunIISummer20UL18MiniAODv2/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/100000/01F9363E-5BB5-534B-AF6A-B771B601FFA3.root']
outputFile        :  ntuple.root
triggerInfo       :  /afs/desy.de/user/w/walsh/cms/ntuplizer/run2_ul/CMSSW_10_6_20/src/Analysis/Ntuplizer/data/ntuples/2018/v6/trigger_info.yml
----------------------------
```

### CRAB submission

Before any crab submission don't forget to initialise crab and get a valid grid proxy

```bash
source /cvmfs/cms.cern.ch/common/crab-setup.sh
voms-proxy-init -rfc -valid 192:00 -voms cms:/cms/dcms
```

The user should go to the directory where the cmsRun python configuration is located.
```bash
cd $CMSSW_BASE/src/Analysis/Ntuplizer/test
```

#### Information on parameters to be parsed to crab submission

To know which samples(*) are available the user can run the script below giving a few parameters, such as year (`-y`), type (`-t`), version (`-v`)
```bash
ntuples_production.py info -y 2017 -t data -v 6
```
(*) a sample is a block of primary datasets

With the information given by the command above, one can list the primary datasets in each sample
```bash
ntuples_production.py info -y 2017 -t data -v 6 -d BTagCSV_UL2017
```
which yields
```
Available datasets in the list
 -> BTagCSV_UL2017
     - /BTagCSV/Run2017C-UL2017_MiniAODv2-v1/MINIAOD
     - /BTagCSV/Run2017F-UL2017_MiniAODv2-v1/MINIAOD
     - /BTagCSV/Run2017D-UL2017_MiniAODv2-v1/MINIAOD
     - /BTagCSV/Run2017E-UL2017_MiniAODv2-v1/MINIAOD
Info from file: 
$CMSSW_BASE/src/Analysis/Ntuplizer/data/ntuples/2017/v6/data/datasets.yml
```
The samples and datasets can also be found in the yaml files in [analysis-ntuples](https://github.com/desy-cms/analysis-ntuples), e.g. for 2017, production v6
- [datasets.yml for data](https://github.com/desy-cms/analysis-ntuples/blob/master/2017/v6/data/datasets.yml)
- [datasets.yml for monte carlo](https://github.com/desy-cms/analysis-ntuples/blob/master/2017/v6/mc/datasets.yml)


#### Submitting to CRAB

The crab submission script is the same as above, but instead of `info` the user must use `crab` as first argument and give the cmsRun python configuration file to be used via option `-c`, e.g.
```bash
ntuples_production.py crab -y 2017 -t data -v 6 -d BTagCSV_UL2017 -c ntuplizer_106X_run2legacy.py
```
Jobs for all the datasets in `BTagCSV_UL2017` will be created.

The `-d` option also accepts a single dataset, e.g. `/BTagCSV/Run2017C-UL2017_MiniAODv2-v1/MINIAOD`. Thus, the script will submit a single dataset.

The command will create a directory called `crab_projects_BTagCSV_UL2017`. Inside it there will be crab directories for the all datasets submitted to crab. Those crab directories are the ones that are used when using crab tools, e.g. checking the crab status for BTagCSV 2017C dataset 
```bash
cd crab_projects_BTagCSV_UL2017
crab status -d crab_BTagCSV_Run2017C-UL2017_MiniAODv2-v1
``` 

#### Retrieving information from submission

A script called `rootfilelist.py` accepts a crab directory as parameter. It will run the `crab report` command and retrieve information from it and the `crab.log` file located inside that directory. The main information are the so-called rootFileList.txt files that contain the paths to the ntuples used in the analysis. That information is automatically copied into the analysis-ntuples directories.

The example below will prepare everything for the example above for you
```bash
cd $CMSSW_BASE/src/Analysis/Ntuplizer
rootfilelist.py test/crab_projects_BTagCSV_UL2017/crab_BTagCSV_Run2017C-UL2017_MiniAODv2-v1
```
You will find the `BTagCSV_Run2017C_rootFileList.txt` in
```bash
cd data/ntuples/2017/v6/data
``` 
where a directory with `additional_info` contains information produced by crab.


:warning: The user should commit those files and directories to a branch in the user's forked repository and make a pull request to be merged to the central repository.

