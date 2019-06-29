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
import pickle

from northstar_cloud.common import logs as logging
from northstar_cloud.common import utils as c_utils

DEFAULT_MODEL_PATH = "northstar_cloud/services/ml_models/"
DEFAULT_MODEL_NAME = "northstar_fire_pred.joblib"
DEFAULT_COL_PICK_NAME = "columns_to_keep.pickle"
DEFAULT_MOD_PICK__NAME = "columns_to_keep.pickle"
ROOT_DIR = os.path.abspath(os.curdir)

LOG = logging.getLogger(__name__)


class IBMWatsonMLAnalytics(object):
    def __init__(self, watson_model_path, watson_model_pickle_mod, watson_model_pickle_col):
        self.watson_model_path = watson_model_path
        self.watson_model_pickle_mod = watson_model_pickle_mod
        self.watson_model_pickle_col = watson_model_pickle_col
        self.model = self._load_model()

    def _load_model(self):
        return load(self.watson_model_path)

    def preprocess(self, input_data):
        df_input = pd.DataFrame(
            input_data, columns=['Date',
                                 'apparentTemperature',
                                 'cloudCover',
                                 'dayofyear',
                                 'dewPoint',
                                 'fire',
                                 'hour',
                                 'humidity',
                                 'icon',
                                 'latitude',
                                 'longitude',
                                 'monthofyear',
                                 'ozone',
                                 'precipAccumulation',
                                 'precipIntensity',
                                 'precipProbability',
                                 'precipType',
                                 'pressure',
                                 'summary',
                                 'temperature',
                                 'time',
                                 'uvIndex',
                                 'visibility',
                                 'windBearing',
                                 'windGust',
                                 'windSpeed']
        )
        df_input.drop(columns=['Date',
                               'precipAccumulation',
                               'precipType',
                               'latitude',
                               'longitude',
                               'time',
                               'apparentTemperature',
                               'icon',
                               'dayofyear',
                               'windGust',
                               'precipIntensity'], inplace=True)

        return df_input

    def predict_fire(self, user, user_weather_data):
        LOG.info("IBMWatsonMLAnalytics:predict_fire: IBM ML analytics "
                 "request for user (%s, %s)", user.user_id, user.user_name)
        is_fire = False

        # Enable model once corresponding weather data conversion available.
        random_list = [True, False]
        return random.choice(random_list)

    def predict_fire_ml(self, user, input_data):
        LOG.info("IBMWatsonMLAnalytics:predict_fire: IBM ML analytics "
                 "request for user (%s, %s)", user.user_id, user.user_name)

        input_data_df = self.preprocess([input_data])


        try:
            with open(self.watson_model_pickle_mod, "rb") as model_file:
                model_reqs = pickle.load(model_file)

            with open(self.watson_model_pickle_col, "rb") as cols_file:
                columns_to_keep = pickle.load(cols_file)
        except Exception as e:
            LOG.exception("predict_fire: Exception during pickle file opening %s", e)

        minmax_scaler = model_reqs.get('min_max_scaler')
        temp_scaler = model_reqs.get('temp_std_scaler')
        summary_one_hot_encoder = model_reqs.get('summary_one_hot_encoder')
        column_mean = model_reqs.get('column_means')

        if set(['summary']).issubset(input_data_df.columns):
            summary_one_hot_encoded = pd.get_dummies(input_data_df.summary)
            input_data_df.drop(columns=['summary'], axis=1, inplace=True)
            input_data_df = input_data_df.join(summary_one_hot_encoded)

        input_data_df[
            ['cloudCover', 'dewPoint', 'hour', 'humidity', 'monthofyear', 'ozone', 'precipProbability', 'pressure',
             'uvIndex', 'visibility', 'windBearing', 'windSpeed']] = minmax_scaler.fit_transform(input_data_df[
                                            ['cloudCover', 'dewPoint', 'hour', 'humidity', 'monthofyear', 'ozone',
                                             'precipProbability', 'pressure', 'uvIndex', 'visibility', 'windBearing',
                                             'windSpeed']])
        input_data_df[['temperature']] = temp_scaler.transform(input_data_df[['temperature']])

        cols_missing = list(set(columns_to_keep) - set(input_data_df.columns))

        for col in cols_missing:
            input_data_df[col] = 0

        input_data_df = input_data_df[columns_to_keep]
        input_data_df.fillna(column_mean, inplace=True)

        y_pred = self.model.predict(input_data_df)

        return y_pred

def get_analytics_helper():
    config = c_utils.read_config()
    ibm_analytics_helper = None
    if config:
        path = ROOT_DIR + "/" + config.get("fire_model_path", DEFAULT_MODEL_PATH) \
               + config.get("fire_model_name", DEFAULT_MODEL_NAME)
        mod_path = ROOT_DIR + "/" + config.get("fire_model_path", DEFAULT_MODEL_PATH) \
               + config.get("fire_model_pickle_mod", DEFAULT_MOD_PICK__NAME)
        col_path = ROOT_DIR + "/" + config.get("fire_model_path", DEFAULT_MODEL_PATH) \
               + config.get("fire_model_pickle_col", DEFAULT_COL_PICK_NAME)
        ibm_analytics_helper = IBMWatsonMLAnalytics(path, mod_path, col_path)
    return ibm_analytics_helper