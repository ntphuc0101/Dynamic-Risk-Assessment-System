import pandas as pd
import sys
import os
from sklearn import metrics
from joblib import load
import json
import logging
from helper_function import preprocess_data

logging.basicConfig\
    (stream=sys.stdout, level=logging.INFO)

#################Load config.json
# and get path variables
with open('config.json','r') as f:
    config = json.load(f)
    logging.info("Loading testdata.csv")
    dataset_csv_path = os.path.join(config['output_folder_path'])
    test_data_path = os.path.join(config['test_data_path'])
    model_path = os.path.join(config['prod_deployment_path'])
    output_model_path = os.path.join(config['output_model_path'])

#################Function for model scoring
def score_model():
    """
    This function should take a trained model
    , load test data, and /
    calculate an F1 score for the model relative
     to the test data
    it should write the result to the
    latestscore.txt file
    """
    logging.info("Loading trained model")
    model = load(os.path.join(model_path,\
                              "trainedmodel.pkl"))
    encoder = load(os.path.join(model_path,\
                                "encoder.pkl"))

    df_frames = pd.read_csv(os.path.join(dataset_csv_path,\
                                         "finaldata.csv"))
    df_x, df_y, _ = preprocess_data(df_frames, encoder)

    logging.info("Predicting test data")
    y_pred = model.predict(df_x)

    f1_score = metrics.f1_score(df_y, y_pred)

    logging.info("Currently, saving latestscore {0}".format(output_model_path))
    if not os.path.isdir(output_model_path):
        os.makedirs(output_model_path)
    with open(os.path.join(output_model_path,\
                           "latestscore.txt"), "w") as score_file:
        score_file.write(str(f1_score) + "\n")
    return f1_score
if __name__ == '__main__':
    logging.info("Running scoring.py")
    score_model()