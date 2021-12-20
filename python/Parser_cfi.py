from __future__ import print_function
import os

import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

def parser(yml_file=None):

   cmssw_base = os.getenv("CMSSW_BASE")
   
   # command line options parsing
   options = VarParsing.VarParsing()

   options.register('maxEvents',
                    100,
                    VarParsing.VarParsing.multiplicity.singleton,
                    VarParsing.VarParsing.varType.int,
                    "maximum number of events")

   options.register('globalTag',
                    '',
                    VarParsing.VarParsing.multiplicity.singleton,
                    VarParsing.VarParsing.varType.string,
                    "condition global tag for the job (\"auto:run2_data\" is default)")
                    
   options.register('year',
                    2017,
                    VarParsing.VarParsing.multiplicity.singleton,
                    VarParsing.VarParsing.varType.int,
                    "year of data taking")

   options.register('type',
                    'data',
                    VarParsing.VarParsing.multiplicity.singleton,
                    VarParsing.VarParsing.varType.string,
                    "data or mc")

   options.register('xsection',
                    -1.,
                    VarParsing.VarParsing.multiplicity.singleton,
                    VarParsing.VarParsing.varType.float,
                    "MC cross section")

   options.register('triggerInfo',
                    '',
                    VarParsing.VarParsing.multiplicity.singleton,
                    VarParsing.VarParsing.varType.string,
                    "Trigger info")

   options.register('outputFile',
                    "ntuple.root",
                    VarParsing.VarParsing.multiplicity.singleton,
                    VarParsing.VarParsing.varType.string,
                    "name for the output root file (\"ntuple.root\" is default)")

   options.register('inputFiles',
                    '',
                    VarParsing.VarParsing.multiplicity.list,
                    VarParsing.VarParsing.varType.string,
                    "files to process")

   options.register('json',
                    'oioi.json',
                    VarParsing.VarParsing.multiplicity.singleton,
                    VarParsing.VarParsing.varType.string,
                    "JSON file (do not use with CRAB!)")

   options.register('version',
                    '',
                    VarParsing.VarParsing.multiplicity.singleton,
                    VarParsing.VarParsing.varType.int,
                    "ntuple production version")

   options.parseArguments()
   
   # default inputFiles (examples)
   input_files = {}
   input_files['data']= {}
   input_files['data'][2017]='/store/data/Run2017D/BTagCSV/MINIAOD/UL2017_MiniAODv2-v1/270000/3A3DF494-008A-1D49-9A95-0D9E334783A2.root'
   input_files['data'][2018]='/store/data/Run2018D/JetHT/MINIAOD/UL2018_MiniAODv2-v1/270000/0DEEC71E-980C-F945-8DB6-7CC0CFE862E2.root'
   input_files['mc']= {}
   input_files['mc'][2017]='/store/mc/RunIISummer20UL17MiniAODv2/SUSYGluGluToBBHToBB_M-450_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/2530000/5CD3FBB6-127F-9E45-B291-F5C40117D617.root'
   input_files['mc'][2018]='/store/mc/RunIISummer20UL18MiniAODv2/QCD_bEnriched_HT300to500_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/120000/30FC1268-ABED-4140-95F0-0E1416F826D9.root'

   # default triggerInfo
   trigger_info = {}
   trigger_info[2017]=cmssw_base+'/src/Analysis/Ntuplizer/data/ntuples/2017/v6/trigger_info.yml'
   trigger_info[2018]=cmssw_base+'/src/Analysis/Ntuplizer/data/ntuples/2018/v6/trigger_info.yml'


   # default globaTag
   global_tag = {}
   global_tag['data'] = {2017:'106X_dataRun2_v35'        , 2018:'106X_dataRun2_v35'}
   global_tag['mc']   = {2017:'106X_mc2017_realistic_v9' , 2018:'106X_upgrade2018_realistic_v16_L1v1'}

   # set defaults
   if not options.inputFiles:
      options.setDefault('inputFiles',input_files[options.type][options.year])
   if not options.globalTag:
      options.setDefault('globalTag',global_tag[options.type][options.year])
   if not options.triggerInfo:
      options.setDefault('triggerInfo',trigger_info[options.year])


   ##
   print('Python Configuration Options')
   print('----------------------------')
   print("version           : ", options.version)
   print("year              : ", options.year)
   print("type              : ", options.type)
   print("globalTag         : ", options.globalTag)
   print("triggerInfo       : ", options.triggerInfo)
   print("inputFiles        : ", options.inputFiles)
   print("outputFile        : ", options.outputFile)
   print("maxEvents         : ", options.maxEvents)
   if options.type == 'mc':
      print("xsection          : ", options.xsection)
   if options.json:
      print("json              : ", options.json)
   print('----------------------------')
   print


   
   return options
