from __future__ import print_function
import os
import yaml

import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

def parser(yml_file=None):

   cmssw_base = os.getenv("CMSSW_BASE")+'/'
   
   # command line options parsing
   options = VarParsing.VarParsing()

   options.register('maxEvents',
                  100,
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.int,
                  "maximum number of events")

   options.register('globalTag',
                  '130X_dataRun3_PromptAnalysis_v1',
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.string,
                  "condition global tag for the job (\"130X_dataRun3_PromptAnalysis_v1\" is default)")
                  
   options.register('year',
                  2023,
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
                  '/store/data/Run2023D/JetMET0/MINIAOD/22Sep2023_v2-v1/2540000/012f384f-443c-4ba1-af3e-86d5ef25afc8.root',
                  VarParsing.VarParsing.multiplicity.list,
                  VarParsing.VarParsing.varType.string,
                  "files to process")

   options.register('json',
                  '',
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.string,
                  "JSON file (do not use with CRAB!)")

   options.register('version',
                    '1',
                    VarParsing.VarParsing.multiplicity.singleton,
                    VarParsing.VarParsing.varType.int,
                    "ntuple production version")

   options.parseArguments()

   trigger_info = ''
   trigger_base_path = '' 
   if options.version:
      # use the trigger from analysis-ntuples
      trigger_info='src/Analysis/Ntuplizer/data/ntuples/'+str(options.year)+'/v'+str(options.version)+'/trigger_info.yml'  
      trigger_base_path = "$CMSSW_BASE/"
   
   ##
   print('Python Configuration Options')
   print('----------------------------')
   print("version           : ", options.version)
   print("year              : ", options.year)
   print("type              : ", options.type)
   print("globalTag         : ", options.globalTag)
   print("triggerInfo       : ", trigger_base_path+trigger_info)
   print("inputFiles        : ", options.inputFiles)
   print("outputFile        : ", options.outputFile)
   print("maxEvents         : ", options.maxEvents)
   if options.type == 'mc':
      print("xsection          : ", options.xsection)
   if options.json:
      print("json              : ", options.json)
   print('----------------------------')
   print

   if trigger_info:
      trigger_info=cmssw_base+trigger_info
      options.setDefault('triggerInfo',trigger_info)
   
   return options
