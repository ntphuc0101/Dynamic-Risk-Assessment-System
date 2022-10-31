import logging
from joblib import load
import pandas as pd
import numpy as np
import timeit
import os
import json
import sys
import subprocess
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

##################Load config.json
# and get environment variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
test_data_path = os.path.join(config['test_data_path'])
model_path = os.path.join(config['prod_deployment_path'])
output_path = os.path.join(config['output_folder_path'])

def preprocess_data(df_frames):
    """
    Function for preproccessing data
    Returns:
        df_x : input dataframe
        df_y : label data
    """
    df_y = df_frames["exited"]
    df_x = df_frames.drop(["exited"], axis=1)

    categorical_features = ["corporation"]
    df_x_continuous = df_x.drop(*[categorical_features], axis=1)

    df_x = df_x_continuous

    return df_x, df_y

def model_predictions(data_file):
    """
    Read the deployed model
    and a test dataset,
    calculate predictions
    Returns:
        return value should be a list
        containing all predictions
        y_pred: predictions
        df_y: data frames for testing
    """
    #r
    logging.info("Loading deployed model")
    model = load(os.path.join(model_path, "trainedmodel.pkl"))

    if data_file is None:
        dataset_path = os.path.join(test_data_path, "testdata.csv")
        df_frames = pd.read_csv(dataset_path)
        logging.info("Loading dataset from {}".format(dataset_path))
    else:
        logging.info("Loading dataset {} from\
         input function".format(data_file))
        dataset_path = os.path.join(test_data_path, data_file)
        df_frames = pd.read_csv(dataset_path)

    df_x, df_y = preprocess_data(df_frames)
    logging.info("Running predictions on data")
    y_pred = model.predict(df_x)
    # return value should be a list containing all predictions
    return y_pred, df_y

##################Function to get summary statistics
def dataframe_summary():
    """
    calculate summary statistics here
    Returns:
            return value should be a list
        containing all summary statistics
        'mean' : mean, 'median': median
        'std': std
    """
    #
    logging.info("Loading and preparing finaldata.csv")
    data_df = pd.read_csv(os.path.join(test_data_path,\
                                       'testdata.csv'))
    data_df = data_df.drop(['exited'], axis=1)
    data_df = data_df.select_dtypes('number')

    logging.info("Calculating statistics for data")
    stat_list_dict = []
    for columns in data_df.columns:
        mean = data_df[columns].mean()
        median = data_df[columns].median()
        std = data_df[columns].std()

        stat_list_dict.append({'mean' : mean,\
                               'median': median, 'std': std})
    return stat_list_dict

def timing_ingestion():
    """
    Returns:
        list[dict]: execution times for each script
        ingestion.py
    """
    logging.info('Calculate timing for ingestion.')
    # timing ingestion
    starttime = timeit.default_timer()
    os.system('python3 ingestion.py')
    ingestion_timing = timeit.default_timer() - starttime
    return ingestion_timing

def timing_training():
    """
    Returns:
        list[dict]: execution
        times for each script
        ingestion.py
    """
    logging.info('Calculate timing for ingestion.')
    # timing ingestion
    starttime = timeit.default_timer()
    os.system('python3 training.py')
    training_timing = timeit.default_timer() - starttime
    return training_timing
def execution_time():
    """
    Function to get timings
    Returns:
        list[dict]: execution times for each script
        ingestion.py and training
    """
    logging.info('calculate timing\
                for ingestion and training')
    ingestion_timing = timing_ingestion()
    training_timing = timing_training()

    return [ingestion_timing, training_timing]

def outdated_packages_list():
    """
    Function to check dependencies
    Returns: Out dated packages
    """
    # get a list of
    outdated_packages = subprocess.check_output(['pip',\
                                                 'list', '--outdated'])
    # get the output as table
    outdated_packages = outdated_packages.decode(sys.stdout.encoding)
    return str(outdated_packages)

def missing_percentage():
    """
    Function to check dependencies
    Returns: List[column name : missing percentages]
    """
    logging.info("Loading and preparing finaldata.csv")
    missing_percent = []
    data_df = pd.read_csv(os.path.join(output_path,\
                                       'finaldata.csv'))
    percentage = data_df.isna().sum() / data_df.shape[0] * 100
    for col, percentage in zip(data_df.columns, percentage):
        missing_percent.append({col : percentage})
    return missing_percent

if __name__ == '__main__':
    model_predictions(None)
    # dataframe_summary()
    # print(execution_time())
    outdated_packages_list()





    
