import datetime
from mongoengine import *

class LatLang(Document):
    lat = DecimalField(required=True)
    lang = DecimalField(required=True)


class HealthInformation(Document):
    need_medical_support = BooleanField()


class RescueLocation(Document):
    rescue_locations = ListField(ReferenceField(LatLang))


class User(Document):
    user_id = StringField(required=True)
    user_name = StringField(required=False, unique=True)
    first_name = StringField(required=False)
    last_name = StringField(required=False)
    phone_number = IntField(required=False, unique=True)
    home_address = StringField(required=False)
    email_address = EmailField(
        verbose_name="Email", unique=True, required=False)
    office_address = StringField(required=False)
    app_id = StringField(required=True, unique=True)
    app_type = StringField(required=True)
    last_updated = DateTimeField(default=datetime.datetime.now)
    curr_location = ReferenceField(LatLang, required=False)
    health_info = ReferenceField(HealthInformation, required=False)
    user_rescue_locations = ReferenceField(RescueLocation, required=False)
    created_at = DateTimeField(default=datetime.datetime.now)

    meta = {'collection': 'users', 'indexes': ['email_address', 'user_name', 'app_id']}


class Images(Document):
    user = ReferenceField(User, required=True)
    image_encode = BinaryField(required=True)
    image_id = StringField(required=True)
    image_name = StringField(required=True, unique=True)
    image_type = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    is_wild_fire = BooleanField(default=False)
    recognition_flag = BooleanField(default=False)
