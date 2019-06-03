from detective_api.common import logs as logging
from detective_api.common import utils as c_utils
from detective_api.db.detective_graph import DetectiveGraph as dt_graph


LOG = logging.getLogger(__name__)


class DetectiveApiService:
    def __init__(self):
        # Graph structure for witness events
        self.detective_graph = dt_graph()
        # expecting list of witness events
        self.witness_events = []
        self.no_witness_events_with_dup = 0

    @property
    def graph(self):
        return self.detective_graph

    def _predict_order_of_all_witness_events(self):

        wintness_topolical_sorts = []
        possible_event_pred = \
            c_utils.PossibleEvents.WITNESS_DECISION_CANT_DECIDE
        is_cycle_present = False

        try:
            is_cycle_present = self.detective_graph.check_cycle_present()
            if is_cycle_present:
                LOG.info("_predict_order_of_all_witness_events: Cycle Found: ")
                return \
                    c_utils.PossibleEvents.WITNESS_DECISION_NO_MERGE_POSSIBLE,\
                    self.witness_events
        except Exception as e:
            LOG.error(
                "_predict_order_of_all_witness_events: "
                "while detecting cycle got: %s"
                % (e)
            )
            return possible_event_pred, self.witness_events

        try:
            wintness_topolical_sorts = \
                self.detective_graph.topological_graph_sort()
        except Exception as e:
            LOG.error(
                "_predict_order_of_all_witness_events: "
                "while topological sort got: %s"
                % (e)
            )
            return possible_event_pred, self.witness_events

        LOG.debug(
            "_predict_order_of_all_witness_events: "
            "topological sort: %s  for "
            "witness events %s"
            % (wintness_topolical_sorts, self.witness_events)
        )
        if wintness_topolical_sorts:
            wintness_first_event_vertex = wintness_topolical_sorts[0]
            wintness_last_event_vertex = \
                wintness_topolical_sorts[len(wintness_topolical_sorts) - 1]

            witness_paths = []
            try:
                witness_paths = \
                    self.detective_graph.get_multiple_paths(
                        wintness_first_event_vertex, wintness_last_event_vertex
                    )
            except Exception as e:
                LOG.error(
                    "_predict_order_of_all_witness_events: "
                    "While getting multiple path: %s"
                    % (e)
                )
                return possible_event_pred, self.witness_events

            return self._get_prediction_on_merge_wintess_events(
                wtness_topological_sort_list=wintness_topolical_sorts,
                wtness_all_paths=witness_paths,
                wt_first_event=wintness_first_event_vertex,
                wt_last_event=wintness_last_event_vertex
            )

        return possible_event_pred, self.witness_events

    def _get_prediction_on_merge_wintess_events(
            self, wtness_topological_sort_list=[],
            wtness_all_paths=[],
            wt_first_event="",
            wt_last_event=""
    ):
        wt_ness_tp_sort_length = len(wtness_topological_sort_list)
        wt_ness_all_path_length = len(wtness_all_paths)

        # getting max length vertex list after
        # getting multiple path longest timeline
        # can help us to predict event order.
        wt_max_len, wt_max_event_list = \
            c_utils.get_max_length_list(wtness_all_paths)
        if wt_ness_all_path_length >= 1:
            if wt_max_len == wt_ness_tp_sort_length and \
                    wt_max_event_list[0] == wt_first_event and \
                    wt_max_event_list[wt_max_len - 1] == wt_last_event:
                return \
                    c_utils.PossibleEvents.\
                    WITNESS_DECISION_MERGE_ALL_POSSIBLE,\
                    [wt_max_event_list]

            if wt_max_len < wt_ness_tp_sort_length and \
                    wt_max_event_list[0] == wt_first_event and \
                    wt_max_event_list[wt_max_len - 1] == wt_last_event \
                    and (self.no_witness_events_with_dup ==
                         (wt_ness_tp_sort_length + 2)):
                return \
                    c_utils.PossibleEvents.\
                    WITNESS_DECISION_PARTIAL_MERGE_POSSIBLE,\
                    wtness_all_paths

        if (wt_ness_all_path_length == 0) or \
                (wt_ness_all_path_length == 1 and
                 wt_max_len < wt_ness_tp_sort_length):
            return \
                c_utils.PossibleEvents.\
                WITNESS_DECISION_NO_MERGE_POSSIBLE,\
                self.witness_events

        return \
            c_utils.PossibleEvents.\
            WITNESS_DECISION_CANT_DECIDE,\
            self.witness_events

    def calculate_witness_merge(self):
        LOG.info(
            "calculate_witness_merge: Calculating witness "
            "event merge for: %s"
            % (self.witness_events)
        )
        return self._predict_order_of_all_witness_events()

    def add_single_witness_event(self, witness_event):
        if witness_event not in self.witness_events:
            self.witness_events.append(witness_event)

    def _build_detetive_witness_graph(self):
        if self.witness_events:
            # Initialize Graph with witness
            # event vertices.
            LOG.debug(
                "_build_detetive_witness_graph: "
                "Building graph for witness events %s"
                % (self.witness_events)
            )
            self.detective_graph.addWinessEentVertices(
                c_utils.convert_unique_agg_list_from_multiple_list(
                    self.witness_events
                )
            )
            # Add links between different event vertices with order.
            for i_list in self.witness_events:
                for et_no in range(len(i_list)):
                    if et_no + 1 < len(i_list):
                        self.detective_graph.addWitnessEventLink(
                            i_list[et_no], i_list[et_no + 1]
                        )

    def init_aggregate_witness_events(self, witness_events):
        """Initialize witness events and build witness's event graph.
        :param witness_events: List of witness events.
        """
        LOG.info(
            "init_aggregate_witness_events: "
            "Initializing input witness events %s"
            % (witness_events)
        )
        self.witness_events = witness_events
        self.no_witness_events_with_dup = \
            c_utils.count_no_items_witness_list(self.witness_events)
        self._build_detetive_witness_graph()


if __name__ == "__main__":
    print("Welcome to smart detective solution")
