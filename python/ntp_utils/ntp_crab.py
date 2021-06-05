import os
import sys
import yaml
from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException
    
from Analysis.Ntuplizer.crabConfig import crabConfig
import subprocess

from ntp_common import ntp_common

from colors import tcolors
W  = tcolors.W
R  = tcolors.R
G  = tcolors.G
O  = tcolors.O
B  = tcolors.B
C  = tcolors.C
Y  = tcolors.Y
BOLD = tcolors.BOLD
UNDERLINE = tcolors.UNDERLINE

def short_requestname(reqname):
   new_reqname = ''
   for sub in reqname.split('_'):
      sublow = sub.lower()
      if 'tune' in sublow or 'tev' in sublow or 'pythia' in sublow or 'realistic' in sublow:
         continue
      new_reqname += sub+'_'
   return new_reqname[:-1]


# Class for ntuples production crab submission
# (not sure this is way for the constructor is a good way)
class ntp_crab:
   def __init__(self,opts):
      common = ntp_common(opts)
      self.__opts = opts
      self.__basedir = common.ntuples_dir()
      self.__datasetdir = common.dataset_dir()
      self.__versiondir = common.version_dir()
      self.__versions = common.versions()
      self.__dataset_yaml = common.dataset_yaml()
      self.__datasetslists = common.datasets_lists()
      self.__datasets = common.datasets()
      self.__pyconfig = common.python_config()
      self.__process = opts.dataset
      self.__datasets = common.datasets()
      self.__username = common.username()
      self.__mypath = '/store/user/'+self.__username
      self.__baseoutdir = self.__mypath+common.base_outdir()
      self.__configs = []
      for dataset, info in self.__datasets.iteritems():
         # get cross sections if available
         self.__configs.append(self.__crab_config(dataset,info))

   def __crab_config(self,dataset,info=None):
      config = crabConfig()
      config.General.workArea += '_' + self.__process        
      config.Data.outLFNDirBase   = self.__baseoutdir + '/'
      config.JobType.psetName = self.__opts.config             
      config.JobType.numCores = 4                       
      config.JobType.maxMemoryMB = 10000
      config.JobType.inputFiles = [self.__versiondir+'/trigger_info.yml']
      config.JobType.pyCfgParams = ["year="+str(self.__opts.year),"type="+self.__opts.type]
      if info:
         for var,value in info.iteritems():
            if var=='xsection_pb':
               config.JobType.pyCfgParams += ["xsection="+str(value)]
      
      #######
      dataset = dataset.split('\n')[0]
      dataset_name = dataset.split('/')[1]
      dataset_cond = dataset.split('/')[2]
      config.Data.inputDataset    = dataset
      config.Data.outputDatasetTag = dataset_cond
      req_name = dataset_name+ '_'+dataset_cond
      # Long request names, usually MC
      if self.__opts.type == 'mc':
         req_name = short_requestname(req_name)
      config.General.requestName  = req_name
      return config

   def __crab_dataset(self,config):
      return config.Data.inputDataset
      


   def submit(self,opt=''):
      print
      print(G+'Running crab submission...'+W)
      print(G+'=========================='+W)
      for cfg in self.__configs:
         dataset = self.__crab_dataset(cfg)
         outtext = " * Submitting dataset " + dataset + "..."
         print (Y+str(outtext)+W) 
         
         if opt=='dryrun':
            if self.__opts.type == 'mc':
               cfg.Data.splitting = 'FileBased'
               cfg.Data.unitsPerJob = 10
            else:
               cfg.Data.splitting = 'LumiBased'
               cfg.Data.unitsPerJob = 2
            cmd ='--dryrun'
            crabCommand('submit', config = cfg, *cmd.split())
            continue
         if opt=='debug' or opt=='test':
            print(' *** Running on '+opt+' mode. Nothing will be done ***'+W)
            continue
         
         crabCommand('submit',config=cfg)
         
      print(G+'=========================='+W)
      print
      if not opt=='debug' and not opt=='test':
         print('See your CRAB projects in crab_projects_'+self.__opts.dataset)
