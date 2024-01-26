#!/usr/bin/env python3
import os
import sys

from Analysis.Ntuplizer.utils.crab_parser import crab_parser
from Analysis.Ntuplizer.utils.crabjob import CrabJob 
from Analysis.Ntuplizer.utils.datainfo import DataInfo


# -----
def main():

   # input options
   my_name = os.path.basename(__file__)
   opts, unknown = crab_parser(my_name)
   
   if opts.which == 'info':
      data_info = DataInfo(opts)
      data_info.print_info()
   
   if opts.which == 'crab':
      crab_job = CrabJob(opts) 
      crab_job.submit()
      sys.exit()
   
# _________________________________________________________________________



if __name__ == '__main__':
   main()

