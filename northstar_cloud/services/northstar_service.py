from northstar_cloud.common import logs as logging
from northstar_cloud.api import northstar_pb2_grpc, northstar_pb2
from northstar_cloud.db import north_star_service_helper as ns_helper

LOG = logging.getLogger(__name__)

class NorthStarServicer(
    northstar_pb2_grpc.NorthStarServiceServicer
):
    """Provides methods that implement functionality
    of northstar service cloud server."""

    def _validate_conv_grpc_user_req_to_dict(self, user_request):
        user_dict = {
            'user_id': None,
            'user_name': None,
            'first_name': None,
            'last_name': None,
            'phone_number': None,
            'home_address': None,
            'email_address': None,
            'office_address': None,
            'app_id': None,
            'app_type': None,
            'health_info': {
                'need_medical_emegency': False
            },
            'curr_location': {
                'curr_lat': None,
                'curr_lang': None
            }
        }

        if user_request.user_id:
            user_dict['user_id'] = user_request.user_id

        if user_request.user_name:
            user_dict['user_name'] = user_request.user_name

        if user_request.first_name:
            user_dict['first_name'] = user_request.first_name

        if user_request.last_name:
            user_dict['last_name'] = user_request.last_name

        if user_request.phone_number:
            user_dict['phone_number'] = user_request.phone_number

        if user_request.home_address:
            user_dict['home_address'] = user_request.home_address

        if user_request.email_address:
            user_dict['email_address'] = user_request.email_address

        if user_request.office_address:
            user_dict['office_address'] = user_request.office_address

        if user_request.app_id:
            user_dict['app_id'] = user_request.app_id

        if user_request.app_type:
            user_dict['app_type'] = user_request.app_type

        if user_request.current_location:
            user_dict['curr_location']['curr_lat'] = user_request.current_location.latitude
            user_dict['curr_location']['curr_lang'] = user_request.current_location.longitude

        if user_request.health_info:
            user_dict['health_info']['need_medical_emegency'] = \
                user_request.health_info.need_medical_support

        return user_dict

    def __init__(self):
        self.ns_service = ns_helper.NorthStarService()

    def GetRescuePoints(self, request, context):
        LOG.info("northstar_service:GetRescuePoints "
                 "currentLatLang: %s", request.currentLatLang)

        return northstar_pb2.GetRescuePointsReply()

    def AddUser(self, request, context):
        LOG.info("northstar_service:AddUser "
                 "User: %s", request.user)

        user_dict = self._validate_conv_grpc_user_req_to_dict(request.user)
        success = self.ns_service.add_user(**user_dict)

        return northstar_pb2.AddUserReply(success=success)

    def UpdateUser(self, request, context):
        pass

    def DeleteUser(self, request, context):
        pass

    def UploadImage(self, request, context):
        pass
