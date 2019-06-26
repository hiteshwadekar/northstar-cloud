import threading
import time
import os
import base64

from northstar_cloud.db import north_star_service_helper as ns_helper
from northstar_cloud.common import logs as logging
from northstar_cloud.services import northstar_watson_services

LOG = logging.getLogger(__name__)

DEFAULT_FILE_PATH = "etc/northstar-service-config.json"
ROOT_DIR = os.path.abspath(os.curdir)
log_file_path = ROOT_DIR + "/" + DEFAULT_FILE_PATH



class NorthStarImageScanning(object):
    def __init__(self, image_scan_config):
        self.image_scan_config = image_scan_config
        self.scan_interval = image_scan_config.get('image_scan_interval', 2)
        self._ns_stop = False
        self._ns_stopped = threading.Event()
        self.ns_analytics = northstar_watson_services.AnalyticsHelper() \
            .get_analytics_instance()

    def stop(self, timeout=None):
        self._ns_stop = True
        self._ns_stopped.wait(timeout)

    def run(self):
        self._stop = False
        try:
            while not self._ns_stop:
                try:
                    self.scane_recently_uploaded_images()
                except Exception:
                    LOG.exception('NorthStarImageScanning:FailedToRunThread')
                time.sleep(self.scan_interval)
        finally:
            self._ns_stopped.set()

    def _predict_fire(self, image):
        LOG.info("_predict_fire: calling IBM analytics")
        classes = self.ns_analytics.predict_fire(
            images_filename=image.image_name,
            image_bytecode=base64.decodebytes(image.image_encode))
        return classes

    def scane_recently_uploaded_images(self):
        LOG.info("scane_recently_uploaded_images: Scanning images for detecting fire ")
        images = ns_helper.get_images_to_scan()

        if images:
            for image in images:
                classes = self._predict_fire(image)




