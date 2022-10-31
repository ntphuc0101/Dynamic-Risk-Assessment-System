import os
import json

with open('config.json','r') as f:
    config = json.load(f)

dataset_csv_path = os.path.join(config['output_folder_path'])
model_path = os.path.join(config['output_model_path'])

def preprocess_data(df_frames):
    """
    Function for preproccessing data
    Returns:
        df_x : input dataframe
        df_y : label data
    """
    # The dataset's final column, "exited",
    # is the target variable for our predictions
    # so drop this column
    # "corporation", will not be
    # used in modeling, this column is dropped
    df_y = df_frames["exited"]
    df_x = df_frames.drop(["exited"], axis=1)

    categorical_features = ["corporation"]
    df_x_continuous = df_x.drop(*[categorical_features], axis=1)

    df_x = df_x_continuous

    return df_x, df_y