import importlib
import re

# Perhaps the problem is this: VarParsing.parseArguments() expects to be run from cmsRun, where sys.argv has a very specific format - cmsRun config.py
# But running here there is no python file being parsed. By using these lines below, things seem to run fine withing python
# import sys
# sys.argv = ['dummy.py']
# import importlib
# loaded_config = importlib.import_module("Analysis.Ntuplizer.cdaq_physics_run2024_2e34_v1p0p3_hlt_v2")


def hlt_paths_info(config,hlt_paths):
    # importing module using string with importlib.import_module
    if config.endswith(".py"):
        config = config.replace(".py", "")    
    loaded_config = importlib.import_module(config)
    process = loaded_config.process
    
    outputs = []
    
    # remove possible repeated paths in the hlt_paths list
    unique_paths = [] 
    [unique_paths.append(x) for x in hlt_paths if x not in unique_paths] 
    menu_version = process.HLTConfigVersion.tableName.value()
    for hlt_path in unique_paths:
        output = ''
        # remove version number from paths
        hlt_path_no_version = hlt_path.split("_")
        hlt_path_no_version = "_".join(hlt_path_no_version[:-1])+"_v"    

        # get all paths in the menu configuration
        path_names = process.pathNames().split(" ")
        path_names = [x for x in path_names if x.startswith("HLT_")]

        menu_hlt_paths = [x for x in path_names if x.startswith(hlt_path_no_version)]
        if not menu_hlt_paths:
            print("WARNING: "+hlt_path_no_version+" not in this menu! Skipping!")
            continue
        
        menu_hlt_path = menu_hlt_paths[0]
        # cms path
        cms_path = eval("process."+menu_hlt_path+".dumpPythonNoNewline()")
        # remove cms.Path
        cms_path = cms_path[9:-1]
        cms_path_modules = cms_path.split("+")
        #ignored modules
        ignored_modules = [ x for x in cms_path_modules if "ignore" in x]
        ignored_modules = [re.search('\(([^)]+)',ig).group(1) for ig in ignored_modules]
    
        # all process modules
        process_modules = eval("process."+menu_hlt_path+".moduleNames()")
    
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
            print("WARNING: no trigger object in the cms.Path for path "+hlt_path_no_version)
            continue
            
        trg_objs = trg_objs_order
    
        # prepare output
        output += menu_hlt_path+":\n"
        output += " l1seeds:\n"
        for l1s in l1_seeds:
            output += " - "+l1s+"\n"
        output += " trigger_objects:\n"
        for to in trg_objs:
            output += " - "+to+"\n"
        output += "\n"
        outputs.append(output)
        
    return menu_version,outputs