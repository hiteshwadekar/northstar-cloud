from concurrent import futures
import time
import os
import grpc

from detective_api.common import logs as logging
from detective_api.api.proto import detective_pb2
from detective_api.api.proto import detective_pb2_grpc
from detective_api.services.\
    detective_api_service import DetectiveApiService as dt_service
from detective_api.common import utils as c_utils

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

LOG = logging.getLogger(__name__)
DEFAULT_FILE_PATH = "minikube/detective-api-config.json"
DEFAULT_BIND = '[::]:50051'
DEFAULT_LOCALHOST_ADDRESS = "localhost:50051"

ROOT_DIR = os.path.abspath(os.curdir)
log_file_path = ROOT_DIR + "/" + DEFAULT_FILE_PATH


class DetectiveServiceServicer(
    detective_pb2_grpc.DetectiveServiceServicer
):
    """Provides methods that implement functionality
    of detective api server."""

    status_to_grpc = {
        c_utils.PossibleEvents.WITNESS_DECISION_CANT_DECIDE:
        detective_pb2.WITNESS_DECISION_CANT_DECIDE,
        c_utils.PossibleEvents.WITNESS_DECISION_PARTIAL_MERGE_POSSIBLE:
        detective_pb2.WITNESS_DECISION_PARTIAL_MERGE_POSSIBLE,
        c_utils.PossibleEvents.WITNESS_DECISION_NO_MERGE_POSSIBLE:
        detective_pb2.WITNESS_DECISION_NO_MERGE_POSSIBLE,
        c_utils.PossibleEvents.WITNESS_DECISION_MERGE_ALL_POSSIBLE:
        detective_pb2.WITNESS_DECISION_MERGE_ALL_POSSIBLE
    }

    def __init__(self):
        self.dt_service = dt_service()

    def _convert_grpc_wtness_req_to_local(self, witness_events):
        local_witness_events = []
        for each_list in witness_events:
            local_witness_events.append(each_list.name)
        return local_witness_events

    def _convert_local_wtness_rpl_to_grpc(self, witness_events):
        req_witness = detective_pb2.GetWitnessMergeReply()
        for each_item in witness_events:
            req_witness.witness_events.extend(
                [detective_pb2.WitnessEvents(name=each_item)]
            )
        return req_witness

    def GetWitnessMergeDecision(self, request, context):
        LOG.info("detetive-api:GetWitnessMergeDecision "
                 "witness-events: %s", request.witness_events)
        # Request recieved.
        witness_events = self._convert_grpc_wtness_req_to_local(
            request.witness_events
        )

        # Service call for decision making.
        self.dt_service.init_aggregate_witness_events(witness_events)
        possible_event_pred, wintess_possible_list = \
            self.dt_service.calculate_witness_merge()

        # Preparing reply
        rply_wintess_possible_merge = \
            self._convert_local_wtness_rpl_to_grpc(wintess_possible_list)
        rply_wintess_possible_merge.decision = \
            self.status_to_grpc[possible_event_pred]
        return rply_wintess_possible_merge


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
    detective_pb2_grpc.add_DetectiveServiceServicer_to_server(
        DetectiveServiceServicer(), server)
    LOG.info("detective-api: service stating...")

    server.add_insecure_port(DEFAULT_BIND)
    try:
        server.start()
        LOG.info(
            "detective-api: is runnnig "
            "at ... %s" % (DEFAULT_LOCALHOST_ADDRESS)
        )
    except Exception as e:
        LOG.info(
            "detective-api: Failed to "
            "start with exception %s" % (e)
        )
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        LOG.info("detective-api: stopped ")
        server.stop(0)


if __name__ == '__main__':
    serve()
