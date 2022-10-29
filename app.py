from flask import Flask, session, jsonify, request
import json
import os
from scoring import score_model
from diagnostics import dataframe_summary, execution_time,\
    outdated_packages_list, missing_percentage,\
    model_predictions
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

######################Set up variables for use in our script
app = Flask(__name__)
app.secret_key = '1652d576-484a-49fd-913a-6879acfa6ba4'

config_file = 'config.json'
logging.info("Reading config file - {}".format(config_file))
with open(config_file,'r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 

prediction_model = None

@app.route('/')
def index():
    return "Hello World"

#######################Prediction Endpoint
@app.route("/prediction", methods=['POST','OPTIONS'])
def predict():        
    """
    call the prediction function you created
    in step 3
    :return: value for prediction outputs
    """
    dataset_path = request.json.get('dataset_path')
    logging.info("dataset path {}".format(dataset_path))
    y_pred, _ = model_predictions(dataset_path)
    return str(y_pred)

@app.route("/scoring", methods=['GET','OPTIONS'])
def stats_scoring():
    """
    Scoring Endpoint
    return value (a single F1 score number)
    in step 3
    """
    #check the score of the deployed model
    score = score_model()
    return str(score)

@app.route("/summarystats", methods=['GET','OPTIONS'])
def stats_summarystats():
    """
    Summary Statistics Endpoint
    return a list of all calculated
    summary statistics
    """
    dataframe_result = dataframe_summary()
    return jsonify(dataframe_result)
@app.route("/diagnostics", methods=['GET','OPTIONS'])
def dignostics():
    """
    Diagnostics Endpoint
    return a list of timing
    and percent NA values
    """
    execution_time_data = execution_time()
    outdated_list = outdated_packages_list()
    missing_pert = missing_percentage()
    result_dict = {
        'missing_percentage': missing_pert,
        'execution_time': execution_time_data,
        'outdated_packages': outdated_list
    }
    return jsonify(result_dict)

if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=8000,\
            debug=True, threaded=True)
