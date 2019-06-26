import grpc
import argparse
import os
import base64

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


def read_config():
    config = {}
    config = c_utils.read_json_file(log_file_path)
    global DEFAULT_BIND
    global DEFAULT_LOCALHOST_ADDRESS

    if 'bind ' in config.keys():
        DEFAULT_BIND = config['bind']

    if 'default_local_address' in config.keys():
        DEFAULT_LOCALHOST_ADDRESS = config['default_local_address']


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

def upload_file_request(upload_file_dict):
    upload_file_req = None
    if upload_file_dict:
        user = northstar_pb2.User()
        if upload_file_dict.get("user_id"):
            user.user_id = upload_file_dict.get("user_id")

        if upload_file_dict.get("user_name"):
            user.user_name = upload_file_dict.get("user_name")

        encoded_string = None
        with open(upload_file_dict["image_path"], "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        upload_file_req = northstar_pb2.UploadImageRequest(
            image_name = upload_file_dict.get('image_name'),
            image_format=northstar_pb2.JPEG,
            image = encoded_string,
            user=user
        )
    return upload_file_req

def get_file_request(get_file_dict):
    get_file_req = None
    if get_file_dict:
        get_file_req = northstar_pb2.GetImageRequest(
            image_name = get_file_dict.get('image_name'),
            image_id=get_file_dict.get('image_id')
        )
    return get_file_req

def get_user_request(get_user_dict):
    get_user_req = None
    if get_user_dict:
        get_user_req = northstar_pb2.GetUserRequest(
            user_id = get_user_dict.get('user_id', None),
            user_name = get_user_dict.get('user_name', None),
            app_id = get_user_dict.get('app_id', None)
        )
    return get_user_req

def get_file_responce(get_file_resp, get_file_dict):
    if get_file_resp:
        image_name = get_file_resp.image_name
        image_type = c_utils.get_file_type_name(get_file_resp.image_format)

        if image_type == "JPEG":
            image_name = image_name + "_download.jpg"

        if image_type == "PNG":
            image_name = image_name + "_download.png"

        image_name = get_file_dict["image_path"] + image_name
        print(image_name)
        try:
            with open(image_name, "wb") as image_write:
                image_write.write(base64.decodebytes(get_file_resp.image))
        except Exception as e:
            LOG.exception("get_file_responce: Error %s", e)

def parse_user_info(user_input_file):
    user_info_dict = c_utils.read_json_file(user_input_file, LOG)
    return user_info_dict

def parse_upload_file_info(upload_input_file):
    upload_file_dict = c_utils.read_json_file(upload_input_file, LOG)
    return upload_file_dict

def parse_get_file_info(get_input_file):
    get_file_dict = c_utils.read_json_file(get_input_file, LOG)
    return get_file_dict


def get_program_args():
    """
    Construct and parse the
    command line arguments to the program.
    """
    parser = argparse.ArgumentParser(
        description='NorthStar cloud tools.'
    )
    parser.add_argument(
        '-user_info_file',
        action='store',
        help='Path to user information json format file.',
        default=False
    )
    parser.add_argument(
        '-get_user_info_file',
        action='store',
        help='Path to get user information json format file.',
        default=False
    )
    parser.add_argument(
        '-upload_file',
        action='store',
        help='Path to user information json format file.',
        default=False
    )
    parser.add_argument(
        '-get_file',
        action='store',
        help='Path to user information json format file.',
        default=False
    )
    return parser.parse_args()

def main():
    program_args = get_program_args()
    client = NorthStar(DEFAULT_LOCALHOST_ADDRESS)

    if program_args.user_info_file:
        input_file = os.path.abspath(program_args.user_info_file)
        if input_file:
            user_info_dict = parse_user_info(input_file)
            req = prep_user_request(user_info_dict)
            resp = client.send_request(req, "AddUser")
            print("\n")
            print("NorthStar-Cloud: OUTPUT")
            print("NorthStar-Cloud: AddUser %s", resp)

    if program_args.upload_file:
        upload_file = os.path.abspath(program_args.upload_file)
        if upload_file:
            user_info_dict = parse_upload_file_info(upload_file)
            req = upload_file_request(user_info_dict)
            resp = client.send_request(req, "UploadImage")
            print("\n")
            print("NorthStar-Cloud: OUTPUT")
            print("NorthStar-Cloud: UploadFile resp -> %s", resp)

    if program_args.get_file:
        get_file_info = os.path.abspath(program_args.get_file)
        if get_file_info:
            get_info_dict = parse_get_file_info(get_file_info)
            req = get_file_request(get_info_dict)
            resp = client.send_request(req, "GetImage")
            get_file_responce(resp, get_info_dict)
            print("\n")
            print("NorthStar-Cloud: OUTPUT")
            print("NorthStar-Cloud: GetImage resp -> %s", resp)

    if program_args.get_user_info_file:
        get_user_info = os.path.abspath(program_args.get_user_info_file)
        if get_user_info:
            get_user_dict = parse_user_info(get_user_info)
            req = get_user_request(get_user_dict)
            resp = client.send_request(req, "GetUser")
            print("\n")
            print("NorthStar-Cloud: OUTPUT")
            print("NorthStar-Cloud: GetUser resp -> %s", resp)


if __name__ == '__main__':
    main()