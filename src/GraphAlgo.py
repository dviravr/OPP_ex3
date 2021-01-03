import heapq as hq
from typing import List
from Node import Node
from src import GraphInterface
from GraphAlgoInterface import GraphAlgoInterface


# from DiGraph import DiGraph


class GraphAlgo(GraphAlgoInterface):
    _graph: GraphInterface
    _path: dict

    _nodes: dict
    # todo: change all self._nodes to self.graph().get_all_v()
    _nis: dict
    # todo: change all self._nodes to self.graph().all_out_edges_of_node()
    _re_nis: dict
    # todo: change all self._nodes to self.graph().all_in_edges_of_node()

    # def __init__(self, graph: GraphInterface):
    #     self._graph = graph

    def __init__(self, nodes: dict, nis: dict, re_nis: dict):  # todo: delete
        self._nodes = nodes
        self._nis = nis
        self._re_nis = re_nis

    def get_graph(self) -> GraphInterface:
        return self._graph

    # todo:
    def load_from_json(self, file_name: str) -> bool:
        return False

    # todo:
    def save_to_json(self, file_name: str) -> bool:
        return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        n1: Node = self.get_graph().get_all_v().get(id1)
        n2: Node = self.get_graph().get_all_v().get(id1)
        self._dijkstra(n1)
        shortest_path = self._reconstruct_path(id2)
        return n2.get_dist(), shortest_path

    def connected_component(self, id1: int) -> list:
        path, re_path = self._scc(id1)
        component = []
        for i in path:
            if i in re_path:
                # self.get_graph().get_all_v().get(i).set_component(id1)
                self._nodes.get(i).set_component(id1)
                component.append(i)
        return component

    def connected_components(self) -> List[list]:
        components = []
        self._reset_components()
        for n in self._nodes:
            if self._nodes.get(n).get_component() is not None:
                components.append(self.connected_component(n))
        return components

    # todo:
    def plot_graph(self) -> None:
        return

    def _dijkstra(self, src: Node) -> int:
        heap: hq = []
        self._path = {}
        src.set_dist(0)
        src.set_visited(True)
        hq.heappush(heap, (0, src))
        visit_count: int = 1
        self._path[0] = None

        while len(heap) > 0:
            node = hq.heappop(heap)[1]
            if node.get_visited():
                node.set_visited(True)
                visit_count += visit_count
            # todo: break if got to dest
            edges = self.get_graph().all_out_edges_of_node(self._graph, node.get_key())
            for e in edges:
                # todo: get node
                ni: Node = self.get_graph().get_all_v().get(e)
                if not ni.get_visited:
                    dist = node.get_dist() + edges.get(e)
                    if ni.get_dist() == -1 or dist < ni.get_dist():
                        ni.set_dist(dist)
                        hq.heappush(heap, (dist, ni))
                        self._path[ni.get_key()] = node.get_key()
        return visit_count

    def _reconstruct_path(self, dest: int) -> list:
        shortest_path = []
        i = self._path.get(dest)
        while i is not None:
            shortest_path.insert(0, i)
            i = self._path.get(i)
        return shortest_path

    def _scc(self, id1: int) -> tuple:
        self._reset_values()
        dfs_path = self._dfs(id1, False)
        self._reset_values()
        dfs_re_path = self._dfs(id1, True)
        return dfs_path, dfs_re_path

    def _dfs(self, id1: int, reverse: bool, s=None) -> set:
        if s is None:
            s = set()
        # nodes: dict = self.get_graph().get_all_v()
        # nodes.get(id1).set_visited(True)
        self._nodes.get(id1).set_visited(True)  # todo: delete
        s.add(id1)

        if reverse:
            # nis = self.get_graph().all_in_edges_of_node(id1)
            nis = self._re_nis.get(id1)  # todo: delete
        else:
            # nis = self.get_graph().all_out_edges_of_node(id1)
            nis = self._nis.get(id1)  # todo: delete
        if nis is not None:
            for ni in nis:
                if not self._nodes.get(ni).get_visited():  # todo: delete
                    # if not nodes.get(ni).get_visited():
                    self._dfs(ni, reverse, s)
        return s

    def _reset_values(self):
        # nodes: dict = self.get_graph().get_all_v()
        for n in self._nodes:  # todo: change
            self._nodes.get(n).set_visited(False)  # todo: change

    def _reset_components(self):
        # nodes: dict = self.get_graph().get_all_v()
        for n in self._nodes:  # todo: change
            self._nodes.get(n).set_component(None)  # todo: change
