from __future__ import print_function
import os
import yaml

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
                    '',
                    VarParsing.VarParsing.multiplicity.singleton,
                    VarParsing.VarParsing.varType.string,
                    "JSON file (do not use with CRAB!)")

   options.register('version',
                    '',
                    VarParsing.VarParsing.multiplicity.singleton,
                    VarParsing.VarParsing.varType.int,
                    "ntuple production version")

   options.parseArguments()
   
   ## default_info.yml
   input_files = []
   global_tag = ''
   def_info = cmssw_base+'/src/Analysis/Ntuplizer/data/ntuples/'+str(options.year)+'/v'+str(options.version)+'/default_info.yml'
   with open(def_info) as f:
      def_info_data = yaml.safe_load(f)
   for dttype,info in def_info_data.items():
      if dttype != options.type:
         continue
      input_files = info['input_files']
      global_tag = info['global_tag'][0]
   trigger_info=cmssw_base+'/src/Analysis/Ntuplizer/data/ntuples/'+str(options.year)+'/v'+str(options.version)+'/trigger_info.yml'  
   
   # set defaults
   if not options.inputFiles:
      options.setDefault('inputFiles',input_files)
   if not options.globalTag:
      options.setDefault('globalTag',global_tag)
   if not options.triggerInfo:
      options.setDefault('triggerInfo',trigger_info)


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
