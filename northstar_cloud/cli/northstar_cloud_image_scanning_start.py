import os

from northstar_cloud.common import logs as logging
from northstar_cloud.common import utils as c_utils
from northstar_cloud.services import northstar_image_scanning_service as ns_services

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

DEFAULT_FILE_PATH = "etc/northstar-service-config.json"
ROOT_DIR = os.path.abspath(os.curdir)
log_file_path = ROOT_DIR + "/" + DEFAULT_FILE_PATH


LOG = logging.getLogger(__name__)


def run():
    image_scan_config = c_utils.read_json_file(log_file_path)
    scan_service = ns_services.NorthStarImageScanning(image_scan_config)
    scan_service.run()

run()