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
         p = str(path)
         triggerPaths.append(p)
         triggerConditions.append(p+'*')
         l1s = info_data[path]['l1seeds']
         for l1 in sorted(l1s):
            if l1 == '':
               continue
            l1Seeds.append(str(l1))
         objs = info_data[path]['trigger_objects']
         for obj in objs:
            if obj == '':
               continue
            triggerObjects.append(str(obj))
            if 'hltL1' in obj and 'Mu' in obj and 'Jet' in obj:
               trgObjL1MuJet.append(str(obj))
               trgObjL1MuJetType.append('l1muon:l1jet')
   else:
      print '>>>>>>>> Msg-W: The given YAML file with trigger info does not exist <<<<<<<<'
      print ''
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
