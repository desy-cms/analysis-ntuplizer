# Given a json file with the trigger information
# Set the parameters for the trigger results filter
# and for the Ntuplizer.
# 4 PSet objects are returned in a meaningful dict

import FWCore.ParameterSet.Config as cms

import os
import yaml

def triggerInfo(info_file):
   info = dict()
   triggerConditions = cms.vstring()     # paths trigger results filter
   triggerPaths = cms.vstring()          # paths for the ntuplizer
   l1Seeds = cms.vstring()               # l1 seeds for the ntuplizer
   triggerObjects = cms.vstring()        # trigger objects for the ntuplizer
   trgObjL1MuJet = cms.vstring()
   trgObjL1MuJetType = cms.vstring()
   
   if os.path.isfile(info_file):
      with open(info_file) as f:
         info_data = yaml.safe_load(f)
      for path, path_info in sorted(info_data.items()):
         p = str(path).strip()
         p = "_".join(p.split("_")[:-1])+"_v" # remove version
         # remove path duplicates
         if not p in triggerPaths:
            triggerPaths.append(p)
            triggerConditions.append(p+'*')
         l1s = info_data[path]['l1seeds']
         for l1 in sorted(l1s):
            if l1 == '':
               continue
            l1str = str(l1).strip()
            #remove l1 seed duplicates
            if not l1str in l1Seeds:  
               l1Seeds.append(l1str)
         objs = info_data[path]['trigger_objects']
         for obj in sorted(objs):
            if obj == '':
               continue
            objstr = str(obj).strip()
            # remove trigger object duplicates
            if not objstr in triggerObjects:
               triggerObjects.append(objstr)
               if 'hltL1' in objstr and 'Mu' in objstr and 'Jet' in objstr:
                  trgObjL1MuJet.append(objstr)
                  trgObjL1MuJetType.append('l1muon:l1jet')
   else:
      print '>>>>>>>> Msg-W: The given YAML file with trigger info does not exist <<<<<<<<'
      print ''
      
   # sort lists
   triggerPaths.sort()
   triggerConditions.sort()
   l1Seeds.sort()  
   triggerObjects.sort()
   
   triggerResultsFilter = cms.PSet(triggerConditions = triggerConditions)
   ntuplizerTriggerPaths = cms.PSet(TriggerPaths = triggerPaths)
   ntuplizerL1Seeds = cms.PSet(L1Seeds = l1Seeds)
   ntuplizerTriggerObjects = cms.PSet(TriggerObjectLabels = triggerObjects, 
       TriggerObjectSplits = trgObjL1MuJet,
       TriggerObjectSplitsTypes = trgObjL1MuJetType)
   info['triggerResultsFilter']=triggerResultsFilter
   info['ntuplizerTriggerPaths']=ntuplizerTriggerPaths
   info['ntuplizerL1Seeds']=ntuplizerL1Seeds
   info['ntuplizerTriggerObjects']=ntuplizerTriggerObjects
   return info
