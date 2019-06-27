import threading
import time
import os
import base64

from northstar_cloud.db import north_star_service_helper as ns_db_helper
from northstar_cloud.common import logs as logging
from northstar_cloud.services import northstar_watson_services
from northstar_cloud.common import utils as c_utils

LOG = logging.getLogger(__name__)

DEFAULT_FILE_PATH = "etc/northstar-service-config.json"
ROOT_DIR = os.path.abspath(os.curdir)
log_file_path = ROOT_DIR + "/" + DEFAULT_FILE_PATH



class NorthStarImageScanning(object):
    def __init__(self, image_scan_config):
        self.image_scan_config = image_scan_config
        self.scan_interval = image_scan_config.get('image_scan_interval', 10)
        self._ns_stop = False
        self._ns_stopped = threading.Event()
        self.ns_analytics = northstar_watson_services.AnalyticsHelper() \
            .get_analytics_instance()
        self.db = None
        self.users_fire_range = image_scan_config.get('users_fire_range', 10)

    def stop(self, timeout=None):
        self._ns_stop = True
        self._ns_stopped.wait(timeout)

    def run(self):
        self._stop = False
        try:
            while not self._ns_stop:
                try:
                    self.db = ns_db_helper.NorthStarService()
                    self.scan_recently_uploaded_images()
                except Exception:
                    LOG.exception('NorthStarImageScanning:FailedToRunThread')
                time.sleep(self.scan_interval)
        finally:
            self._ns_stopped.set()


    def _get_users_from_fire_range(self, fire_lat, fire_long):
        affected_users = []
        users = self.db.get_all_users()
        if users:
            for user in users:
                fire_range = c_utils.get_distqance_bet_two_points_using_haversine(
                    fire_lat, fire_long, user.curr_location.lat, user.curr_location.lang
                )
                LOG.info("_get_users_from_fire_range: User ({0}, {1}, {2}, {3}) is {4} "
                         "miles away from fire at ({5}, {6})"
                         .format(
                    user.user_name,
                    user.user_id,
                    user.curr_location.lat,
                    user.curr_location.lang,
                    fire_range,
                    fire_lat,
                    fire_long)
                )
                if fire_range in range(0, self.users_fire_range):
                    affected_users.append(user)
        return affected_users


    def notify_users(self, fire_location):
        need_notify_users = self._get_users_from_fire_range(
            fire_location.lat, fire_location.lang)
        return need_notify_users

    def calculate_safe_location(self):
        pass

    def _predict_fire(self, image):
        LOG.info("_predict_fire: calling IBM analytics")
        classes = self.ns_analytics.predict_fire(
            images_filename=image.image_name,
            image_bytecode=base64.decodebytes(image.image_encode))
        return classes

    def scan_recently_uploaded_images(self):
        LOG.info("scan_recently_uploaded_images: Scanning images for detecting fire... ")
        images = self.db.get_images_to_scan()
        if images:
            for image in images:
                try:
                    # Uncomment below line, when we want to test to see real product
                    # by commenting we are saving API calls (free limit).
                    # classes = self._predict_fire(image)
                    classes = {'images': [{'classifiers': [{'classifier_id': 'DefaultCustomModel_2080973559', 'name':
                        'Default Custom Model', 'classes': [{'class': 'wildfire', 'score': 0.767}]}],
                                           'image': 'fire_burned.jpg'}], 'images_processed': 1, 'custom_classes': 2}
                    if classes:
                        fire_enum = c_utils.get_classification_for_image(classes, image.image_name)
                        if fire_enum and fire_enum.name == "FIRE":
                            LOG.info("scan_recently_uploaded_images: -DETECETED FIRE---- at location latitude %s, longitude %s-> ",
                                     image.user.curr_location.lat, image.user.curr_location.lang)
                            LOG.info("scan_recently_uploaded_images: Notify users within 10 miles range from above location latitude %s, longitude %s",
                                     image.user.curr_location.lat, image.user.curr_location.lang)
                            need_notify_users = self.notify_users(image.user.curr_location)
                            if need_notify_users:
                                LOG.info(
                                    "scan_recently_uploaded_images: These users %s could affect fire from location latitude %s, longitude %s",
                                    [(user.user_id, user.user_name) for user in need_notify_users], image.user.curr_location.lat, image.user.curr_location.lang)
                            self.db.update_image(image, is_wild_fire=True, recognition_flag=True)
                        else:
                            continue
                except Exception as e:
                    LOG.info("scan_recently_uploaded_images: exception %s occurred while scanning image. ", e)
                    continue
        else:
            LOG.info("scan_recently_uploaded_images: No images found to scan..")
