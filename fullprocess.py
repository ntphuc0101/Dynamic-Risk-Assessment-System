import training
import scoring
import deployment
import diagnostics
import reporting
import ingestion
import json
import os
import logging
import glob

file_config = "config.json"
with open(file_config, "r") as f:
    config = json.load(f)

input_folder_path = config["input_folder_path"]
prod_deployment_path = os.path.join(config['prod_deployment_path'])
model_path = os.path.join(config['output_model_path'])
output_path = os.path.join(config['output_folder_path'])
#Check and read new data
#first, read ingestedfiles.txt
# Check and read new data
logging.info("Checking for new data")

# First, read ingestedfiles.txt
ingested_files = []
with open(os.path.join(output_path, "ingestedfiles.txt")) as files:
    for file in files:
        ingested_files.append(file.rstrip())
#second, determine whether the source data folder
# has files that aren't listed in ingestedfiles.txt
source_files = set(glob.glob(input_folder_path + '/*.csv'))
isnon_source_data = False
for file in source_files:
    if file not in ingested_files:
        isnon_source_data = True
##################Deciding whether to proceed, part 1
#if you found new data, then proceed. otherwise,
# do end the process here
if not isnon_source_data:
    logging.info("No new data found")
    exit(0)
##################Checking for model drift
#check whether the score from the
# deployed model is different from
# the score from the model that uses the newest ingested data
ingestion.merge_multiple_dataframe()
scoring.score_model()
score_arr = []
score_files = [prod_deployment_path, model_path]
for file in score_files:
    with open(os.path.join(file, "latestscore.txt"), "r")\
            as report_score_f1:
        score_arr.append(float(report_score_f1.read()))

##################Deciding whether to proceed, part 2
#if you found model drift, you should proceed.
# otherwise, do end the process here
if score_arr[0] <= score_arr[1]:
    logging.info("No model drift detected")
    exit(0)

##################Re-deployment
#if you found evidence for model drift,
# re-run the deployment.py script
logging.info("Re-training model, if model is drifted")
training.train_model()
logging.info("Re-scoring model with the re-trained one")
scoring.score_model()

##################Diagnostics and reporting
# Re-deployment
logging.info("Re-deploying model into production")
# If you found evidence for model drift,
# re-run the deployment.py script
deployment.store_model_into_pickle()
# Diagnostics and reporting
logging.info("Running diagnostics and reporting the model")
#run diagnostics.py and reporting.py
# for the re-deployed model
diagnostics.model_predictions(None)
diagnostics.dataframe_summary()
diagnostics.missing_percentage()
diagnostics.execution_time()
diagnostics.outdated_packages_list()

reporting.score_model()





