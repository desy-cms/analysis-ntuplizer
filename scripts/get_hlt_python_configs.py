#!/usr/bin/env python3
"""
Read a CSV file, collect unique HLT menu keys matching a filter, and
generate local python configuration files using the `hltGetConfiguration`
utility.

This script scans the CSV `hlt_key` column for values containing the
requested substring filter. For each unique matching HLT menu key, it
invokes `hltGetConfiguration adg:<hlt_menu>` and writes the resulting
Python configuration to a local file.

Each matching `hlt_key` value is normalized into a filename by:
- stripping a leading '/'
- replacing '/' with '_'
- replacing '.' with 'p'
- converting to lowercase
- appending '.py'

Example usage:
    ./get_hlt_configs.py --run_summary run_summary_2023_pp.csv --filter_hlt_key /cdaq/physics/Run2023 [--output-dir ./hlt_configs]

The output files are written into the specified output directory with
one generated Python configuration file per unique matching HLT menu.

"""
import argparse
import csv
import os
import subprocess
import sys

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Read a CSV from the run summary and collect unique hlt_key values matching a filter."
    )
    parser.add_argument(
        "--run_summary",
        dest="run_summary_file",
        required=True,
        help="Path to the input CSV file",
    )
    parser.add_argument(
        "--filter_hlt_key",
        dest="filter_hlt_key",
        required=True,
        help="Substring filter to apply to the hlt_key column",
    )
    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        default="./hlt_configs",
        help="Directory where generated HLT config python files will be saved",
    )
    
    return parser.parse_args()

def main():
    """Process the input CSV and generate HLT configuration files."""
    args = parse_args()
    unique_keys = set()

    with open(args.run_summary_file, newline="", encoding="utf-8") as csvfile:
        filtered_lines = (line for line in csvfile if not line.lstrip().startswith('#'))
        reader = csv.DictReader(filtered_lines, delimiter=',', quotechar='"')
        if "hlt_key" not in reader.fieldnames:
            raise ValueError("Input CSV must contain a column named 'hlt_key'.")
        for row in reader:
            hlt_key = row.get("hlt_key", "")
            if args.filter_hlt_key in hlt_key:
                unique_keys.add(hlt_key)

    os.makedirs(args.output_dir, exist_ok=True)
    unique_list = sorted(unique_keys)
    
    print(f"Unique HLT menu keys (total of {len(unique_list)})")
    # for hlt_key in unique_list:
    #     print(hlt_key)

    config_hlt_paths = {}
    unique_hlt_paths = set()
    for index, hlt_menu in enumerate(unique_list, start=1):
        # Generate a consistent output filename for each matching HLT menu key.
        hlt_config = hlt_menu.lstrip('/').replace('/', '_').replace('.', 'p').lower()
        hlt_config_file = os.path.join(args.output_dir, hlt_config + '.py')

        with open(hlt_config_file, "w", encoding="utf-8") as outfile:
            # Execute commands sequentially; wait for each hltGetConfiguration to finish before continuing
            proc = subprocess.Popen(["hltGetConfiguration", f"adg:{hlt_menu}"], stdout=outfile)
            proc.wait()
            if proc.returncode != 0:
                raise subprocess.CalledProcessError(proc.returncode, proc.args)

        print(f"[{index}/{len(unique_list)}] Generated {hlt_config_file} from hlt_menu={hlt_menu}")
        
    #     # looking at the HLT Paths in the generated config file
    #     sys.argv = ['dummy.py']
    #     namespace = {}
    #     with open(hlt_config_file) as f:
    #         code = f.read()
    #     exec(compile(code, "dummy.py", "exec"), namespace)
    #     process = namespace["process"]
    #     config_hlt_paths[hlt_config] = [x for x in process.pathNames().split(" ") if x.startswith("HLT_")]
    #     for hlt_path in config_hlt_paths[hlt_config]:
    #         unique_hlt_paths.add(hlt_path)
    # print(config_hlt_paths.keys())


if __name__ == "__main__":
    main()
