import argparse
import os

from detective_api.common import logs as logging
from detective_api.\
    services.detective_api_service import DetectiveApiService \
    as dt_service
from detective_api.common import utils as dt_utils

LOG = logging.getLogger(__name__)


def main():
    program_args = get_program_args()
    input_file = os.path.abspath(program_args.witnesses_input_file)

    if input_file:
        witness_list = parse_witness_list(input_file)

        dt_service_api = dt_service()
        dt_service_api.init_aggregate_witness_events(witness_list)

        possible_event_pred, wintess_possible_list = \
            dt_service_api.calculate_witness_merge()

        print("\n")
        print("detective-api: OUTPUT")
        print("detective-api: Witness events given input     "
              ": %s " % witness_list)
        print("detective-api: Witness events prediction      "
              ": %s " % possible_event_pred.name)
        print("detective-api: Witness events predicted list  "
              ": %s " % wintess_possible_list)
        print("\n")


def parse_witness_list(witness_input_file):
    witness_event_list = dt_utils.read_json_file(
        witness_input_file, LOG)
    dt_utils.verify_witness_data_list_string_format(
        witness_event_list, LOG
    )
    return witness_event_list


def get_program_args():
    """
    Construct and parse the command line arguments to the program.
    """
    parser = argparse.ArgumentParser(
        description='Smart witness analysis tools.'
    )
    parser.add_argument(
        'witnesses_input_file',
        help='Path to list of witnesses events json format file.'
    )
    return parser.parse_args()


if __name__ == '__main__':
    main()
