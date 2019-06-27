import json

from ibm_watson import VisualRecognitionV3
from ibm_watson import ApiException

from northstar_cloud.common import logs as logging
from northstar_cloud.common import utils as c_utils

LOG = logging.getLogger(__name__)

class NorthStarWatson(object):
    def __init__(self, watson_api_version, watson_api_key, classifier_ids):
        self.watson_api_version = watson_api_version
        self.watson_api_key = watson_api_key
        self.classifier_ids = classifier_ids
        self.visual_recognition = None
        try:
            self.visual_recognition = VisualRecognitionV3(
                version=self.watson_api_version,
                iam_apikey=self.watson_api_key
            )
            self.visual_recognition.disable_SSL_verification()
        except ApiException as ex:
            LOG.exception("NorthStarWatson:__init__ Failed to connect watson "
                          "visual recognition with %s", ex)


    def predict_fire(self, images_filename, image_bytecode):
        LOG.info("NorthStarWatson:predict_fire: IBM VR analytics request for image %s", images_filename)
        classes = None
        if self.visual_recognition:
            classes = self.visual_recognition.classify(
                images_file=image_bytecode,
                images_filename=images_filename,
                threshold='0.6',
                owners=["me"],
                classifier_ids = self.classifier_ids
            ).get_result()
            LOG.info("NorthStarWatson:predict_fire: IBM VR analytics responce %s", json.dumps(classes, indent=2))
        return classes


class AnalyticsHelper(object):
    def __init__(self):
        self.north_star_watson = None

    def get_analytics_instance(self):
        read_config = c_utils.read_config()
        self.north_star_watson = NorthStarWatson(
            read_config['iam_vr_version'],
            read_config['iam_vr_apikey'],
            read_config['iam_classifier_ids']
        )
        return self.north_star_watson