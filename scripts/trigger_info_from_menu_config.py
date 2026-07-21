#!/usr/bin/env python3


# hlt_paths.txt is a file whose lines contain each the name of
# the HLT paths the will go into the trigger_info.yml
# User will be asked to give the configuration of the trigger menu
# The configuration file containing the menu should be put in
# Analysis/Ntuplizer/python

import sys
import os
import glob
import argparse
from Analysis.Ntuplizer.utils.hlt_paths_info import hlt_paths_info

def main(args):
   
   paths_filename = args.paths
   with open(paths_filename) as menu_config:
      paths = menu_config.readlines()
      
   configs = glob.glob(args.configs)
   configs.sort()

   hlt_menu_versions = {}
   menu_objects = {}
   hlt_paths_objects = {}
   total_configs = len(configs)
   for idx, config in enumerate(configs, start=1):

      if not config: 
         continue
      # if config.endswith(".py"):
      #    config = config.replace(".py", "")
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
      # progress bar 
      if total_configs:
         progress = (idx / total_configs) * 100
      else:
         progress = 100.0
      # progress bar on same line, filled with 'x'
      bar_len = total_configs
      filled = int((progress / 100.0) * bar_len)
      bar = "x" * filled + "-" * (bar_len - filled)
      print(f"Processing config {idx}/{total_configs} ({progress:.1f}%) [{bar}]", end="\r", file=sys.stderr, flush=True)

   
   # Save the trigger info to a YAML file
   # finish progress line
   print(file=sys.stderr)
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
   # Add an argument for the comma-separated values or glob pattern
   parser.add_argument("--paths", default="hlt_paths.txt", help="file with list of paths")
   parser.add_argument("--configs", default="./hlt_configs/*.py", help="glob pattern for configuration module files\n!!! use quotes in the command line to avoid shell expansion")
   parser.add_argument("--output", default="output_yaml.yml", help="output yaml file name")
   # Parse the arguments
   args = parser.parse_args()

   # Remove the command line arguments to avoid problems with VarParsing
   sys.argv = sys.argv[:1]

   main(args)