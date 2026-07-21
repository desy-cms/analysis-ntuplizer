from __future__ import print_function
import os
import yaml

import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

def ntuplizer_parser(yml_file=None):

   cmssw_base = os.getenv("CMSSW_BASE")+'/'
   
   # command line options parsing
   command_line_parser = VarParsing.VarParsing()

   command_line_parser.register('maxEvents',
                 100,
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.int,
                  "maximum number of events")

   command_line_parser.register('globalTag',
                  '150X_dataRun3_v2',
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.string,
                  "condition global tag for the job (\"150X_dataRun3_v2\" is default)")
                  
   command_line_parser.register('year',
                  2024,
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.int,
                  "year of data taking")

   command_line_parser.register('type',
                  'data',
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.string,
                  "data or mc")

   command_line_parser.register('xsection',
                  -1.,
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.float,
                  "MC cross section")

   command_line_parser.register('triggerInfo',
                  '',
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.string,
                  "Trigger info")

   command_line_parser.register('outputFile',
                  "ntuple.root",
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.string,
                  "name for the output root file (\"ntuple.root\" is default)")

   command_line_parser.register('inputFiles',
                  '/store/data/Run2024G/JetMET0/MINIAOD/PromptReco-v1/000/385/801/00000/0302af56-b957-4ae2-a4a8-685177661997.root',
                  VarParsing.VarParsing.multiplicity.list,
                  VarParsing.VarParsing.varType.string,
                  "files to process")

   command_line_parser.register('json',
                  '',
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.string,
                  "JSON file (do not use with CRAB!)")

   command_line_parser.register('version',
                    None,
                    VarParsing.VarParsing.multiplicity.singleton,
                    VarParsing.VarParsing.varType.int,
                    "ntuple production version")

   command_line_parser.register('logReportEvery',
                  10000,
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.int,
                  "report every n events")

   command_line_parser.parseArguments()

   trigger_info = ''
   trigger_base_path = '' 
   if command_line_parser.version:
      # use the trigger from analysis-ntuples
      trigger_info='src/Analysis/Ntuplizer/data/ntuples/'+str(command_line_parser.year)+'/v'+str(command_line_parser.version)+'/trigger_info.yml'  
      trigger_base_path = "$CMSSW_BASE/"
   
   ##
   print('Python Configuration Options')
   print('----------------------------')
   print("version           : ", command_line_parser.version)
   print("year              : ", command_line_parser.year)
   print("type              : ", command_line_parser.type)
   print("globalTag         : ", command_line_parser.globalTag)
   print("triggerInfo       : ", trigger_base_path+trigger_info)
   print("inputFiles        : ", command_line_parser.inputFiles)
   print("outputFile        : ", command_line_parser.outputFile)
   print("maxEvents         : ", command_line_parser.maxEvents)
   if command_line_parser.type == 'mc':
      print("xsection          : ", command_line_parser.xsection)
   if command_line_parser.json:
      print("json              : ", command_line_parser.json)
   print("logReportEvery    : ", command_line_parser.logReportEvery)
   print('----------------------------')
   print

   if trigger_info:
      trigger_info=cmssw_base+trigger_info
      command_line_parser.setDefault('triggerInfo',trigger_info)
   
   return command_line_parser
