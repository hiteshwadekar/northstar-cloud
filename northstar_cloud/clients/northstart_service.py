import grpc
import argparse
import os

from northstar_cloud.api import northstar_pb2_grpc
from northstar_cloud.api import northstar_pb2

from northstar_cloud.common import logs as logging
from northstar_cloud.common import utils as c_utils

LOG = logging.getLogger(__name__)

DEFAULT_FILE_PATH = "etc/northstar-service-config.json"
DEFAULT_BIND = '[::]:50051'
DEFAULT_LOCALHOST_ADDRESS = "localhost:50051"


class NorthStar(object):
    def __init__(self, endpoint):
        self.channel = grpc.insecure_channel(endpoint)
        self.stub = northstar_pb2_grpc.NorthStarServiceStub(
            self.channel
        )

    def send_request(self, req, func):
        LOG.info("northstar-service-client: Request :%s", req)
        method = getattr(self.stub, func)
        try:
            resp = method(req)
        except Exception as e:
            LOG.error(
                "Failed to send request "
                "with error :%s" % (e)
            )
            raise
        LOG.info("northstar-service-client: Response :%s", resp)
        return resp

    def cleanup(self):
        if self.channel:
            self.channel.close()

def prepare_add_user(app_id='test1', app_type='iOS'):
    add_user_req = northstar_pb2.AddUserRequest()

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


def read_config():
    config = {}
    config = c_utils.read_json_file(log_file_path)
    global DEFAULT_BIND
    global DEFAULT_LOCALHOST_ADDRESS

    if 'bind ' in config.keys():
        DEFAULT_BIND = config['bind']

    if 'default_local_address' in config.keys():
        DEFAULT_LOCALHOST_ADDRESS = config['default_local_address']


def main():
    program_args = get_program_args()
    input_file = os.path.abspath(program_args.user_info_file)
    client = NorthStar(DEFAULT_LOCALHOST_ADDRESS)

    if input_file:
        user_info_dict = parse_user_info(input_file)
        req = prep_user_request(user_info_dict)
        resp = client.send_request(req, "AddUser")
        print("\n")
        print("NorthStar-Cloud: OUTPUT")
        print("NorthStar-Cloud: %s", resp)


def prep_user_request(user_info_dict):
    lat_lan_req = northstar_pb2.LatLng(latitude=float(user_info_dict['curr_lat']),
                                       longitude=float(user_info_dict['curr_lang']))

    health_info_req = northstar_pb2.HealthInfo(need_medical_support=False)
    if user_info_dict['need_medical_emegency']:
        health_info_req = northstar_pb2.HealthInfo(need_medical_support=True)

    user = northstar_pb2.User(user_name=user_info_dict['user_name'],
                                  first_name=user_info_dict['first_name'],
                                  last_name=user_info_dict['last_name'],
                                  phone_number=user_info_dict['phone_number'],
                                  home_address=user_info_dict['home_address'],
                                  email_address=user_info_dict['email_address'],
                                  office_address=user_info_dict['office_address'],
                                  app_id=user_info_dict['app_id'],
                                  app_type=user_info_dict['app_type'],
                                  current_location=lat_lan_req,
                                  health_info=health_info_req
                                  )
    user_req = northstar_pb2.AddUserRequest(user=user)
    return user_req

def parse_user_info(user_input_file):
    user_info_list = c_utils.read_json_file(user_input_file, LOG)
    return user_info_list

def get_program_args():
    """
    Construct and parse the
    command line arguments to the program.
    """
    parser = argparse.ArgumentParser(
        description='NorthStar cloud tools.'
    )
    parser.add_argument(
        'user_info_file',
        help='Path to user information json format file.'
    )
    return parser.parse_args()

if __name__ == '__main__':
    main()