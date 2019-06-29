import json

from northstar_cloud.common import logs as logging
from northstar_cloud.common import utils as c_utils

LOG = logging.getLogger(__name__)

class NorthStarIBMGeospatial(object):
    def __init__(self, watson_api_version, watson_api_key, classifier_ids):
        self.geo_api_version = watson_api_version
        self.geo_api_key = watson_api_key

    def register_users_geoservice(self, users):
        LOG.info("NorthStarIBMGeospatial:register_users_geoservice: Register Users in Geospatial services %s", users)
        success = False

        return success

    def start_geospatial_service(self):
        LOG.info("NorthStarIBMGeospatial:start_geospatial_service: Starting geospatial servics.")
        success = False

        return success

    def add_geospatial_fire_region(self, fire_region_name, fire_location):
        LOG.info("NorthStarIBMGeospatial:add_geospatial_fire_region: Adding geospatial fire region %s", fire_location)
        success = False

        return success

    def remove_geospatial_fire_region(self, fire_region_name):
        LOG.info("NorthStarIBMGeospatial:remove_geospatial_fire_region: "
                 "Removing geospatial fire region %s", fire_region_name)
        success = False

        return success

    def geospatial_fire_region(self):
        LOG.info("NorthStarIBMGeospatial:geospatial")
        success = False

        return success


def get_geospatial_instance(self):
    read_config = c_utils.read_config()
    self.north_star_geo = NorthStarIBMGeospatial(
        read_config['iam_vr_version'],
        read_config['iam_vr_apikey'],
        read_config['iam_classifier_ids']
    )
    return self.north_star_geo