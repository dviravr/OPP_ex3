import heapq as hq
from typing import List
from Node import Node
from src import GraphInterface
from src import GraphAlgoInterface
from DiGraph import DiGraph


class GraphAlgo(GraphAlgoInterface):
    _graph: GraphInterface
    _path: dict

    def __init__(self, graph: GraphInterface):
        self._graph = graph

    def get_graph(self) -> GraphInterface:
        return self._graph

    def load_from_json(self, file_name: str) -> bool:
        return False

    def save_to_json(self, file_name: str) -> bool:
        return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        n1: Node = self.get_graph().get_node(id1)
        n2: Node = self.get_graph().get_node(id2)
        self._dijkstra(n1)
        shortest_path = self._reconstruct_path(id2)
        return n2.get_dist(), shortest_path

    def connected_component(self, id1: int) -> list:
        n1: Node = self.get_graph().get_node(id1)
        return

    def connected_components(self) -> List[list]:
        return

    def plot_graph(self) -> None:
        return

    def _dijkstra(self, src: Node, reverse: bool) -> int:
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
            if reverse:
                edges = self.get_graph().all_in_edges_of_node(self._graph, node.get_key())
            else:
                edges = self.get_graph().all_out_edges_of_node(self._graph, node.get_key())
            for e in edges:
                # todo: get node
                ni: Node = self.get_graph().get_node(e)
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

    # def _scc(self, id1: int):

