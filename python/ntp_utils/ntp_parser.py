
from argparse import ArgumentParser
from argparse import HelpFormatter

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


def ntp_parser():
   idesc = G+'*** '+UNDERLINE
   fdesc = W+G+' ***'+W
   options = ArgumentParser(prog='submit_crab.py', \
      formatter_class=lambda prog: HelpFormatter(prog,indent_increment=6,max_help_position=80,width=280), \
      description=idesc+'Ntuple Production Script (CRAB)'+fdesc, \
      epilog=Y+'NB: requires the installation of https://github.com/desy-cms/analysis-ntuples in Analysis/Ntuplizer/data/ntuples'+W,\
      add_help=True)
   options._optionals.title = Y+'optional'+W
   options._positionals.title = Y+'mandatory arguments'+W
   
   # suboptions
   suboptions = options.add_subparsers()
   
   ## suboption production
   crab_opt = suboptions.add_parser('crab',\
                         description=idesc+'Ntuple Production with CRAB '+fdesc,\
                         help='ntuple production via crab')
   crab_opt._optionals.title = Y+'optional'+W
   crab_opt.set_defaults(which='crab')   
   
   crab_req = crab_opt.add_argument_group(Y+'mandatory'+W)
   crab_req.add_argument("-t"  , dest="type"    , required=True  , choices={"data", "mc"}  , help=R+"type of sample"+W)
   crab_req.add_argument("-c"  , dest="config"  , required=True                       , help=R+"python configuration file"+W)
   crab_req.add_argument("-d"  , dest="dataset" , required=True                       , help=R+"name of file with list of datasets"+W)
#   crab_req.add_argument("-l"  , dest="label"   , required=True                       , help=R+"a label, e.g. Legacy"+W)
   crab_req.add_argument("-v"  , dest="version" , required=True                       , help=R+"production version"+W)
   crab_req.add_argument("-y"  , dest="year"    , required=True                       , help=R+"data taking year"+W)
   crab_opt.add_argument("-n"  , dest="units"                    , type=int           , help=C+"number of units per job/events"+W)
   crab_opt.add_argument("-r"  , dest="run_range"                                     , help=C+"run range (e.g. 193093-193999,198050,199564)"+W)
   crab_opt.add_argument("-j"  , dest="lumi_mask"                                     , help=C+"URL address or the path to a JSON file on disk."+W)

   ## suboption info
   info_opt = suboptions.add_parser('info',\
                         description=idesc+'Ntuples Information'+fdesc,\
                         help='display available info for submission')
   info_opt._optionals.title = Y+'optional'+W
   info_opt.set_defaults(which='info')   
   info_req = info_opt.add_argument_group(Y+'mandatory'+W)
   info_req.add_argument("-y"  , dest="year"    , required=True                      , help=R+"data taking year"+W)
   info_req.add_argument("-t"  , dest="type"    , required=True  , choices={"data", "mc"}  , help=R+"type of sample"+W)
   info_opt.add_argument("-v"  , dest="version"                                      , help=C+"production version (latest = -1)"+W)
   info_opt.add_argument("-d"  , dest="dataset"                                      , help=C+"list of datasets"+W)

   return options.parse_known_args()
   



