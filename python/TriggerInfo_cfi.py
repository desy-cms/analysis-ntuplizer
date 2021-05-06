# Given a json file with the trigger information
# Set the parameters for the trigger results filter
# and for the Ntuplizer.
# 4 PSet objects are returned in a meaningful dict

import FWCore.ParameterSet.Config as cms

import os
import json

def triggerInfo(info_file):
   info = dict()
   triggerConditions = cms.vstring()     # paths trigger results filter
   triggerPaths = cms.vstring()          # paths for the ntuplizer
   l1Seeds = cms.vstring()               # l1 seeds for the ntuplizer
   triggerObjects = cms.vstring()        # trigger objects for the ntuplizer
   
   if os.path.isfile(info_file):
      with open(info_file) as f:
         info_data = json.load(f)
      for path, path_info in sorted(info_data.items()):
         p = str(path)
         triggerPaths.append(p)
         triggerConditions.append(p+'*')
         l1s = info_data[path]['l1seeds']
         for l1 in sorted(l1s):
            if l1 == '':
               continue
            l1Seeds.append(str(l1))
         objs = info_data[path]['trgobjs']
         for obj in objs:
            if obj == '':
               continue
            triggerObjects.append(str(obj))
   else:
      print '>>>>>>>> Msg-W: The given JSON file with trigger info does not exist <<<<<<<<'
      print ''
   triggerResultsFilter = cms.PSet(triggerConditions = triggerConditions)
   ntuplizerTriggerPaths = cms.PSet(TriggerPaths = triggerPaths)
   ntuplizerL1Seeds = cms.PSet(L1Seeds = l1Seeds)
   ntuplizerTriggerObjects = cms.PSet(TriggerObjectLabels = triggerObjects)
   info['triggerResultsFilter']=triggerResultsFilter
   info['ntuplizerTriggerPaths']=ntuplizerTriggerPaths
   info['ntuplizerL1Seeds']=ntuplizerL1Seeds
   info['ntuplizerTriggerObjects']=ntuplizerTriggerObjects
   return info
