#!/usr/bin/env python

import os.path
import urllib2
import sys
from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import getUsernameFromSiteDB

# colors
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple


ARGSN = len(sys.argv)
if ARGSN < 3:
   print (R+"You need to provide the CMSSW python config, the samples list file and optionally the json in this order"+W)
   sys.exit()

# ---
# Some parameter steering
RUN_RANGE       = ''
UNITS_PER_JOB   = 50
TYPE            = 'DATA'
CAMPAIGN        = 'Run2016/80x_triggerstudies17_run2016hv1_raw_userv37'

ARGS = sys.argv
PSET = ARGS[1]
SAMPLE = ARGS[2]
JSON = ''
if ARGSN == 4:
   JSON = ARGS[3]

psetname, pset_ext = os.path.splitext(PSET)
samplename, sample_ext = os.path.splitext(SAMPLE)

if not ( os.path.isfile(PSET) and pset_ext == '.py' ):
   print (R+"The given python config does not exist or it is not a python file"+W)
   sys.exit()

if not ( os.path.isfile(SAMPLE) and sample_ext == '.txt' ):
   print (R+"The given sample list file does not exist or it is not a txt file"+W)
   sys.exit()

# Some parameter steering
PROCESS         = samplename.split('/')[-1]
MYPATH          = '/store/user/%s/' % (getUsernameFromSiteDB())
BASEOUTDIR      = MYPATH+'Analysis/Ntuples/' + TYPE + '/' + CAMPAIGN

dataset_list    = 'samples/data/' + PROCESS + '.txt'
f_datasets = open(dataset_list,'r')
datasets = f_datasets.readlines()

# colors
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple

# _________________________________________________________________________

if __name__ == '__main__':

   from CRABAPI.RawCommand import crabCommand
   from CRABClient.ClientExceptions import ClientException
   from httplib import HTTPException
    
   from Analysis.Ntuplizer.crabConfig import crabConfig
   config = crabConfig()

# ====== GENERAL
   config.General.workArea += '_' + PROCESS
   config.General.transferLogs = False

# ====== DATA   
   config.Data.splitting   = 'LumiBased'
   config.Data.unitsPerJob  = UNITS_PER_JOB
   config.Data.totalUnits   = -1
   config.Data.outLFNDirBase   = BASEOUTDIR + '/'
   if JSON != '':
      config.Data.lumiMask = JSON
#   config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader/'
#   config.Data.allowNonValidInputDataset = True    # If dataset not valid yet, will run over valid files only
   if RUN_RANGE != '':
      config.Data.runRange = RUN_RANGE


# ====== JOBTYPE
   config.JobType.psetName    = PSET
#   config.JobType.inputFiles = ['Fall15_25nsV2_DATA_PtResolution_AK4PFPuppi.txt','Fall15_25nsV2_DATA_PtResolution_AK4PFchs.txt','Fall15_25nsV2_DATA_SF_AK4PFPuppi.txt','Fall15_25nsV2_DATA_SF_AK4PFchs.txt']
   config.JobType.numCores    = 4
   
   for dataset in datasets:
      dataset = dataset.split('\n')[0]
      dataset_name = dataset.split('/')[1]
      dataset_cond = dataset.split('/')[2]
      dataset_tier = dataset.split('/')[3]
#      
      config.Data.inputDataset    = dataset
      config.Data.outputDatasetTag = dataset_cond
#      
      config.General.requestName  = dataset_name
      config.General.requestName += '_'+dataset_cond
      if RUN_RANGE != '':
         config.General.requestName += '_'+RUN_RANGE
      
      outtext = "Submitting dataset " + dataset + "..."
      print (O+str(outtext)+W) 
#      
      crabCommand('submit', config = config)
      print (O+"--------------------------------"+W)
      print

# _________________________________________________________________________
