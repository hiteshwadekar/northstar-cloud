import json
import sys
from enum import Enum
from math import radians, cos, sin, asin, sqrt

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