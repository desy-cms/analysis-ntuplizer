#!/usr/bin/env python3
"""
Read a CSV file, collect unique HLT menu keys matching a filter, and
generate local python configuration files using the `hltGetConfiguration`
utility.

Each matching `hlt_key` value is normalized into a filename by:
- stripping a leading '/'
- replacing '/' with '_'
- replacing '.' with 'p'
- converting to lowercase
- appending '.py'
"""
import argparse
import csv
import subprocess


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Read a CSV and collect unique hlt_key values matching a filter."
    )
    parser.add_argument(
        "--csv",
        dest="csv_file",
        required=True,
        help="Path to the input CSV file",
    )
    parser.add_argument(
        "--filter",
        dest="filter_string",
        required=True,
        help="Substring filter to apply to the hlt_key column",
    )
    return parser.parse_args()


def main():
    """Process the input CSV and generate HLT configuration files."""
    args = parse_args()
    unique_keys = set()

    with open(args.csv_file, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        if "hlt_key" not in reader.fieldnames:
            raise ValueError("Input CSV must contain a column named 'hlt_key'.")
        for row in reader:
            hlt_key = row.get("hlt_key", "")
            if args.filter_string in hlt_key:
                unique_keys.add(hlt_key)

    unique_list = sorted(unique_keys)
    for hlt_menu in unique_list:
        # Generate a consistent output filename for each matching HLT menu key.
        hlt_config_py = hlt_menu.lstrip('/').replace('/', '_').replace('.', 'p').lower() + '.py'

        with open(hlt_config_py, "w", encoding="utf-8") as outfile:
            # Execute commands sequentially; wait for each hltGetConfiguration to finish before continuing
            proc = subprocess.Popen(["hltGetConfiguration", f"adg:{hlt_menu}"], stdout=outfile)
            proc.wait()
            if proc.returncode != 0:
                raise subprocess.CalledProcessError(proc.returncode, proc.args)

        print(f"Generated {hlt_config_py} from hlt_menu={hlt_menu}")


if __name__ == "__main__":
    main()
