import os
from detective_api.tests import base
from detective_api.services import detective_api_service \
    as dt_api_service
from detective_api.common import utils as c_utils

DEFAULT_LOGGING_FILE_NAME = "logging.ini"
ROOT_DIR = os.path.abspath(os.curdir)


class TestWitnessApiService(base.BaseTest):
    def setUp(self):
        super(TestWitnessApiService, self).setUp()
        self.service = dt_api_service.DetectiveApiService()
        self.example_test_dir = ROOT_DIR + "/examples"

        self.example_full_merge_file_path1 = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            self.example_test_dir + "/example1.json"
        )
        self.example_partial_merge_file_path1 = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            self.example_test_dir + "/example2.json"
        )
        self.example_no_merge_file_path1 = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            self.example_test_dir + "/example3.json"
        )
        self.example_full_merge_file_path2 = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            self.example_test_dir + "/example4.json"
        )
        self.example_partial_merge_file_path2 = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            self.example_test_dir + "/example5.json"
        )
        self.example_no_merge_file_path2 = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            self.example_test_dir + "/example6.json"
        )

    def test_full_merge_1_witness_events(self):
        full_merge_witness_data = c_utils.read_json_file(
            self.example_full_merge_file_path1
        )
        self.service.init_aggregate_witness_events(full_merge_witness_data)
        is_merge_possible, merge_list = self.service.calculate_witness_merge()
        self.assertEqual(
            is_merge_possible.name,
            c_utils.PossibleEvents.WITNESS_DECISION_MERGE_ALL_POSSIBLE.name
        )
        self.assertEqual(
            merge_list,
            [["fight", "gunshot", "falling", "fleeing"]]
        )

    def test_full_merge_2_witness_events(self):
        full_merge_witness_data = c_utils.read_json_file(
            self.example_full_merge_file_path2
        )
        self.service.init_aggregate_witness_events(full_merge_witness_data)
        is_merge_possible, merge_list = self.service.calculate_witness_merge()
        self.assertEqual(
            is_merge_possible.name,
            c_utils.PossibleEvents.WITNESS_DECISION_MERGE_ALL_POSSIBLE.name
        )
        self.assertEqual(merge_list, [["0", "1", "2", "3"]])

    def test_partial_merge_1_witness_events(self):
        partial_merge_witness_data = c_utils.read_json_file(
            self.example_partial_merge_file_path1
        )
        self.service.init_aggregate_witness_events(partial_merge_witness_data)
        is_merge_possible, merge_list = self.service.calculate_witness_merge()
        self.assertEqual(
            is_merge_possible.name,
            c_utils.PossibleEvents.WITNESS_DECISION_PARTIAL_MERGE_POSSIBLE.name
        )
        self.assertEqual(
            merge_list,
            [['shadowy figure', 'demands', 'scream', 'siren'],
             ['shadowy figure', 'pointed gun', 'scream', 'siren']]
        )

    def test_partial_merge_2_witness_events(self):
        partial_merge_witness_data = c_utils.read_json_file(
            self.example_partial_merge_file_path2
        )
        self.service.init_aggregate_witness_events(partial_merge_witness_data)
        is_merge_possible, merge_list = self.service.calculate_witness_merge()
        self.assertEqual(
            is_merge_possible.name,
            c_utils.PossibleEvents.WITNESS_DECISION_PARTIAL_MERGE_POSSIBLE.name
        )
        self.assertEqual(merge_list, [
            ['buying gas', 'pouring gas',
             'laughing', 'lighting match', 'fire', 'smoke'],
            ['buying gas', 'pouring gas',
             'crying', 'fire', 'smoke']
        ])

    def test_no_merge_1_witness_events(self):
        no_merge_witness_data = c_utils.read_json_file(
            self.example_no_merge_file_path1
        )
        self.service.init_aggregate_witness_events(no_merge_witness_data)
        is_merge_possible, merge_list = self.service.calculate_witness_merge()
        self.assertEqual(
            is_merge_possible.name,
            c_utils.PossibleEvents.WITNESS_DECISION_NO_MERGE_POSSIBLE.name
        )
        self.assertEqual(merge_list, [
            ['argument', 'stuff', 'pointing'],
            ['press brief', 'scandal', 'pointing'],
            ['bribe', 'coverup']
        ])

    def test_no_merge_2_witness_events(self):
        no_merge_witness_data = c_utils.read_json_file(
            self.example_no_merge_file_path2
        )
        self.service.init_aggregate_witness_events(no_merge_witness_data)
        is_merge_possible, merge_list = self.service.calculate_witness_merge()
        self.assertEqual(
            is_merge_possible.name,
            c_utils.PossibleEvents.WITNESS_DECISION_NO_MERGE_POSSIBLE.name
        )
        self.assertEqual(
            merge_list,
            [['start1', 'end1', 'deadend'], ['end1', 'start1', 'deadend']]
        )
