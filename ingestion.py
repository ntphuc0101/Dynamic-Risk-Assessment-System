"""
Author: Nguyen Thai Vinh PHuc
Date: October, 2022
This script used for ingesting data
"""
import pandas as pd
import os
import logging
import json
import sys
import glob
from datetime import datetime
logging.basicConfig(stream=sys.stdout, level=logging.INFO)




#############Load config.json and get input and output paths
with open('config.json','r') as f:
    config = json.load(f) 

input_folder_path = config['input_folder_path']
output_folder_path = config['output_folder_path']
if not os.path.isdir(output_folder_path):
    os.makedirs(output_folder_path)

logging.info(f"Reading files from {input_folder_path}")


#############Function for data ingestion
def merge_multiple_dataframe():
    #check for datasets, compile them together, and write to an output file
    csv_files = glob.glob("%s/*.csv" % input_folder_path)

    df_frames = pd.concat(map(pd.read_csv, csv_files), ignore_index=True)

    logging.info("Curently, Dropping duplicates.")
    df_frames.drop_duplicates(inplace=True)

    logging.info("Saving ingested txt file")
    df_frames.to_csv(os.path.join(output_folder_path, 'finaldata.csv'), index=False)

    logging.info("Saving ingested metadata - read file names with paths")
    with open(os.path.join(output_folder_path, 'ingestedfiles.txt'), "w") as file:
        file.write("\n".join(csv_files))

if __name__ == '__main__':
    merge_multiple_dataframe()
