from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import logging
from diagnostics import model_predictions

logger = logging.getLogger(__name__)

###############Load config.json
# and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path'])
test_data_path = os.path.join(config['test_data_path'])
model_path = config['output_model_path']

def score_model():
    """
    Function for reporting
    calculate a confusion matrix using\
    the test data and the deployed model
    :return: the confusion matrix to the workspace
    """
    y_pred, y_true = model_predictions(None)

   # plot the confusion matrix
    confusion = metrics.confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 6))
    ax = sns.heatmap(confusion, annot=True, cmap='Blues')

    ax.set_title('Confusion matrix')
    ax.set_xlabel('\nPredicted Values')
    ax.set_ylabel('Actual Values')
    ax.xaxis.set_ticklabels(['False', 'True'])
    ax.yaxis.set_ticklabels(['False', 'True'])
    plt.savefig(os.path.join(model_path, 'confusionmatrix.png'))

if __name__ == '__main__':
    score_model()
