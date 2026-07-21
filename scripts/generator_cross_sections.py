#!/usr/bin/env python3
import os
import sys
import subprocess
import yaml
import re
import argparse
import textwrap

def fix_yaml_format(filename):
    """
    Reads a file, modifies lines based on specific rules, and writes the updated content back to the file.
    pyyaml dump width parameter seems not to be working, which spoils the format

    Args:
        filename (str): The path to the input file.

    Returns:
        None
    """
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        modified_lines = []
        
        modified_lines.append('# --------------------------------------------------------------------')
        modified_lines.append('# MC Datasets for RunII Legacy')
        modified_lines.append('# Cross sections can be obtained from the database')
        modified_lines.append('#    https://cms-gen-dev.cern.ch/xsdb')
        modified_lines.append('#    -> search query: DAS=<primary dataset name>')
        modified_lines.append('# or from the generator itself')
        modified_lines.append('#    https://twiki.cern.ch/twiki/bin/view/CMS/HowToGenXSecAnalyzer')
        modified_lines.append('# --------------------------------------------------------------------')
        modified_lines.append('#')
        modified_lines.append('')
        
        # patterns for matching
        pattern_question_mark = r'\s+\?\s+'
        pattern_colon = r'\s+\:'
        pattern_not_space = r'^[^\s]'

        
        for line in lines:
            line = line.rstrip()  # Remove trailing whitespace

            match_question_mark = re.search(pattern_question_mark, line)
            match_colon = re.search(pattern_colon, line)
            match_not_space = re.search(pattern_not_space, line)
            
            if match_question_mark:
                matched_question_mark_substring = match_question_mark.group(0).lstrip()
                modified_line = re.sub(re.escape(matched_question_mark_substring), '', line, count=1)
                modified_lines.append(modified_line)
            elif match_colon:
                matched_colon_substring = match_colon.group(0).lstrip()
                modified_lines[-1] = modified_lines[-1]+":"
                modified_line = re.sub(re.escape(matched_colon_substring), ' ', line, count=1)
                modified_lines.append(modified_line)
            else:
                # Regular line, no modification needed
                if match_not_space:
                    modified_lines.append('')
                    modified_lines.append('#####')
                modified_lines.append(line)

        with open(filename, 'w') as output_file:
            output_file.write('\n'.join(modified_lines))

        print(f"File '{filename}' processed successfully.")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")

    

def download_gen_xsec_cfg():
    # Download genXsec_cfg.py from GitHub
    # https://twiki.cern.ch/twiki/bin/view/CMS/HowToGenXSecAnalyzer
    try:
        subprocess.run(["curl", "-s", "https://raw.githubusercontent.com/cms-sw/genproductions/master/Utilities/calculateXSectionAndFilterEfficiency/genXsec_cfg.py", "-o", "genXsec_cfg.py"], check=True)
        print("genXsec_cfg.py downloaded successfully.")
    except subprocess.CalledProcessError:
        print("Error downloading genXsec_cfg.py. Please check the URL or try again later.")
        sys.exit(1)
        
        
def extract_primary_dataset(dataset_name):
    # Extract the primary dataset name (last part of the dataset path)
    parts = dataset_name.split("/")
    primary_dataset = parts[1]
    return primary_dataset

def gen_xsec_analyzer(dataset_list_name,dataset_name,num_files=1):
    xsection_pb = -1.
    xsection_uncert_pb = -1.
    # Extract the primary dataset name
    primary_dataset = extract_primary_dataset(dataset_name)
    # Construct the dasgoclient query 
    query = f'dasgoclient -query="file dataset={dataset_name}" | head -n {num_files}'
    try:
        # Execute the query and get the first file path
        file_path = subprocess.check_output(query, shell=True, text=True).strip().replace('\n',',')
        # Run the cmsRun command
        cmsrun_command = f'cmsRun genXsec_cfg.py inputFiles={file_path} maxEvents=-1 >& ./log/{primary_dataset}_{dataset_list_name}.log'
        subprocess.run(cmsrun_command, shell=True, check=True)
        print(f"Analysis completed for dataset: {dataset_name}./nOutput saved as ./log/{primary_dataset}_{dataset_list_name}.log")

        # Extract cross section from the output file
        with open(f"./log/{primary_dataset}_{dataset_list_name}.log", "r") as output_file:
            for line in output_file:
                if "After filter: final cross section" in line:
                    xsection_str = line.split("=")[1].strip()
                    xsection_str = xsection_str.replace("pb", "")  # Remove "pb" if present
                    xsection_pb, xsection_uncert_pb = map(float, xsection_str.split("+-"))
                    break
    except subprocess.CalledProcessError:
        print(f"Error running analysis for dataset: {dataset_name}")
                        
    return xsection_pb, xsection_uncert_pb

def update_yaml(datasets_yml,dataset_list_name,dataset_name,xsection):
    xsection_pb = xsection[0]
    xsection_uncert_pb = xsection[1]
    # Update datasets.yml with cross section values for the specific process
    with open(datasets_yml, "r") as yml_file:
        datasets = yaml.safe_load(yml_file)
        if dataset_list_name in datasets:
            try:
                datasets[dataset_list_name][dataset_name]["xsection_pb"] = xsection_pb
                datasets[dataset_list_name][dataset_name]["xsection_uncert_pb"] = xsection_uncert_pb
            except TypeError as e:
                # create the keys, if they don't exist, and fill the values
                datasets[dataset_list_name][dataset_name] = {}
                datasets[dataset_list_name][dataset_name]["xsection_pb"] = xsection_pb
                datasets[dataset_list_name][dataset_name]["xsection_uncert_pb"] = xsection_uncert_pb
            if xsection_pb > 0:                     
                print(f"Updated {datasets_yml} with cross section values for {dataset_name} in {dataset_list_name}")
        else:
            print(f"'{dataset_list_name}' not found in datasets.yml. No update performed.")

    # Write updated datasets.yml back to file
    with open(datasets_yml, "w") as yml_file:
        yaml.dump(datasets, yml_file, default_flow_style=False, width = 1000, sort_keys=False)



def main():
    
    print("======================================================================================================")
    print("WARNING: while processing the yaml_file may have weird format. The formatting will be fixed at the end")
    print("N.B.: the cross sections differ from file to file, i.e., same process may have different values")
    print("======================================================================================================")
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            Process datasets for cross sections
            The yaml_file has the following minimal structure:
            dataset_list_name1:
              dataset1_1:
              dataset1_2:
              ...
            dataset_list_name2:
              dataset2_1:
              dataset2_2:
              ...
        '''))
    parser.add_argument("--yaml_file", required=True, help="Path to the YAML file containing datasets")
    parser.add_argument("--dataset_list_name", required=True, help="Name of the dataset list")
    parser.add_argument("--no_xsection", action="store_true", help="Will set xsection to -1")
    parser.add_argument("--num_files", type=int, default=1, help="Number of files to process")    

    args = parser.parse_args()
    yaml_file = args.yaml_file
    dataset_list_name = args.dataset_list_name
    no_xsection = args.no_xsection
    num_files = args.num_files
    
    # Download genXsec_cfg.py
    if not no_xsection:
        download_gen_xsec_cfg()
        os.makedirs("./log", exist_ok=True)
    
    with open(yaml_file, "r") as yml_file:
        datasets = yaml.safe_load(yml_file)
        dataset_list = datasets.get(dataset_list_name, {}).keys()
    
    xsection = (-1.,-1.)
    for dataset in dataset_list:
        if not no_xsection:
            xsection_pb, xsection_uncert_pb = gen_xsec_analyzer(dataset_list_name,dataset,num_files)
            xsection = (xsection_pb, xsection_uncert_pb)
        update_yaml(yaml_file,dataset_list_name,dataset,xsection)
 
    # The pyyaml dump width parameter does not work!?
    fix_yaml_format(yaml_file)
    
    print("======================================= THE END ======================================================")

    

# Example usage
if __name__ == "__main__":
    main()
    
    
