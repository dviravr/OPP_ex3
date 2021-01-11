import heapq as hq
import json
import random
from os import path
from typing import List

import matplotlib.pyplot as plt

from src.DiGraph import DiGraph
from src.GraphAlgoInterface import GraphAlgoInterface
from src.GraphInterface import GraphInterface
from src.Node import Node


class GraphAlgo(GraphAlgoInterface):
    _graph: GraphInterface

    def __init__(self, graph: GraphInterface = None):
        self._graph = graph

    def get_graph(self) -> GraphInterface:
        return self._graph

    def load_from_json(self, file_name: str) -> bool:
        if path.exists(file_name):
            graph: GraphInterface = DiGraph()
            try:
                with open(file_name, 'r') as json_file:
                    data = json.load(json_file)
                    for n in data["Nodes"]:
                        if "pos" in n:
                            p = n["pos"].split(",")
                            pos = float(p[0]), float(p[1]), float(p[2])
                            graph.add_node(n["id"], pos)
                        else:
                            graph.add_node(n["id"])
                    for e in data["Edges"]:
                        graph.add_edge(e["src"], e["dest"], e["w"])
                    self._graph = graph
                return True
            except IOError as e:
                print(e)
        return False

    def save_to_json(self, file_name: str) -> bool:
        if self.get_graph() is not None:
            try:
                with open(file_name, 'w') as file:
                    json.dump(self.get_graph(), file, default=lambda o: o.__dict__(), indent=4)
                    return True
            except IOError as e:
                print(e)
        return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        n1: Node = self.get_graph().get_all_v().get(id1)
        n2: Node = self.get_graph().get_all_v().get(id2)
        if n1 is None or n2 is None:
            return float('inf'), []
        self._reset_values()
        # calculate the shortest path from id1 to id2
        shortest_path = self._reconstruct_path(id1, id2, self._dijkstra(n1, n2))
        # print(self.get_graph().get_all_v().get(id2).get_dist())
        return n2.get_dist(), shortest_path

    def connected_component(self, id1: int) -> list:
        # getting the two paths of the graph and the transpose graph
        component = []
        if self.get_graph() is not None and id1 in self.get_graph().get_all_v():
            bfs_path, transpose_path = self._scc(id1)
            for i in bfs_path:
                if i in transpose_path:
                    # looping over the paths and checking whether the node is in both paths
                    # if he is in both paths he is part of the component.
                    # setting him a component id and appending him to the component list
                    self.get_graph().get_all_v().get(i).set_component(id1)
                    component.append(i)
        return component

    def connected_components(self) -> List[list]:
        components = []
        self._reset_components()
        nodes: dict = self.get_graph().get_all_v()
        for n in nodes:
            if nodes.get(n).get_component() is None:
                # looping on all nodes and checking if he is part of component already
                # if not check is component and append his component list to the components list
                components.append(self.connected_component(n))
        return components

    def plot_graph(self) -> None:
        nodes: dict = self.get_graph().get_all_v()
        min_max_x, min_max_y = self._min_max_pos()
        nodes_pos = self._random_pos(min_max_x, min_max_y)

        set3 = plt.get_cmap('Set3')
        ax = plt.axes()
        r = (min_max_x[1] - min_max_x[0]) / 1000

        for n in nodes:
            x = nodes_pos.get(n)[0]
            y = nodes_pos.get(n)[1]
            plt.scatter(x, y, c='b', s=50)

            edges: dict = self.get_graph().all_out_edges_of_node(n)
            for e in edges:
                # r = 0.03 * edges.get(e)
                dx = nodes_pos.get(e)[0] - x
                dy = nodes_pos.get(e)[1] - y
                # Each arrow is in width and color corresponding to their weight,
                #   The higher the weight they will get a darker color and the size of the arrow will increase
                ax.arrow(x, y, dx, dy, length_includes_head=True, width=r,
                         color=set3(edges.get(e)), head_width=10 * r * edges.get(e),
                         head_length=10 * r * edges.get(e))
        plt.colorbar()
        plt.show()
        return

    def _min_max_pos(self) -> tuple:
        # the method find the range of the position of all nodes in the graph.
        # return tuple that present the range in the x-axis and the y-axis.
        nodes: dict = self.get_graph().get_all_v()
        max_x: float = float('-inf')
        min_x: float = float('inf')
        max_y: float = float('-inf')
        min_y: float = float('inf')
        for n in nodes:
            pos: tuple = nodes.get(n).get_pos()
            if pos is not None:
                max_x = max(max_x, pos[0])
                min_x = min(min_x, pos[0])
                min_y = min(min_y, pos[1])
                max_y = max(max_y, pos[1])
        if min_x == float('inf'):
            min_x = 0
            min_y = 0
            max_x = 1
            max_y = 1
        if min_x == max_x:
            max_x += 1
        if min_y == max_y:
            max_y += 1
        return (min_x, max_x), (min_y, max_y)

    def _random_pos(self, min_max_x: tuple, min_max_y: tuple) -> dict:
        # There may be a situation where JSON did not get locations for all the vertices
        # so to draw them on the graph we will chose random locations for those vertices that came without a location.

        nodes: dict = self.get_graph().get_all_v()
        pos_set: set = set()
        pos_dict: dict = {}
        for n in nodes:
            if nodes.get(n).get_pos() is not None:
                pos_set.add(nodes.get(n).get_x())

        for n in nodes:
            if nodes.get(n).get_pos() is None:
                x = random.uniform(min_max_x[0], min_max_x[1])
                while x in pos_set:
                    x = random.uniform(min_max_x[0], min_max_x[1])
                y = random.uniform(min_max_y[0], min_max_y[1])
                pos_set.add(x)
            else:
                x = (nodes.get(n).get_x())
                y = (nodes.get(n).get_y())
            pos_dict[n] = x, y
        return pos_dict

    def _dijkstra(self, src: Node, dest: Node) -> dict:
        # create empty minimum heap
        # the elements in the heap should be a tuple that hold two elements
        # the first is the distance from the src node to the current node, the second is the node himself
        heap: hq = []
        src.set_dist(0)
        src.set_visited(True)
        hq.heappush(heap, (0, src))
        # create new dictionary of the path, every key holds up his parent node
        # the parent of the src is None
        # di_path = {src: None}
        di_path = {}

        while len(heap) > 0:
            # pooping out the minimum element from the heap
            node: Node = hq.heappop(heap)[1]
            if node.get_key() == dest.get_key():
                break
            if not node.get_visited():
                # if the node wasn't visited yet set the visit to true
                node.set_visited(True)
            edges = self.get_graph().all_out_edges_of_node(node.get_key())
            # looping over all the edges the going out of the node
            for e in edges:
                ni: Node = self.get_graph().get_all_v().get(e)
                if not ni.get_visited():
                    # if the node wasn't visited yet calculate the distance from the src node to this node
                    # and check if the distance is lower then the previous distance
                    # (assuming the distances initialized to infinity (in this case -1 is infinity))
                    dist = node.get_dist() + edges.get(e)
                    if ni.get_dist() == -1 or dist < ni.get_dist():
                        # updating the distance, adding the node t the heap and updating the parent of the node
                        ni.set_dist(dist)
                        hq.heappush(heap, (dist, ni))
                        di_path[ni.get_key()] = node.get_key()
        return di_path

    def _reconstruct_path(self, src: int, dest: int, full_path: dict) -> list:
        if full_path.get(dest) is None:
            return []
        shortest_path = [dest]
        parent = full_path.get(dest)
        # reconstructing the path using the path dictionary into a list starting from the dest key
        while parent != src:
            # wile we didn't get to the src node that his parent is None
            # insert the parent to the list and go to the next parent
            shortest_path.insert(0, parent)
            parent = full_path.get(parent)
        shortest_path.insert(0, src)
        return shortest_path

    def _scc(self, id1: int) -> tuple:
        # making two paths with the dfs algorithm, one of the graph and the second of the transpose graph
        # and returning them as a tuple
        self._reset_values()
        dfs_path = self._bfs(id1, False)
        self._reset_values()
        dfs_transpose_path = self._bfs(id1, True)
        return dfs_path, dfs_transpose_path

    def _bfs(self, id1: int, reverse: bool) -> set:
        # initializing the path to be an empty set
        bfs_path = set()
        # temp list that work like a queue
        queue = []
        nodes: dict = self.get_graph().get_all_v()
        nodes.get(id1).set_visited(True)
        queue.append(id1)
        # adding the node id to the path
        bfs_path.add(id1)

        while queue:
            node: int = queue.pop(0)
            if reverse:
                # if we are looking for the path in transpose graph take all in edges of a node
                # else take all the out edges of a node
                neighbors = self.get_graph().all_in_edges_of_node(node)
            else:
                neighbors = self.get_graph().all_out_edges_of_node(node)
            for ni in neighbors:
                # if we didn't visit the node visit him and his neighbors
                if not nodes.get(ni).get_visited():
                    queue.append(ni)
                    nodes.get(ni).set_visited(True)
                    bfs_path.add(ni)
        return bfs_path

    def _reset_values(self):
        nodes: dict = self.get_graph().get_all_v()
        # reset all node values of visited to false and distance to -1
        for n in nodes:
            nodes.get(n).set_visited(False)
            nodes.get(n).set_dist(float('inf'))

    def _reset_components(self):
        nodes: dict = self.get_graph().get_all_v()
        # reset all node values of component to None
        for n in nodes:
            nodes.get(n).set_component(None)
