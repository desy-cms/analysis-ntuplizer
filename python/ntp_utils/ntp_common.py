import os
import sys
import yaml
from glob import glob
from colors import tcolors
import subprocess

W  = tcolors.W
R  = tcolors.R
G  = tcolors.G
O  = tcolors.O
B  = tcolors.B
C  = tcolors.C
Y  = tcolors.Y
BOLD = tcolors.BOLD
UNDERLINE = tcolors.UNDERLINE

class ntp_common:
   def __init__(self,opts):
      self.__opts = opts
      self.__ntuplesdir = self.__ntuples_dir()
      self.__versions = self.__get_versions()
      self.__versiondir = self.__version_dir()
      self.__datasetdir = self.__dataset_dir()
      self.__datasetyml = self.__dataset_yaml()
      self.__datasetsdict = self.__datasets_dict()
      self.__datasetalias = self.dataset_alias()
      self.__pyconfig = self.__python_config()

   def dataset_alias(self):
      if not self.__opts.dataset.startswith('/'):
         return self.__opts.dataset
      dsa = ''
      for alias,datasets in self.__datasetsdict.iteritems():
         for dataset,values in datasets.iteritems():
            if dataset == self.__opts.dataset:
               # get the alias of the existing dataset block
               dsa = alias
               # alter dictionary content
               content = self.__datasetsdict[alias][dataset]
               self.__datasetsdict = {alias:{dataset:content}}
               break
         if dsa:
            break
      
      if not dsa:
         print(R+'The given dataset has no entry in '+W)
         print(Y+self.__datasetyml+W)      
         sys.exit()
      return dsa
      
      
   def __ntuples_dir(self):
      nd  = os.getenv('CMSSW_BASE')+'/src/Analysis/Ntuplizer/data/ntuples/'+self.__opts.year
      if not os.path.exists(nd):
         print(R+'ERROR: Please check the given year'+W)
         sys.exit()
      return nd

   def __python_config(self):
      pc = ''
      if self.__opts.which != 'crab':
         return pc
      if self.__opts.config:
         if not os.path.exists(self.__opts.config):
            print(R+'ERROR: Configuration files does not exist'+W)
            sys.exit()
         else:
            pc = self.__opts.config
      return pc
      
   def python_config(self):
      return self.__pyconfig
         
   def __version_dir(self):
      vd = ''
      if self.__opts.version:
         vd = self.__ntuplesdir+'/v'+self.__opts.version
      if not os.path.exists(vd):
         print(R+'ERROR: Please check your version'+W)
         self.print_versions()
         sys.exit()
      return vd
         
   def __dataset_dir(self):
      dd = ''
      if self.__opts.version:
         dd = self.__ntuplesdir+'/v'+self.__opts.version+'/'+self.__opts.type
      return dd
         
   def __dataset_yaml(self):
      dy = ''
      if self.__datasetdir:
         dy = self.__datasetdir+'/datasets.yml'
      return dy

   def options(self):
      return  self.__opts
        
   def ntuples_dir(self):
      return self.__ntuplesdir
      
   def version_dir(self):
      return self.__versiondir
      
   def dataset_dir(self):
      return self.__datasetdir
    
   def dataset_yaml(self):
      return self.__datasetyml
    
   def versions(self):
      return self.__versions
          
   def datasets_lists(self):
      return sorted(self.__datasetsdict.keys())
      
   def datasets(self):
      ds = ''
      if len(self.__datasetsdict) > 0 and self.__datasetalias in self.__datasetsdict:
         ds = self.__datasetsdict[self.__datasetalias]
      else:
         print(R+'ERROR: Please check the name of your dataset list'+W)
         self.print_datasets_lists()
         sys.exit()
      return ds
      
   def __get_versions(self):
      vs = glob(self.__ntuplesdir+'/v*')
      vs = [os.path.basename(v) for v in vs]
      vs = [int(v.replace("v","",1)) for v in vs]
      vs.sort()
      vs = [str(v) for v in vs]
      return vs
   
   def __datasets_dict(self):
      dss = {}
      if not self.__datasetyml:
         return dss
      version = self.__versions[-1] if self.__opts.version<0 else self.__opts.version
      with open(self.__datasetyml) as f:
         dss = yaml.load(f, Loader=yaml.FullLoader)
      if len(dss)==0:
         print('No list of datasets available')
         return
      return dss
      
   def print_versions(self):
      print('Available versions')
      for v in self.__versions:
         print(' -> '+v)
         
   def print_datasets_lists(self):
      print('Available lists of datasets')
      dss = self.datasets_lists()
      for ds in dss:
         print(' -> '+C+ds+W)
      self.print_yaml()

   def print_datasets(self):
      ds = self.datasets()
      if len(ds) < 1:
         return
      print('Available datasets in the list')
      print(' -> '+C+self.__datasetalias+W)
      for dataset,info in ds.iteritems():
         print('     - '+G+dataset+W)
         if not info:
            continue
         for var, value in info.iteritems():
            print('       * ' + var + ' = ' +str(value))
      self.print_yaml()

   def print_yaml(self):
      print('Info from file: ')
      print(Y+self.__datasetyml+W)

   def username(self):
      checkusername = subprocess.Popen(['crab', 'checkusername'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      stdout,stderr = checkusername.communicate()
      return stdout.split('Username is: ')[1].rstrip()
      
   def base_outdir(self):
      bo = ''
      if self.python_config():
         bo = '/Analysis/Ntuples/'+self.__opts.type.upper()+'/Run'+self.__opts.year+'-v'+str(self.__opts.version)+'/'+os.path.basename(self.__pyconfig).split('.py')[0]
      return bo
