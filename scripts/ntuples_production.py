#!/usr/bin/env python3
import os
import sys

from Analysis.Ntuplizer.ntp_utils.ntp_parser import ntp_parser
from Analysis.Ntuplizer.ntp_utils.ntp_info import ntp_info
from Analysis.Ntuplizer.ntp_utils.ntp_crab import ntp_crab 


# -----
def main():

   # input options
   opts, unknown = ntp_parser()
   
   if opts.which == 'info':
      info = ntp_info(opts)
      info.print_info()
   
   if opts.which == 'crab':
      crab = ntp_crab(opts) 
      crab.submit()
      sys.exit()
   
# _________________________________________________________________________



if __name__ == '__main__':
   main()

