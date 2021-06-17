import re
import sys
import importlib

# # importing module using string with importlib.import_module
# #from hlt_10_1_0_grun_v1 import process
# loaded_process = importlib.import_module("hlt_10_1_0_grun_v1")
# process = loaded_process.process
# 
def processing(process,hlt_path_nov):
   output = ''
   # get all paths in the menu configuration
   path_names = process.pathNames().split(" ")
   path_names = [x for x in path_names if x.startswith("HLT_")]

   hlt_paths = [ x for x in path_names if hlt_path_nov in x ]
   if len(hlt_paths) < 1:
      print("WARNING: "+hlt_path_nov+" not in this menu! Skipping!")
      print
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
#   print(process_modules)
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
   
   # remove the version number from the path
#   hlt_path_nov = hlt_path.split("_")
#   hlt_path_nov = "_".join(hlt_path_nov[:-1])+"_v"
   
   # prepare output
   output += hlt_path_nov+":\n"
   output += " l1seeds:\n"
   for l1s in l1_seeds:
      output += " - "+l1s+"\n"
   output += " trigger_objects:\n"
   for to in trg_objs:
      output += " - "+to+"\n"
   output += "\n"
      
   return output

def main():
   # read file with hlt config and hlt paths
   with open('hlt_paths.txt') as menu_config:
      paths = menu_config.readlines()
   config = paths[0].replace("\n","")
   # importing module using string with importlib.import_module
   #from hlt_10_1_0_grun_v1 import process
   loaded_process = importlib.import_module(config)
   process = loaded_process.process
   
   # menu version
   print("# Menu version: " + process.HLTConfigVersion.tableName.value() + "\n")
   #loop over paths
   with open(config+".yml", "w") as f:
   # menu version
      f.write("# Menu version: " + process.HLTConfigVersion.tableName.value() + "\n")
      f.write("\n")
      for hlt_path in sorted(paths[1:]):
         hlt_path = hlt_path.replace("\n","").strip()
#         if not "HLT_Mu12_DoublePFJets54MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v" in hlt_path:
#            continue 
         output = processing(process,hlt_path)
         if output:
            f.write(output)

if __name__ == "__main__":
   # HLT Path (process uses VarParsing, which prevents using command line parameters directly. TO DO: find a solution, or workaround)
   hlt_path = "HLT_Mu12_DoublePFJets40MaxDeta1p6_DoubleCaloBTagCSV_p79_v"
   #hlt_path = "HLT_Mu8_v11"
   main()
