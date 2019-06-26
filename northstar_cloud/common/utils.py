import json
import sys
from enum import Enum

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


def get_max_length_list(wt_paths):
    max_len = 0
    max_len_list = []
    for item in wt_paths:
        if max_len < len(item):
            max_len = len(item)
            max_len_list = item
    return max_len, max_len_list


def convert_unique_agg_list_from_multiple_list(input_list):
    if input_list:
        unique_set = set()
        for each_list in input_list:
            unique_set.update(each_list)
        return list(unique_set)
    return []


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


def calculate_diff_between_long_latitudes():
    pass




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

def get_classification_for_image(result, image_name):
    if result:
        if result['images_processed'] == 1:
            if image_name == result['images'][0]['image']:
                for out in result['images'][0]['classifiers']:
                    for item in out['classes']:
                        if item['class'] == 'wildfire':
                            return Fire.FIRE
    return Fire.NO
