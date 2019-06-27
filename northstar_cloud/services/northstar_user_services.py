import base64

from northstar_cloud.common import logs as logging
from northstar_cloud.api import northstar_pb2_grpc, northstar_pb2
from northstar_cloud.db import north_star_db_helper as ns_helper
from northstar_cloud.services.ibm_cloud_services import ibm_visual_rec_services
from northstar_cloud.common import exceptions as ns_exceptions

from northstar_cloud.common import utils as c_utils


LOG = logging.getLogger(__name__)

class NorthStarServicer(
    northstar_pb2_grpc.NorthStarServiceServicer
):
    """Provides methods that implement functionality
    of northstar service cloud server."""

    def __init__(self):
        self.ns_service = ns_helper.NorthStarService()
        self.ns_analytics = ibm_visual_rec_services.AnalyticsHelper()\
            .get_analytics_instance()

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


    def _reply_user(self, db_user):
        if db_user:
            rescue_locations = []
            if db_user.user_rescue_locations:
                rescue_locations = [northstar_pb2.LatLng(latitude=float(each_loc.lat), longitude=float(each_loc.lang))
                                    for each_loc in db_user.user_rescue_locations.rescue_locations]
            user_reply = northstar_pb2.GetUserReply(
                user=northstar_pb2.User(
                    user_id = str(db_user.user_id),
                    user_name = str(db_user.user_name),
                    first_name = str(db_user.first_name),
                    last_name = str(db_user.last_name),
                    phone_number = str(db_user.phone_number),
                    home_address = str(db_user.home_address),
                    email_address = str(db_user.email_address),
                    office_address = str(db_user.office_address),
                    app_id = str(db_user.app_id),
                    app_type = str(db_user.app_type),
                    last_updated = str(db_user.last_updated),
                    created_at = str(db_user.created_at),
                    health_info = northstar_pb2.HealthInfo(
                        need_medical_support = bool(
                            db_user.health_info.need_medical_support
                        )
                    ),
                    current_location=northstar_pb2.LatLng(
                        latitude=float(db_user.curr_location.lat),
                        longitude=float(db_user.curr_location.lang)
                    ),
                    rescue_locations = rescue_locations
                )
            )
            return user_reply
        return northstar_pb2.GetUserReply()

    def GetUser(self, request, context):
        LOG.info("northstar_service:GetUser for "
                 "user_id: %s user_name %s app_id %s",
                 request.user_id, request.user_name, request.app_id)
        user_id = None
        user_name = None
        app_id=None

        if request.user_id:
            user_id = request.user_id

        if request.user_name:
            user_name = request.user_name

        if request.app_id:
            app_id = request.app_id

        user = self.ns_service.get_user(user_id=user_id, user_name=user_name, app_id=app_id)
        return self._reply_user(user)

    def UpdateUser(self, request, context):
        pass

    def DeleteUser(self, request, context):
        pass

    def UploadImage(self, request, context):
        LOG.info("northstar_service:UploadImage for "
                 "User: %s image_name %s",
                 request.user, request.image_name)
        user_id = None
        user_name = None

        if request.user.user_id:
            user_id = request.user.user_id

        if request.user.user_name:
            user_name = request.user.user_name

        success = self.ns_service.store_image(
            image_name=request.image_name,
            image_type=c_utils.get_file_type_name(request.image_format),
            image_encode=request.image,
            user_name=user_name,
            user_id=user_id
        )
        return northstar_pb2.UploadImageReply(success=success)

    def _reply_image(self, image):
        if image:
            image_reply = northstar_pb2.GetImageReply(
                image_id=image.image_id,
                image_name=image.image_name,
                image_format=c_utils.get_file_type_pb2(image.image_type),
                image=image.image_encode,
                user=northstar_pb2.User(
                    user_id=image.user.user_id,
                    user_name=image.user.user_name)
            )
            return image_reply
        return northstar_pb2.GetImageReply()


    def _predict_fire(self, image):
        LOG.info("_predict_fire: calling IBM analytics")
        classes = self.ns_analytics.predict_fire(
            images_filename=image.image_name,
            image_bytecode=base64.decodebytes(image.image_encode))
        return classes


    def GetImage(self, request, context):
        LOG.info("northstar_service:GetImage for "
                 "image_id: %s image_name %s",
                 request.image_id, request.image_name)
        image_id = None
        image_name = None
        if request.image_id:
            image_id = request.image_id

        if request.image_name:
            image_name = request.image_name

        if not image_id or not image_name:
            raise ns_exceptions.ImageNameNotProvided()

        image = self.ns_service.get_image(image_id=image_id, image_name=image_name)
        return self._reply_image(image)
