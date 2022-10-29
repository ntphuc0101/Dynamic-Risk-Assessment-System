import requests
import logging
import sys
import json
import os
import pandas as pd
#Specify a URL that resolves to your workspace
URL = "http://192.168.1.100:8000/"
logging.basicConfig(stream=sys.stdout,\
                    level=logging.INFO)

config_file = 'config.json'
logging.info("Reading config file - {}".format(config_file))
with open(config_file,'r') as f:
    config = json.load(f)

#Call each API endpoint and store the responses
headers = {'Content-type': 'application/json',\
           'Accept': 'text/plain'}
logging.info("Headers is {}".format(headers))

model_path = os.path.join(config['output_model_path'])

json_file = 'config.json'
with open(json_file,'r') as f:
    config = json.load(f)
model_path = os.path.join(config['output_model_path'])
logging.info("Reading json file - {}".format(json_file))

# #Call each API endpoint and store the responses
json_header = {"dataset_path": "testdata.csv"}
logging.info("Reading with routing prediction and json - {}"\
             .format(json_header))
response1 = requests.post("%s/prediction" % URL,\
                          json=json_header, headers=headers).text

response_get = ['scoring', 'summarystats', 'diagnostics']
responses = []
responses.append(response1)

for get_item in response_get:
    if get_item == 'scoring':
        response = requests.get(f'{URL}/{get_item}').text
    else:
        response = requests.get(f'{URL}/{get_item}').json()

    responses.append(response)
# #write the responses to your workspace
count_response = 0
with open(os.path.join(model_path, "apireturns2.txt"), "w") as w_file:
    w_file.write(' ===============================================\n')
    w_file.write('              ** Model reporting   **               \n')
    for item_response in responses:
        w_file.write('\n===============================================\n')

        if count_response == 0:
            w_file.write('\n Result of routing prediction \n')
            w_file.write('F1 score is {}'.format(item_response))

        elif count_response == 3:
            w_file.write('\n Result of execution time \n')
            w_file.write(json.dumps(item_response['execution_time'],\
                                    indent=4, sort_keys=True))
            w_file.write('\n Result of missing percentage \n')
            w_file.write(json.dumps(item_response['missing_percentage'],\
                                    indent=4, sort_keys=True))
            w_file.write('\n Result of outdated list \n')
            w_file.write(item_response['outdated_packages'])

        elif count_response == 2:
            w_file.write('\n Result of summary stats \n')
            df_frame = pd.DataFrame(item_response)
            w_file.write(str(df_frame))
            
        else:
            w_file.write('\nResults of routing {} '.\
                         format(response_get[count_response-1]))
            w_file.write('{}'.format(item_response))

        count_response = count_response + 1

