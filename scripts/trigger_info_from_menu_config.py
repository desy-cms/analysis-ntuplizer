#!/usr/bin/env python3


# hlt_paths.txt is a file whose lines contain each the name of
# the HLT paths the will go into the trigger_info.yml
# User will be asked to give the configuration of the trigger menu
# The configuration file containing the menu should be put in
# Analysis/Ntuplizer/python

import sys
import argparse
from Analysis.Ntuplizer.utils.hlt_paths_info import hlt_paths_info

def main(args):
   # Split the values into a list
   configs = args.configs.split(",")
   paths_filename = args.paths
   with open(paths_filename) as menu_config:
      paths = menu_config.readlines()
   
   hlt_menu_versions = {}
   menu_objects = {}
   hlt_paths_objects = {}
   for config in configs:
      if not config: 
         continue
      if config.endswith(".py"):
         config = config.replace(".py", "")
      # output_yaml = config.split('.')[-1]+".yml"
      # read file with hlt config and hlt paths
      
      hlt_menu_versions[config], menu_objects[config] = hlt_paths_info(config,paths)
      # The menu_objects is a list with each hlt_path as one element.
      # They are already in yaml format from hlt_paths_info, so we can just write them to the output file
      # TODO: perhaps this should be changed, i.e. convert to yaml here instead of there??? 
      for hlt_path in menu_objects[config]:
         if not hlt_path:
            continue
         hlt_path_v = hlt_path.split("\n")[0]  # get the path name with the version number, e.g. HLT_Mu50_v1
         # As this is a dictionary, if the same path is in different menus, it will be overwritten, but the last one will be kept
         # it should be safe by construction, for the same path should have the same modules in different menus
         hlt_paths_objects[hlt_path_v] = hlt_path
   
   # Save the trigger info to a YAML file
   with open(args.output, "w") as f:
      f.write("#==================================================================\n")
      f.write("# Trigger information for ntuple production\n")
      f.write("#==================================================================\n")
      f.write("# Trigger info extracted from the following HLT menu versions\n")
      for menu_version in hlt_menu_versions.values():
         f.write(f"# Menu version: {menu_version}\n")
      f.write("#------------------------------------------------------------------\n")
      f.write("\n")
      for path_objects in hlt_paths_objects.values():
         for path_object in path_objects:
            if path_object:
               f.write(path_object)
      
if __name__ == "__main__":
   # HLT Path (process uses VarParsing, which prevents using command line parameters directly. TO DO: find a solution, or workaround; see below)
   # Create an argument parser
   parser = argparse.ArgumentParser()
   # Add an argument for the comma-separated values
   parser.add_argument("--paths", default="hlt_paths.txt", help="file with list of paths")
   parser.add_argument("--configs", help="comma-separated values fo configuration modules name")
   parser.add_argument("--output", default="output_yaml.yml", help="output yaml file name")
   # Parse the arguments
   args = parser.parse_args()

   # Remove the command line arguments to avoid problems with VarParsing
   sys.argv = sys.argv[:1]

   main(args)