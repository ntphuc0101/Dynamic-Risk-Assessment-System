from flask import Flask, session, jsonify, request
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np
import pickle
import os
from sklearn import metrics
import json
import logging
import sys

print("hello")
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

###################Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
model_path = os.path.join(config['output_model_path']) 

def preprocess_data(df_frames, encoder):
    df_y = df_frames["exited"]
    df_x = df_frames.drop(["exited"], axis=1)

    categorical_features = ["corporation"]
    df_x_categorical = df_x[categorical_features].values
    df_x_continuous = df_x.drop(*[categorical_features], axis=1)

    if not encoder:
        encoder = OneHotEncoder(sparse=False, handle_unknown="ignore")
        df_x_categorical = encoder.fit_transform(df_x_categorical)
    else:
        df_x_categorical = encoder.transform(df_x_categorical)
    df_x = np.concatenate([df_x_categorical, df_x_continuous], axis=1)

    return df_x, df_y, encoder

#################Function for training the model
def train_model():
    """
    reading filedata.csv
    split dataset and training, testing model
    """
    df_frames = pd.read_csv(os.path.join(dataset_csv_path, "finaldata.csv"))
    df_x, df_y, encoder = preprocess_data(df_frames, None)

    x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=0.20)
    
    #use this logistic regression for training
    model = LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                    intercept_scaling=1, l1_ratio=None, max_iter=100,
                    multi_class='auto', n_jobs=None, penalty='l2',
                    random_state=0, solver='liblinear', tol=0.0001, verbose=0,
                    warm_start=False)
    
    #fit the logistic regression to your data
    logging.info("Currently, Training model")
    model.fit(x_train, y_train)
    print("Model score model in training dataset {0}"/
          .format(model.score(x_test, y_test)))

    #write the trained model to your workspace
    # in a file called trainedmodel.pkl
    logging.info("Currently, Saving model {0}".format(model_path))
    if not os.path.isdir(model_path):
        os.makedirs(model_path)

    pickle.dump(model, open(os.path.join(model_path, "trainedmodel.pkl"), 'wb'))
    pickle.dump(encoder, open(os.path.join(model_path, "encoder.pkl"), 'wb'))

if __name__ == '__main__':
    logging.info("Running training.py")
    train_model()
