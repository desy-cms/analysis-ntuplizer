#!/usr/bin/env python3


# hlt_paths.txt is a file whose lines contain each the name of
# the HLT paths the will go into the trigger_info.yml
# User will be asked to give the configuration of the trigger menu
# The configuration file containing the menu should be put in
# Analysis/Ntuplizer/python

import re
import sys
import importlib

from pathlib import Path

# 
def processing(process,hlt_path_nov):
   output = ''
   # get all paths in the menu configuration
   path_names = process.pathNames().split(" ")
   path_names = [x for x in path_names if x.startswith("HLT_")]

   hlt_paths = [x for x in path_names if x.startswith(hlt_path_nov)]
   if not hlt_paths:
      print("WARNING: "+hlt_path_nov+" not in this menu! Skipping!")
      return output
   hlt_path = hlt_paths[0]
   # cms path
   cms_path = eval("process."+hlt_path+".dumpPythonNoNewline()")
   # remove cms.Path
   cms_path = cms_path[9:-1]
   cms_path_modules = cms_path.split("+")
   #ignored modules
   ignored_modules = [ x for x in cms_path_modules if "ignore" in x]
   ignored_modules = [re.search('\(([^)]+)',ig).group(1) for ig in ignored_modules]
   
   # all process modules
   process_modules = eval("process."+hlt_path+".moduleNames()")
   
   # trigger objects and L1 seeds of the path
   trg_objs = []
   for mod_name  in process_modules:
      mod = eval("process."+mod_name+".dumpPython()")
      # HLT EDFilters with saveTags - trigger objects
      if not 'EDFilter' in mod or not 'saveTags' in mod or str("process."+mod_name) in ignored_modules:
         continue
      mod_pars = mod.split("\n")
      save_tags = [x for x in mod_pars if "saveTags" in x][0].lstrip()
      if not "True" in save_tags:
         continue
      trg_objs.append(mod_name)
      # Find L1 seeds
      if not "HLTL1TSeed" in mod:
         continue
      l1_par = [x for x in mod_pars if "L1SeedsLogicalExpression" in x][0]
      l1_par = re.search('\(([^)]+)',l1_par).group(1).replace("'","")
      if " AND " in l1_par:
         print("WARNING: 'AND' logic for L1! Skipping!")
         continue
      l1_seeds = l1_par.split(" OR ")
   
   # Preserving the path modules order
   trg_objs_order = []
   for pm in cms_path_modules:
      pmo = pm.replace("process.","")
      if pmo in trg_objs:
         trg_objs_order.append(pmo)
   if not trg_objs_order:
      print("WARNING: no trigger object in the cms.Path for path "+hlt_path_nov)
      return output
         
   trg_objs = trg_objs_order
   
   # prepare output
   output += hlt_path+":\n"
   output += " l1seeds:\n"
   for l1s in l1_seeds:
      output += " - "+l1s+"\n"
   output += " trigger_objects:\n"
   for to in trg_objs:
      output += " - "+to+"\n"
   output += "\n"
      
   return output

def main(config):
   config = Path(config).stem
   # read file with hlt config and hlt paths
   with open('hlt_paths.txt') as menu_config:
      paths = menu_config.readlines()
   # in case path is repeated in hlt_paths.txt
   unique_paths = [] 
   [unique_paths.append(x) for x in paths if x not in unique_paths] 

   # importing module using string with importlib.import_module
   loaded_config = importlib.import_module('Analysis.Ntuplizer.'+config)
   process = loaded_config.process
   
   # menu version
   print("# Menu version: " + process.HLTConfigVersion.tableName.value() + "\n")
   with open(config+".yml", "w") as f:
   # menu version
      f.write("# Menu version: " + process.HLTConfigVersion.tableName.value() + "\n")
      f.write("\n")
      #loop over paths
      for hlt_path in unique_paths:
         hlt_path = hlt_path.replace("\n","").strip()
         if not hlt_path: # remove empty lines
            continue
         # remove version if any given
         hlt_path_nov = hlt_path.split("_")
         hlt_path_nov = "_".join(hlt_path_nov[:-1])+"_v"
         output = processing(process,hlt_path_nov)
         if output:
            f.write(output)

if __name__ == "__main__":
   # HLT Path (process uses VarParsing, which prevents using command line parameters directly. TO DO: find a solution, or workaround)
   config = input("Enter the name of the menu config file: ") 
   main(config)
