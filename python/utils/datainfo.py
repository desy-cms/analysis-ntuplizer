import os
import sys
import yaml
from glob import glob
from Analysis.Ntuplizer.utils.datacommon import DataCommon
#from colors import tcolors
from Analysis.Ntuplizer.utils.colors import tcolors

W  = tcolors.W
R  = tcolors.R
G  = tcolors.G
O  = tcolors.O
B  = tcolors.B
C  = tcolors.C
Y  = tcolors.Y
BOLD = tcolors.BOLD
UNDERLINE = tcolors.UNDERLINE


# Class for ntuples production info
# (not sure this is way for the constructor is a good way)
class DataInfo:
   def __init__(self,opts):
      self.__common = DataCommon(opts)
      self.__opts = opts
      
   def print_info(self):
      if not self.__opts.version:
         self.__common.print_versions()
         return
      if not self.__opts.dataset:  
         self.__common.print_datasets_lists()
         return 
      if len(self.__common.datasets_lists()) == 0:
         print(R+'No dataset list available'+W)
         return 
      self.__common.print_datasets()
      
      return
      
