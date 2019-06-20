from concurrent import futures
import time
import os
import grpc

from northstar_cloud.common import logs as logging
from northstar_cloud.common import utils as c_utils
from northstar_cloud.api import northstar_pb2_grpc
from northstar_cloud.services import northstar_service

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

LOG = logging.getLogger(__name__)
DEFAULT_FILE_PATH = "etc/northstar-service-config.json"
DEFAULT_BIND = '[::]:50051'
DEFAULT_LOCALHOST_ADDRESS = "localhost:50051"

ROOT_DIR = os.path.abspath(os.curdir)
log_file_path = ROOT_DIR + "/" + DEFAULT_FILE_PATH


def read_config():
    config = {}
    config = c_utils.read_json_file(log_file_path)
    global DEFAULT_BIND
    global DEFAULT_LOCALHOST_ADDRESS

    if 'bind ' in config.keys():
        DEFAULT_BIND = config['bind']

    if 'default_local_address' in config.keys():
        DEFAULT_LOCALHOST_ADDRESS = config['default_local_address']


def serve():
    read_config()
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10))
    northstar_pb2_grpc.add_NorthStarServiceServicer_to_server(
        northstar_service.NorthStarServicer(), server)
    LOG.info("northstar-cloud: service stating...")

    server.add_insecure_port(DEFAULT_BIND)
    try:
        server.start()
        LOG.info(
            "northstar-cloud: is runnnig "
            "at ... %s" % (DEFAULT_LOCALHOST_ADDRESS)
        )
    except Exception as e:
        LOG.info(
            "northstar-cloud: Failed to "
            "start with exception %s" % (e)
        )
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        LOG.info("northstar-cloud: stopped ")
        server.stop(0)


if __name__ == '__main__':
    serve()
