import os
import logging
import sys
import json
from shutil import copy2

##################Load config.json
# and correct path variable
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
prod_deployment_path = os.path.join(config['prod_deployment_path']) 
model_path = os.path.join(config['output_model_path'])

logging.basicConfig(stream=sys.stdout,\
                    level=logging.INFO)

####################function for deployment
def store_model_into_pickle():
    """
    copy the latest pickle file,
    the latestscore.txt value
    , and the ingestfiles.txt file into
    the deployment directory
    :param model: trained model
    :return: None
    """
    # check the output folder is not
    if not os.path.isdir(prod_deployment_path):
        os.makedirs(prod_deployment_path)
    copied_files = ["latestscore.txt", "ingestedfiles.txt",\
                    "trainedmodel.pkl", "encoder.pkl"]
    logging.info("Deploying trained model to production")
    logging.info(
        "Copying trainedmodel.pkl,\
        ingestfiles.txt and latestscore.txt")
    for file in copied_files:
        source_filepath = os.path.join(model_path, file)
        if not os.path.exists(source_filepath):
            source_filepath = os.path.join(dataset_csv_path, file)
            copy2(source_filepath, prod_deployment_path)
            logging.info("copy {0} to {1}".format(source_filepath,\
                                                  prod_deployment_path))
        else:
            logging.info("copy {0} to {1}".format(source_filepath,\
                                                  prod_deployment_path))
            copy2(source_filepath,\
                  prod_deployment_path)

if __name__ == '__main__':
    logging.info("Running deployment.py")
    store_model_into_pickle()
        

