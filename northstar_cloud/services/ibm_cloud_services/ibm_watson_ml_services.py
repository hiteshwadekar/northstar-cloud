import json
import os
import random
import pandas as pd

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE
from sklearn.metrics import confusion_matrix
from joblib import dump, load

from northstar_cloud.common import logs as logging
from northstar_cloud.common import utils as c_utils

DEFAULT_MODEL_PATH = "northstar_cloud/services/ml_models/"
DEFAULT_MODEL_NAME = "northstar_fire_pred.joblib"
ROOT_DIR = os.path.abspath(os.curdir)

LOG = logging.getLogger(__name__)


class IBMWatsonMLAnalytics(object):
    def __init__(self, watson_model_path):
        self.watson_model_path = watson_model_path
        self.model = self._load_model()

    def _load_model(self):
        return load(self.watson_model_path)

    def predict_fire(self, user, user_weather_data):
        LOG.info("IBMWatsonMLAnalytics:predict_fire: IBM ML analytics "
                 "request for user (%s, %s)", user.user_id, user.user_name)
        is_fire = False

        # Enable model once corresponding weather data conversion available.
        random_list = [True, False]
        return random.choice(random_list)

def get_analytics_helper():
    config = c_utils.read_config()
    ibm_analytics_helper = None
    if config:
        path = ROOT_DIR + "/" + config.get("fire_model_path", DEFAULT_MODEL_NAME) \
               + config.get("fire_model_name", DEFAULT_MODEL_PATH)
        ibm_analytics_helper = IBMWatsonMLAnalytics(path)
    return ibm_analytics_helper