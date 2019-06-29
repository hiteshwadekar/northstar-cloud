import json
import sys
from enum import Enum
from math import radians, cos, sin, asin, sqrt, atan2, degrees
from geopy.distance import geodesic
from northstar_cloud.api import northstar_pb2

class FileType(Enum):
    UNKNOWN = 0
    JPEG = 1
    PNG = 2

class Fire(Enum):
    NO = 0
    FIRE = 1
    CANT_SAY = 2


def get_file_type_name(file_type):
    if northstar_pb2.UNKNOWN:
        return FileType.UNKNOWN.name

    if northstar_pb2.JPEG:
        return FileType.JPEG.name

    if northstar_pb2.PNG:
        return FileType.PNG.name


def get_file_type_pb2(file_type_name):
    file_type_dict = {
        FileType.JPEG.name: northstar_pb2.JPEG,
        FileType.PNG.name: northstar_pb2.PNG,
        FileType.UNKNOWN.name: northstar_pb2.UNKNOWN
    }
    return file_type_dict.get(file_type_name, None)


def read_json_file(input_file, LOG=None):
    if input_file:
        try:
            with open(input_file, "r") as infile:
                return json.load(infile)
        except FileNotFoundError:
            if LOG:
                LOG.error("northstar-cloud: "
                          "File not found at : %s " % input_file)
            else:
                print("northstar-cloud: "
                      "File not found at : %s " % (input_file))
            sys.exit(0)
    return []

'''
Sample output from watson recognization service.
{
  "images": [
    {
      "classifiers": [
        {
          "classifier_id": "DefaultCustomModel_2080973559",
          "name": "Default Custom Model",
          "classes": [
            {
              "class": "wildfire",
              "score": 0.767
            }
          ]
        }
      ],
      "image": "fire_burned.jpg"
    }
  ],
  "images_processed": 1,
  "custom_classes": 2
}
'''

'''
classes = {'images': [{'classifiers': [{'classifier_id': 'DefaultCustomModel_2080973559', 'name': 
'Default Custom Model', 'classes': [{'class': 'wildfire', 'score': 0.767}]}], 'image': 'fire_burned.jpg'}], 'images_processed': 1, 'custom_classes': 2}
'''

def read_config(file_name="config"):
    config_file = '/etc/northstar-service-config/%s' % file_name
    with open(config_file) as json_file:
        config = json.load(json_file)
    return config


def get_classification_for_image(result, image_name):
    """
    Parsing the classification output
    """
    if result:
        if result['images_processed'] == 1:
            if image_name == result['images'][0]['image']:
                for out in result['images'][0]['classifiers']:
                    for item in out['classes']:
                        if item['class'] == 'wildfire':
                            return Fire.FIRE
    return Fire.NO


def get_distance_bet_two_points_using_haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 3956 # Radius of earth in miles. Use 6371 for kilometers
    return c * r

def get_distance_between_two_points_in_miles(lat1, lon1, lat2, lon2):
    from_point = (lat1, lon1)
    to_point = (lat2, lon2)
    return geodesic(from_point, to_point).miles

def calculate_compass_bearing(lat1, lon1, lat2, lon2):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    Sample Output
        : calculate_compass_bearing(37.3229978, -122.0321823, 37.3229978, -121.0321823)
        : 89.69684131116264
    """
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    diffLong = radians(lon2 - lon1)

    x = sin(diffLong) * cos(lat2)
    y = cos(lat1) * sin(lat2) - (sin(lat1)
            * cos(lat2) * cos(diffLong))

    initial_bearing = atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


def get_safe_points(wind_dir=0, user_lat=0.0, user_long=0.0):
    if wind_dir:
        if int(wind_dir) in range(0, 181):
            updated_lat = user_lat + 0.033333
            return updated_lat, user_long

        if int(wind_dir) in range(182, 271):
            updated_lat = user_lat - 0.033333
            return updated_lat, user_long

        if int(wind_dir) in range(271, 361):
            updated_lat = user_lat + 0.033333
            return updated_lat, user_long
    return user_lat, user_long


def get_hospitals_point(wind_dir=0, user_lat=0.0, user_long=0.0):
    # We will hospitals DB ready, in the mean time
    # redirect user to safe location

    if wind_dir:
        if int(wind_dir) in range(0, 181):
            updated_lat = user_lat + 3.033333
            return updated_lat, user_long

        if int(wind_dir) in range(182, 271):
            updated_lat = user_lat - 3.033333
            return updated_lat, user_long

        if int(wind_dir) in range(271, 361):
            updated_lat = user_lat + 3.033333
            return updated_lat, user_long
    return user_lat, user_long


def get_weather_host():
    config = read_config()
    return config.get('weather_host', 'https://api.weather.com')

def get_default_params():
    config = read_config()
    return {
        'apiKey': config.get('weather_api_key', ''),
        'language': 'en-US'
    }

def request_headers():
    return {
        'User-Agent': 'Request-Promise',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip'
    }


def get_dummy_weather_no_fire_data():
    return {
        "time": 1499360400,
        "summary": "Foggy",
    "icon": "fog",
    "precipIntensity": 0,
    "precipProbability": 0,
    "temperature": 87.72,
    "apparentTemperature": 87.72,
    "dewPoint": 50.78,
    "humidity": 0.28,
    "pressure": 1016.99,
    "windSpeed": 4.42,
    "windGust": 6.44,
    "windBearing": 54,
    "cloudCover": 0.19,
    "uvIndex": 5,
    "visibility": 1.24,
    "latitude": "36.07228",
    "longitude": "-120.26561",
    "Date": "07/06/17",
    "hour": 10,
    "dayofyear": 187,
    "monthofyear": 7
  }


def get_dummy_weather_with_fire_data():
    return {
    "time": 1518991200,
    "summary": "Clear",
    "icon": "clear-day",
    "precipIntensity": 0,
    "precipProbability": 0,
    "temperature": 59.2,
    "apparentTemperature": 59.2,
    "dewPoint": -0.78,
    "humidity": 0.09,
    "pressure": 998.1,
    "windSpeed": 10.74,
    "windGust": 32.81,
    "windBearing": 257,
    "cloudCover": 0,
    "uvIndex": 3,
    "visibility": 9.997,
    "latitude": "37.40208",
    "longitude": "-118.50235",
    "Date": "02/18/18",
    "hour": 14,
    "dayofyear": 49,
    "monthofyear": 2
  }