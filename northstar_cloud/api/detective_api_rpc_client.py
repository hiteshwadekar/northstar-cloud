from __future__ import print_function
import argparse
import os
import grpc

from detective_api.common import logs as logging
from detective_api.api.proto import detective_pb2_grpc
from detective_api.api.proto import detective_pb2
from detective_api.common import utils as dt_utils


LOG = logging.getLogger(__name__)

DEFAULT_LOCALHOST_ADDRESS = "localhost:50051"
DEFAULT_FILE_PATH = "minikube/detective-api-config.json"
DEFAULT_BIND = '[::]:50051'

ROOT_DIR = os.path.abspath(os.curdir)
log_file_path = ROOT_DIR + "/" + DEFAULT_FILE_PATH


class Client(object):
    def __init__(self, endpoint):
        self.channel = grpc.insecure_channel(endpoint)
        self.stub = detective_pb2_grpc.DetectiveServiceStub(
            self.channel
        )

    def send_request(self, req, func):
        LOG.info("detective-api-client: Request :%s", req)
        method = getattr(self.stub, func)
        try:
            resp = method(req)
        except Exception as e:
            LOG.error(
                "Failed to send request "
                "with error :%s" % (e)
            )
            raise
        LOG.info("detective-api-client: Response :%s", resp)
        return resp

    def cleanup(self):
        if self.channel:
            self.channel.close()


def prepare_get_prediction(witness_list):
    req_witness = detective_pb2.GetWitnessMergeRequest()
    for each_item in witness_list:
        req_witness.witness_events.extend(
            [detective_pb2.WitnessEvents(name=each_item)]
        )
    return req_witness


def convert_grpc_wtness_req_to_local(witness_events):
    local_witness_events = []
    for each_list in witness_events:
        local_witness_events.append(each_list.name)
    return local_witness_events


decision_to_grpc_name = \
    {
        1: dt_utils.PossibleEvents.
        WITNESS_DECISION_MERGE_ALL_POSSIBLE.name,
        2: dt_utils.PossibleEvents.
        WITNESS_DECISION_PARTIAL_MERGE_POSSIBLE.name,
        3: dt_utils.PossibleEvents.
        WITNESS_DECISION_NO_MERGE_POSSIBLE.name,
        0: dt_utils.PossibleEvents.
        WITNESS_DECISION_CANT_DECIDE.name
    }


def read_config():
    config = {}
    config = dt_utils.read_json_file(log_file_path)
    global DEFAULT_BIND
    global DEFAULT_LOCALHOST_ADDRESS

    if 'bind ' in config.keys():
        DEFAULT_BIND = config['bind']

    if 'default_local_address' in config.keys():
        DEFAULT_LOCALHOST_ADDRESS = config['default_local_address']


def main():
    program_args = get_program_args()
    input_file = os.path.abspath(program_args.witnesses_input_file)
    client = Client(DEFAULT_LOCALHOST_ADDRESS)

    if input_file:
        witness_list = parse_witness_list(input_file)
        req = prepare_get_prediction(witness_list)
        resp = client.send_request(req, "GetWitnessMergeDecision")
        wintess_possible_list = convert_grpc_wtness_req_to_local(
            resp.witness_events
        )
        print("\n")

        print("detective-api: OUTPUT")
        print("detective-api: Witness "
              "events given input : %s " % witness_list)
        print("detective-api: Witness "
              "events prediction      "
              ": %s " % decision_to_grpc_name[resp.decision])
        print("detective-api: Witness "
              "events predicted list  "
              ": %s " % wintess_possible_list)


def parse_witness_list(witness_input_file):
    witness_event_list = dt_utils.read_json_file(witness_input_file, LOG)
    dt_utils.verify_witness_data_list_string_format(
        witness_event_list, LOG
    )
    return witness_event_list


def get_program_args():
    """
    Construct and parse the
    command line arguments to the program.
    """
    parser = argparse.ArgumentParser(
        description='Smart witness analysis tools.'
    )
    parser.add_argument(
        'witnesses_input_file',
        help='Path to list of witnesses events json format file.'
    )
    return parser.parse_args()


if __name__ == '__main__':
    main()
