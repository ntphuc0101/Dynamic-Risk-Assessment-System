from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from joblib import load
import json
import logging



#################Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f)

    logging.info("Loading testdata.csv")
    dataset_csv_path = os.path.join(config['output_folder_path'])
    test_data_path = os.path.join(config['test_data_path'])


#################Function for model scoring
def score_model():
    """
    This function should take a trained model, load test data, and /
    calculate an F1 score for the model relative to the test data
    it should write the result to the latestscore.txt file
    """
    model = load(os.path.join(model_path, "trainedmodel.pkl"))
    encoder = load(os.path.join(model_path, "encoder.pkl"))