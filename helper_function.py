import os
import json
import numpy as np
from sklearn.preprocessing import OneHotEncoder

with open('config.json','r') as f:
    config = json.load(f)

dataset_csv_path = os.path.join(config['output_folder_path'])
model_path = os.path.join(config['output_model_path'])

def preprocess_data(df_frames, encoder):
    """
    Function for preproccessing data
    Returns:
        df_x : input dataframe
        df_y : label data
        encoder : one hotspot coding
    """
    # The dataset's final column, "exited",
    # is the target variable for our predictions
    # so drop this column
    # "corporation", will not be
    # used in modeling, this column is dropped
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