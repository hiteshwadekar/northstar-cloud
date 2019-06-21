import uuid

from northstar_cloud.db import clients
from northstar_cloud.db.models import northstar_db_model as ns_model

from northstar_cloud.common import logs as logging

LOG = logging.getLogger(__name__)

class NorthStarService(object):
    def __init__(self):
        try:
            self.db_client = clients.get_db_connection()
        except Exception as e:
            LOG.exception("NorthStarService:__init__: database connecting issue %s",e)

    def add_user(self, **kwargs):
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
            'curr_location': None,
            'health_info': None
        }

        if kwargs.get('user_id'):
            user_dict['user_id'] = kwargs.get('user_id')
        else:
            user_dict['user_id'] = str(uuid.uuid4())
        user_dict['user_name'] = kwargs.get('user_name', None)
        user_dict['first_name'] = kwargs.get('first_name', None)
        user_dict['last_name'] = kwargs.get('last_name', None)
        user_dict['phone_number'] = kwargs.get('phone_number', None)
        user_dict['home_address'] = kwargs.get('home_address', None)
        user_dict['email_address'] = kwargs.get('email_address', None)
        user_dict['office_address'] = kwargs.get('office_address', None)
        user_dict['app_id'] = kwargs.get('app_id', None)
        user_dict['app_type'] = kwargs.get('app_type', None)

        if kwargs['curr_location']:
            try:
                lat_lang = ns_model.LatLang(lat=float(kwargs['curr_location']['curr_lat']),
                                        lang=float(kwargs['curr_location']['curr_lang']))
                lat_lang.save()
                user_dict['curr_location'] = lat_lang
            except Exception as e:
                LOG.exception("add_user: failed to add user location %s", e)
                return False

        if kwargs['health_info']:
            try:
                health_info = ns_model.HealthInformation(
                    need_medical_support=bool(kwargs['health_info']['need_medical_emegency']))
                health_info.save()
                user_dict['health_info'] = health_info
            except Exception as e:
                LOG.exception("add_user: failed to add user health info %s", e)
                return False

        try:
            user = ns_model.User(**user_dict)
            user.save()
        except Exception as e:
            LOG.exception("add_user: failed to add user %s", e)
            return False
        return True

    def get_user(self, user_id):
        pass

    def update_user(self, update_user_request):
        pass

    def get_user_rescue_locations(self, user_id):
        pass

    def store_image(self, user_id, image_name, image_type, image_encode, user_name=None, image_id=None):
        try:
            if user_name:
                user = ns_model.User.objects(user_name=user_name).first()
            elif user_id:
                user = ns_model.User.objects(user_id=user_id).first()
            else:
                LOG.exception("store_image: requierd user to store image %s", user_id)
                return False

            if not user:
                LOG.exception("store_image: failed to get user %s", user_id)
                return False
            if not image_id:
                image_id = str(uuid.uuid4())
            image = ns_model.Images(user=user, image_id=image_id,
                                    image_name=image_name, image_type=image_type, image_encode=image_encode)
            image.save()
        except Exception as e:
            LOG.exception("store_image: failed to store image %s", e)
            return False
        return True

    def get_image(self, image_id=None, image_name=None):
        image = None
        try:
            if image_id:
                image = ns_model.Images.objects(image_id=image_id).first()
            elif image_name:
                image = ns_model.Images.objects(image_name=image_name).first()
            else:
                LOG.exception("get_image: requierd either image_id or image_name to get image ")
        except Exception as e:
            LOG.exception("get_image: failed to get image %s", e)
        return image

    def get_user(self, user_id=None, user_name=None, app_id=None):
        user = None
        try:
            if user_id:
                user = ns_model.User.objects(user_id=user_id).first()
            elif user_name:
                user = ns_model.User.objects(user_name=user_name).first()
            elif app_id:
                user = ns_model.User.objects(app_id=app_id).first()
            else:
                LOG.exception("get_user: requierd either user_id or user_name or app_id to get user ")
        except Exception as e:
            LOG.exception("get_user: failed to get user %s", e)
        return user
