from collections import defaultdict
from detective_api.common import logs as logging
from detective_api.common import exceptions as dt_exception

LOG = logging.getLogger(__name__)


class Graph:
    def __init__(self):
        # Unique vertex list for wintness events.
        self.vertices = []
        # Graph structure for witness events.
        self.graph = defaultdict(list)

    @property
    def vertices(self):
        return self.vertices

    @property
    def graph(self):
        return self.graph

    def init_vertices(self, unique_vertices_list):
        LOG.debug(
            "init_vertices: initializing unique vertices"
            % (unique_vertices_list)
        )
        self.vertices = unique_vertices_list

    def add_vertex(self, vertex):
        if vertex not in self.vertices:
            self.vertices.append(vertex)
            self.graph[vertex] = []

    def add_edge(self, from_vertex, to_vertex=None):
        if from_vertex:
            LOG.debug(
                "add_edge: adding edge in"
                "graph from Vertex:%s to Vertex:%s "
                % (from_vertex, to_vertex)
            )
            self.graph[from_vertex].append(to_vertex)

    def _get_single_path_for_vertices(
            self, from_vt, to_vt, path=[]):
        path = path + [from_vt]
        if from_vt == to_vt:
            return path
        if from_vt not in self.graph:
            return None
        for ng_vertex in self.graph[from_vt]:
            if ng_vertex not in path:
                newpath = self._get_single_path_for_vertices(
                    ng_vertex,
                    to_vt, path
                )
                if newpath:
                    return newpath
        return None

    def _get_all_paths_for_vertices(
            self, from_vertex, to_vertex, single_path=[]):
        single_path = single_path + [from_vertex]

        if from_vertex == to_vertex:
            return [single_path]

        if from_vertex not in self.graph:
            return []

        multiple_paths = []
        for ng_vertex in self.graph[from_vertex]:
            if ng_vertex not in single_path:
                # Recursively find path destination
                # vertex by exploring all its connected vertex.
                LOG.debug(
                    "_get_all_paths_for_vertices: "
                    "finding path from Vertex:%s to Vertex:%s "
                    % (ng_vertex, to_vertex)
                )
                paths = self._get_all_paths_for_vertices(
                    ng_vertex,
                    to_vertex,
                    single_path
                )
                for path in paths:
                    multiple_paths.append(path)
        return multiple_paths

    def _get_shortest_path_for_vertices(
            self, fromeventvertex, toeventvertex, single_path=[]):
        single_path = single_path + [fromeventvertex]

        if fromeventvertex == toeventvertex:
            return single_path
        if fromeventvertex not in self.graph:
            return None

        shortest = None
        for linkEventVertex in self.graph[fromeventvertex]:
            if linkEventVertex not in single_path:
                new_single_path = self._get_shortest_path_for_vertices(
                    linkEventVertex,
                    toeventvertex,
                    single_path
                )
                if new_single_path:
                    if not shortest or len(new_single_path) < len(shortest):
                        shortest = new_single_path
        return shortest

    def get_multiple_paths(self, from_vertex, to_vertex):
        # Get multiple paths for source and destination vertex in the graph.
        # Using DFS way to find path.
        LOG.debug(
            "get_multiple_paths: "
            "getting paths from Vertex:%s to Vertex:%s "
            % (from_vertex, to_vertex)
        )
        if from_vertex and to_vertex:
            return self._get_all_paths_for_vertices(
                from_vertex, to_vertex
            )
        return None

    def _sort_topological_graph(
            self, vt_from, vertices_visted, vt_sroted_stack):
        vertices_visted[vt_from] = True
        for neighbor_vertex in self.graph[vt_from]:
            try:
                if not vertices_visted[neighbor_vertex]:
                    # Recursively sort each conneceted vertices.
                    LOG.debug(
                        "_topologicalWitnessEvents: finding "
                        "topological order path from Vertex:%s "
                        % (neighbor_vertex)
                    )
                    self._topologicalWitnessEvents(
                        neighbor_vertex,
                        vertices_visted,
                        vt_sroted_stack
                    )
            except KeyError:
                raise dt_exception.TopologicalSortKeyError(
                    vertex_key=vt_from
                )
                vt_sroted_stack.insert(0, vt_from)

    def topological_graph_sort(self):
        # Topological sorting (DFS) for all witness events
        LOG.debug(
            "topological_graph_sort: topological sorting "
            "for vertices %s "
            % self.vertices
        )
        vertices_visited = {
            each_vt: False for each_vt in self.vertices
        }
        vt_sroted_stack = []

        for vt in self.vertices:
            # Find all topological orders for each vertex.
            if not vertices_visited[vt]:
                self._sort_topological_graph(
                    vt,
                    vertices_visited,
                    vt_sroted_stack
                )
        return vt_sroted_stack

    def _check_if_cycle_present(
            self, vertex,
            vertices_visited, vertices_stack
    ):

        vertices_visited[vertex] = True
        vertices_stack[vertex] = True

        # Recur for all neighbours
        # if any neighbour is visited and in
        for vt in self.graph[vertex]:
            if not vertices_visited[vt]:
                if self._check_if_cycle_present(
                        vt,
                        vertices_visited,
                        vertices_stack):
                    return True
            elif vertices_stack[vt]:
                return True

        # Backtracking here..
        vertices_stack[vertex] = False
        return False

    def check_cycle_present(self):
        vertices_visited = {
            each_vt: False for each_vt in self.vertices
        }
        vertices_stack = {
            each_vt: False for each_vt in self.vertices
        }

        for vt in self.vertices:
            if not vertices_visited[vt]:
                if self._check_if_cycle_present(
                        vt,
                        vertices_visited,
                        vertices_stack):
                    return True
        return False
