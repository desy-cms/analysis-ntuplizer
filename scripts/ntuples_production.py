#!/usr/bin/env python2
import os
import sys

from Analysis.Ntuplizer.ntp_utils import ntp_parser
from Analysis.Ntuplizer.ntp_utils import ntp_info
from Analysis.Ntuplizer.ntp_utils import ntp_crab 


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

