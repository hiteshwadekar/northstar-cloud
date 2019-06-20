import json
import sys
from enum import Enum


class PossibleEvents(Enum):
    WITNESS_DECISION_MERGE_ALL_POSSIBLE = 1
    WITNESS_DECISION_PARTIAL_MERGE_POSSIBLE = 2
    WITNESS_DECISION_NO_MERGE_POSSIBLE = 3
    WITNESS_DECISION_CANT_DECIDE = 4


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


def count_no_items_witness_list(original_list=[]):
    count = 0
    for each_list in original_list:
        for _ in each_list:
            count += 1
    return count


def verify_witness_data_list_string_format(witness_event_list, LOG=None):

    if not witness_event_list or len(witness_event_list) == 0:
        LOG.error(
            "detective-api: Provided witness list is empty : %s "
            % witness_event_list)
        sys.exit(0)

    if type(witness_event_list) is not list:
        LOG.error("detective-api: Provided witness "
                  "list is WRONG format, "
                  "it should be 'LIST' : %s " % witness_event_list)
        sys.exit(0)

    for item in witness_event_list:
        if type(item) is not list:
            LOG.error("detective-api: Provided witness "
                      "sub-list is WRONG format, "
                      "it should be 'LIST' : %s " % witness_event_list)
            sys.exit(0)

        for each_event in item:
            if not isinstance(each_event, str):
                LOG.error("detective-api: Provided witness events "
                          "should be 'STRING' : %s " % witness_event_list)
                sys.exit(0)
