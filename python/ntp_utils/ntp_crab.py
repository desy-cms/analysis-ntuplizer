import os
import sys
import yaml
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

if not 'crab' in os.getenv('PYTHONPATH'):
   print(R+'It seems you did not initialised CRAB. You may need to issue the command below before continue'+W)
   print(Y+'source /cvmfs/cms.cern.ch/common/crab-setup.sh'+W)
   print('Also make sure you have a valid grid proxy')
   print(Y+'voms-proxy-init -rfc -valid 192:00 -voms cms:/cms/dcms'+W)
   sys.exit()


from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException
    
from Analysis.Ntuplizer.crabConfig import crabConfig
import subprocess

from ntp_common import ntp_common


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
      self.__process = common.dataset_alias()
      self.__datasets = common.datasets()
      self.__username = common.username()
      self.__mypath = '/store/user/'+self.__username
      self.__baseoutdir = self.__mypath+common.base_outdir()
      self.__configs = []
      for dataset, info in self.__datasets.iteritems():
         # get cross sections if available
         self.__configs.append(self.__crab_config(dataset,info))

   def __crab_config(self,dataset,info=None):
      dataset_pd = dataset.split('\n')[0]
      dataset_name = dataset_pd.split('/')[1]
      dataset_cond = dataset_pd.split('/')[2]
      config = crabConfig()
      config.General.workArea += '_' + self.__process        
      config.Data.outLFNDirBase   = self.__baseoutdir + '/'
      config.JobType.psetName = self.__opts.config             
      config.JobType.numCores = 4                       
      config.JobType.maxMemoryMB = 10000
      config.JobType.inputFiles = [self.__versiondir+'/trigger_info.yml']
      # Passing cmsRun parameters
      config.JobType.pyCfgParams = ["year="+str(self.__opts.year),"type="+self.__opts.type,"triggerInfo="+self.__versiondir+"/trigger_info.yml"]
      if info:
         for var,value in info.iteritems():
            if var=='xsection_pb':
               config.JobType.pyCfgParams += ["xsection="+str(value)]
      
      #######
      config.Data.inputDataset    = dataset_pd
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
         
         pyc = self.__opts.config+'c'
         if ".pyc" in pyc and os.path.exists(pyc):
            os.remove(pyc)
        
         proj_dir =cfg.General.workArea+"/crab_"+cfg.General.requestName
         crabCommand('submit',config=cfg)
         
         # ntuple_crab log file
         import subprocess
         cmd = ['crab', '--version']
         p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
         crab_version = p.stdout.read()
         if os.path.exists(proj_dir):
            with open(proj_dir+"/ntuple_crab.log","w") as f:
               f.write("DATASET = "+dataset+"\n")
               f.write("YEAR = "+str(self.__opts.year)+"\n")
               f.write("TYPE = "+self.__opts.type+"\n")
               f.write("VERSION = "+self.__opts.version+"\n")
               f.write("NTUPLES_REPO_DIR = "+self.__versiondir+"\n")
               f.write("TRIGGER_INFO = "+self.__versiondir+'/trigger_info.yml'+"\n")
               f.write("PYTHON_CONFIG = "+str(os.getcwd())+"/"+self.__opts.config+"\n")
               f.write("NTUPLES_OUTPUT = "+self.__baseoutdir+"\n")
               f.write("CMSSW_BASE = "+str(os.getenv('CMSSW_BASE'))+"\n")
               f.write("CMSSW_RELEASE_BASE = "+str(os.getenv('CMSSW_RELEASE_BASE'))+"\n")
               f.write("CRAB_VERSION = "+crab_version)
               
            # TO DO: put an ntuple_production.log file there
            #        should contain input parameter to crab submission
            #        year, dataset, version, config file, type
            print
         
         
      print(G+'=========================='+W)
      print
      if not opt=='debug' and not opt=='test':
         print('See your CRAB projects in crab_projects_'+self.__process)
