import threading
import time
import base64

from northstar_cloud.db import north_star_db_helper as ns_db_helper
from northstar_cloud.common import logs as logging
from northstar_cloud.services.ibm_cloud_services import ibm_visual_rec_services
from northstar_cloud.services.ibm_cloud_services import ibm_weather_services
from northstar_cloud.common import utils as c_utils

LOG = logging.getLogger(__name__)


class NorthStarImageScanning(object):
    def __init__(self, image_scan_config):
        self.image_scan_config = image_scan_config
        self.scan_interval = image_scan_config.get('image_scan_interval', 10)
        self._ns_stop = False
        self._ns_stopped = threading.Event()
        self.ns_analytics = ibm_visual_rec_services.AnalyticsHelper() \
            .get_analytics_instance()
        self.db = None
        self.users_fire_range = image_scan_config.get('users_fire_range', 10)
        self.ibm_weather_service = ibm_weather_services.IBMWeatherServices()

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
                fire_range = c_utils.get_distance_bet_two_points_using_haversine(
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

    def get_safe_location(self, wind_dir, user_location):
        # Calculating safe routes from away wind direction from fire.
        safe_lat, safe_log = c_utils.get_safe_points(
            wind_dir=wind_dir,
            user_lat=float(user_location.lat),
            user_long=float(user_location.lang)
        )

        return safe_lat, safe_log

    def get_hospitals_location(self, fire_wind_dir, user_location):
        # Get hospitals from near user location
        hospital_lat, hospital_log = c_utils.get_hospitals_point(
            wind_dir=fire_wind_dir,
            user_lat=float(user_location.lat),
            user_long=float(user_location.lang)
        )

        return hospital_lat, hospital_log


    def get_wind_direction(self, fire_location):
        # Getting wind direction  from fire location
        wind_direction_data = {}
        if fire_location:
            wind_direction_data = self.ibm_weather_service.get_current_forecast(
                fire_location.lat,
                fire_location.lang
            )
        return wind_direction_data

    def get_users_in_path_wind_direction(self, fire_location):
        users = self.db.get_all_users()
        wind_path_users = []
        safe_locations = []
        hospital_locations = []
        for user in users:
            fire_wind_direction_data = self.get_wind_direction(fire_location)
            if fire_wind_direction_data and \
                    self.image_scan_config['wdir'] in fire_wind_direction_data and \
                    self.image_scan_config['wdir_cardinal'] in fire_wind_direction_data:
                diff_wdir_cardinal = c_utils.calculate_compass_bearing(
                    user.curr_location.lat,
                    user.curr_location.lang,
                    fire_location.lat,
                    fire_location.lang
                )
                # if fire_location and user location in cardinal if wind direction
                if int(diff_wdir_cardinal) in range(0, 91):
                    wind_path_users.append(user)

                    safe_lat, safe_long = self.get_safe_location(fire_wind_direction_data['wdir'], user.curr_location)
                    safe_locations.append((safe_lat, safe_long))

                    hos_lat, hos_long = self.get_hospitals_location(fire_wind_direction_data['wdir'], user.curr_location)
                    safe_locations.append((hos_lat, hos_long))

        return wind_path_users, safe_locations, hospital_locations

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
                            LOG.info("scan_recently_uploaded_images: - DETECTED FIRE USING IMAGE UPLOADED BY USER ---- @(latitude %s, longitude %s) ",
                                     image.user.curr_location.lat, image.user.curr_location.lang)

                            LOG.info("weather_ml_analytics_job: Searching for users within 10 miles for notification.")

                            need_notify_users = self.notify_users(image.user.curr_location)
                            if need_notify_users:
                                LOG.info(
                                    "scan_recently_uploaded_images: ALERT USERS %s THAT THEY ARE NEAR WILDFIRE. "
                                    "GET READY FOR POSSIBLE EVACUATION. WILL ALERT WHEN EVACUATION NEEDED.",
                                    [(user.user_id, user.user_name) for user in need_notify_users])


                            #TODO Get the safe points too
                            notifying_user_in_wind_direction, safe_locations, hospital_locations = self.get_users_in_path_wind_direction(image.user.curr_location)
                            if notifying_user_in_wind_direction:
                                for user in notifying_user_in_wind_direction:

                                    if user.health_info.need_medical_support:
                                        LOG.info(
                                            "scan_recently_uploaded_images: ALERT USERS WITH MEDICAL NEED (%s , %s) TO EVACUATE IMMEDIATELY TO HOSPITAL %s."
                                            "WILDFIRE IS APPROACHING",
                                            user.user_id, user.user_name, hospital_locations
                                        )
                                    else:
                                        LOG.info(
                                            "scan_recently_uploaded_images: ALERT USERS (%s , %s) TO EVACUATE IMMEDIATELY TO SAFE LOCATION %s. "
                                            "WILDFIRE IS APPROACHING",
                                            user.user_id, user.user_name, safe_locations
                                        )
                            self.db.update_image(image, is_wild_fire=True, recognition_flag=True)
                        else:
                            continue
                except Exception as e:
                    LOG.info("scan_recently_uploaded_images: exception %s occurred while scanning image. ", e)
                    continue
        else:
            LOG.info("scan_recently_uploaded_images: No images found to scan..")
