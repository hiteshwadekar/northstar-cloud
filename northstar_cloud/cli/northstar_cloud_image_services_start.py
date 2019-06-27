from northstar_cloud.common import logs as logging
from northstar_cloud.common import utils as c_utils
from northstar_cloud.services import northstar_image_scanning_service as ns_services

LOG = logging.getLogger(__name__)


def run():
    image_scan_config = c_utils.read_config()
    scan_service = ns_services.NorthStarImageScanning(image_scan_config)
    scan_service.run()

run()