import threading
import time
import base64

from northstar_cloud.db import north_star_db_helper as ns_db_helper
from northstar_cloud.common import logs as logging
from northstar_cloud.services.ibm_cloud_services import ibm_watson_ml_services
from northstar_cloud.services.ibm_cloud_services import ibm_weather_services
from northstar_cloud.common import utils as c_utils

LOG = logging.getLogger(__name__)

class NorthStarUserMlService(object):
    def __init__(self, user_ml_config):
        self.user_ml_config = user_ml_config

        # Default user ml scal interval an hour
        self.user_ml_scan_interval = self.user_ml_config.get('user_ml_scan_interval', 60000)
        self._ns_stop = False
        self._ns_stopped = threading.Event()

        self.ns_analytics = ibm_watson_ml_services.get_analytics_helper()
        self.db = None
        self.users_fire_range = self.user_ml_config.get('users_fire_range', 10)
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
                    self.weather_ml_analysis_job()
                except Exception:
                    LOG.exception('NorthStarImageScanning:FailedToRunThread')
                time.sleep(self.user_ml_scan_interval)
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

    def calculate_safe_location(self):
        pass

    def get_user_location_weather(self, user_location):
        weather_data = {}
        if user_location:
            weather_data = self.ibm_weather_service.get_hourly_forecast(
                user_location.lat,
                user_location.lang
            )
        return weather_data

    def _predict_fire(self, user):
        LOG.info("_predict_fire: calling IBM ML analytics service.")
        possible_fire = False

        user_weather_data = self.get_user_location_weather(user.curr_location)
        possible_fire = self.ns_analytics.predict_fire(user, user_weather_data)

        return possible_fire, user_weather_data

    def weather_ml_analysis_job(self):
        LOG.info("weather_ml_analysis_job: checking weather fire patterns.")
        users = self.db.get_all_users()
        if users:
            for user in users:
                try:
                    possible_fire, user_weather_data = self._predict_fire(user)
                    if possible_fire:
                        LOG.info(
                            "weather_ml_analysis_job: -PREDICTED FIRE CONDITION ---- at location latitude %s, longitude %s-> ",
                            user.curr_location.lat, user.curr_location.lang)

                        LOG.info("weather_ml_analysis_job: User weather data: %s", user_weather_data)

                        LOG.info("weather_ml_analysis_job: Notify users within 10 miles range from location latitude %s, longitude %s",
                                 user.curr_location.lat, user.curr_location.lang)
                        need_notify_users = self.notify_users(user.curr_location)
                        if need_notify_users:
                            LOG.info(
                                "weather_ml_analysis_job: Notifying these users %s  for possible fire condition at latitude %s, longitude %s",
                                    [(user.user_id, user.user_name) for user in need_notify_users], user.curr_location.lat, user.curr_location.lang)
                        else:
                            continue
                    else:
                        LOG.info("weather_ml_analysis_job: No user found to to check weather fire pattern ..")
                except Exception as e:
                    LOG.info("weather_ml_analysis_job: exception %s occurred while predicting fire condition. ", e)
                    continue
        else:
            LOG.info("weather_ml_analysis_job: No user found to to check weather fire pattern ..")
