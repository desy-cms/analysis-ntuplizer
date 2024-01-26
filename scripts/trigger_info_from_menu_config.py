#!/usr/bin/env python3


# hlt_paths.txt is a file whose lines contain each the name of
# the HLT paths the will go into the trigger_info.yml
# User will be asked to give the configuration of the trigger menu
# The configuration file containing the menu should be put in
# Analysis/Ntuplizer/python

import re
import sys
import importlib
import argparse

from pathlib import Path

from Analysis.Ntuplizer.utils.hlt_paths_info import hlt_paths_info

def main(config_module_name,paths_filename):
   config = config_module_name
   if config.endswith(".py"):
      config = config.replace(".py", "")
   output_yaml = config.split('.')[-1]+".yml"
   # read file with hlt config and hlt paths
   with open(paths_filename) as menu_config:
      paths = menu_config.readlines()
   
   menu_version, outputs = hlt_paths_info(config,paths)
   with open(output_yaml, "w") as f:
      f.write(f"# Menu version: {menu_version}\n")
      f.write("\n")
      for output in outputs:
         if output:
            f.write(output)
      
if __name__ == "__main__":
   # HLT Path (process uses VarParsing, which prevents using command line parameters directly. TO DO: find a solution, or workaround; see below)

   # Create an argument parser
   parser = argparse.ArgumentParser()
   # Add an argument for the comma-separated values
   parser.add_argument("--paths", default="hlt_paths.txt", help="file with list of paths")
   parser.add_argument("--configs", help="comma-separated values fo configuration modules name")
   # Parse the arguments
   args = parser.parse_args()
   # Split the values into a list
   configs = args.configs.split(",")
   paths_filename = args.paths

   # Remove the command line arguments to avoid problems with VarParsing
   sys.argv = sys.argv[:1]

   # trigger info for each config
   for config_module_name in configs:
      if config_module_name:
         main(config_module_name,paths_filename)
