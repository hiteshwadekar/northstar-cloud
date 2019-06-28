from northstar_cloud.common import logs as logging
from northstar_cloud.common import utils as c_utils
from northstar_cloud.services import northstar_user_ml_analytics_service as ns_ml_services

LOG = logging.getLogger(__name__)


def run():
    user_ml_config = c_utils.read_config()
    scan_service = ns_ml_services.NorthStarUserMlService(user_ml_config)
    scan_service.run()

run()