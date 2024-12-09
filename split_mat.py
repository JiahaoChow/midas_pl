import os
import os.path as path
from os.path import join as pj
import argparse
import sys
import csv
from glob import glob
from tqdm import tqdm
import utils
import concurrent.futures

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('--task', type=str, default="ct1_tp1")
o = parser.parse_args()

# Get base directories
base_dirs = sorted(glob(pj("./", o.task, "subset_*")))

# Function to process a single csv file
def process_csv(mat_name, in_dir, out_dir):
    # Load matrix data
    mat = utils.load_csv(mat_name)
    mod = path.splitext(path.basename(mat_name))[0]
    cell_num = len(mat) - 1
    feat_num = len(mat[0]) - 1
    print(f"Splitting {mod} matrix: {cell_num} cells, {feat_num} features")
    
    # Prepare output directory and filename format
    out_mod_dir = pj(out_dir, mod)
    utils.mkdirs(out_mod_dir, remove_old=True)
    vec_name_fmt = utils.get_name_fmt(cell_num) + ".csv"
    vec_name_fmt = pj(out_mod_dir, vec_name_fmt)

    # Save each cell's vector in parallel
    for cell_id in range(cell_num):
        vec_name = vec_name_fmt % cell_id
        utils.save_list_to_csv([mat[cell_id + 1][1:]], vec_name)

# Main loop over base directories
for base_dir in base_dirs:
    # Specify input and output directories
    in_dir = pj(base_dir, "mat")
    out_dir = pj(base_dir, "vec")
    utils.mkdirs(out_dir, remove_old=True)
    print(f"\nDirectory: {in_dir}")

    # Get list of CSV files to process
    mat_names = glob(pj(in_dir, '*.csv'))

    # Use ThreadPoolExecutor to parallelize file processing
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        
        # Submit tasks to thread pool
        for mat_name in mat_names:
            futures.append(executor.submit(process_csv, mat_name, in_dir, out_dir))
        
        # Wait for all futures to complete
        concurrent.futures.wait(futures)