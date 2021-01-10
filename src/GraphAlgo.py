import json
import heapq as hq
import math
import random

from src.Node import Node
from typing import List
from src.DiGraph import DiGraph
import matplotlib.pyplot as plt
from src.GraphInterface import GraphInterface
from src.GraphAlgoInterface import GraphAlgoInterface
from pathlib import Path


class GraphAlgo(GraphAlgoInterface):
    _graph: GraphInterface

    def __init__(self, graph: GraphInterface = None):
        self._graph = graph

    def get_graph(self) -> GraphInterface:
        return self._graph

    def load_from_json(self, file_name: str) -> bool:
        graph: GraphInterface = DiGraph()
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

    # todo:
    def save_to_json(self, file_name: str) -> bool:
        with open(file_name, 'w') as json_file:
            print()
        return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        n1: Node = self.get_graph().get_all_v().get(id1)
        n2: Node = self.get_graph().get_all_v().get(id2)
        if n1 is None or n2 is None:
            return float('inf'), []
        self._reset_values()
        # calculate the shortest path from id1 to id2
        shortest_path = self._reconstruct_path(id2, self._dijkstra(n1))
        # print(self.get_graph().get_all_v().get(id2).get_dist())
        return n2.get_dist(), shortest_path

    def connected_component(self, id1: int) -> list:
        # getting the two paths of the graph and the transpose graph
        path, transpose_path = self._scc(id1)
        component = []
        for i in path:
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

    # todo:
    def plot_graph(self) -> None:
        HSV = plt.get_cmap('Set3')
        minMax: tuple = self.min_max_pos()
        print((minMax[0][1] - minMax[0][0]) / 25)
        print(self.maxDist())
        self.random_pos(minMax)

        set3 = plt.get_cmap('Set3')
        nodes: dict = self.get_graph().get_all_v()
        ax = plt.axes()
        r = round((minMax[0][1] - minMax[0][0]) / 20)

        for n in nodes:
            x = (nodes.get(n).get_x())
            y = (nodes.get(n).get_y())
            plt.scatter(x, y, c='b', s=50)

            edges: dict = self.get_graph().all_out_edges_of_node(n)
            for e in edges:
                # r = 0.03 * edges.get(e)
                dx = nodes.get(e).get_x() - x
                dy = nodes.get(e).get_y() - y
                ax.arrow(x, y,
                         dx, dy, length_includes_head=True, width=10 * r * edges.get(e), color=set3(edges.get(e)),
                         head_width=10 * r * edges.get(e), head_length=10 * r * edges.get(e))
        # plt.colorbar(ticks=[0.0,0.5,1.0,1.5,2.0,2.5,3.0], )
        # plt.clim(0.0,100.0)
        plt.show()
        return

    def min_max_pos(self) -> tuple:
        nodes: dict = self.get_graph().get_all_v()
        maxX: float = float('-inf')
        minX: float = float('inf')
        maxY: float = float('-inf')
        minY: float = float('inf')
        maxD: float
        for n in nodes:
            pos: tuple = nodes.get(n).get_pos()
            if pos is not None:
                maxX = max(maxX, pos[0])
                minX = min(minX, pos[0])
                minY = min(minY, pos[1])
                maxY = max(maxY, pos[1])
        return (minX, maxX), (minY, maxY)

    def random_pos(self, minMax: tuple) -> None:
        nodes: dict = self.get_graph().get_all_v()
        posSet: set = {}
        for n in nodes:
            if nodes.get(n).get_pos() is not None:
                posSet.add(n.get_x())

        for n in nodes:
            if nodes.get(n).get_pos() is None:
                x = random.uniform(minMax[0][0], minMax[0][1])
                while x in posSet:
                    x = random.uniform(minMax[0][0], minMax[0][1])
                y = random.uniform(minMax[1][0], minMax[1][1])
                # while y in g.posDict.values():
                #    y = random.uniform(g.minY, g.maxY)
                nodes.get(n).set_pos((x, y))
                posSet.add(x)
            else:
                x = (nodes.get(n).get_x())
                y = (nodes.get(n).get_y())

    def maxDist(self) -> float:
        nodes: dict = self.get_graph().get_all_v()
        maxD: float = 0.0
        p1: tuple = ()
        p2: tuple = ()
        for n in nodes:
            p1 = nodes.get(n).get_pos()
            for i in self.get_graph().all_out_edges_of_node(n):
                p2 = nodes.get(i).get_pos()
                maxD = max(maxD, math.dist(p1, p2))
        return maxD

    def min_max_pos(self) -> tuple:
        nodes: dict = self.get_graph().get_all_v()
        maxX: float = float('-inf')
        minX: float = float('inf')
        maxY: float = float('-inf')
        minY: float = float('inf')
        maxD: float
        for n in nodes:
            pos: tuple = nodes.get(n).get_pos()
            if pos is not None:
                maxX = max(maxX, pos[0])
                minX = min(minX, pos[0])
                minY = min(minY, pos[1])
                maxY = max(maxY, pos[1])
        return (minX, maxX), (minY, maxY)

    def random_pos(self, minMax: tuple) -> None:
        nodes: dict = self.get_graph().get_all_v()
        posSet: set = {}
        for n in nodes:
            if nodes.get(n).get_pos() is not None:
                posSet.add(n.get_x())

        for n in nodes:
            if nodes.get(n).get_pos() is None:
                x = random.uniform(minMax[0][0], minMax[0][1])
                while x in posSet:
                    x = random.uniform(minMax[0][0], minMax[0][1])
                y = random.uniform(minMax[1][0], minMax[1][1])
                # while y in g.posDict.values():
                #    y = random.uniform(g.minY, g.maxY)
                nodes.get(n).set_pos((x, y))
                posSet.add(x)
            else:
                x = (nodes.get(n).get_x())
                y = (nodes.get(n).get_y())

    def maxDist(self) -> float:
        nodes: dict = self.get_graph().get_all_v()
        maxD: float = 0.0
        p1: tuple = ()
        p2: tuple = ()
        for n in nodes:
            p1 = nodes.get(n).get_pos()
            for i in self.get_graph().all_out_edges_of_node(n):
                p2 = nodes.get(i).get_pos()
                maxD = max(maxD, math.dist(p1, p2))
        return maxD

    def _dijkstra(self, src: Node) -> dict:
        # create empty minimum heap
        # the elements in the heap should be a tuple that hold two elements
        # the first is the distance from the src node to the current node, the second is the node himself
        heap: hq = []
        src.set_dist(0)
        src.set_visited(True)
        hq.heappush(heap, (0, src))
        # create new dictionary of the path, every key holds up his parent node
        # the parent of the src is None
        path = {src: None}

        while len(heap) > 0:
            # pooping out the minimum element from the heap
            node = hq.heappop(heap)[1]
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
                        path[ni.get_key()] = node.get_key()
        return path

    def _reconstruct_path(self, dest: int, path: dict) -> list:
        if path.get(dest) is None:
            return []
        shortest_path = [dest]
        parent = path.get(dest)
        # reconstructing the path using the path dictionary into a list starting from the dest key
        while parent is not None:
            # wile we didn't get to the src node that his parent is None
            # insert the parent to the list and go to the next parent
            shortest_path.insert(0, parent)
            parent = path.get(parent)
        return shortest_path

    def _scc(self, id1: int) -> tuple:
        # making two paths with the dfs algorithm, one of the graph and the second of the transpose graph
        # and returning them as a tuple
        self._reset_values()
        dfs_path = self._dfs(id1, False)
        self._reset_values()
        dfs_transpose_path = self._dfs(id1, True)
        return dfs_path, dfs_transpose_path

    def _dfs(self, id1: int, reverse: bool, path: set = None) -> set:
        # initializing the path to be an empty set if we didn't go him from the function call
        if path is None:
            path = set()
        nodes: dict = self.get_graph().get_all_v()
        nodes.get(id1).set_visited(True)
        # adding the node id to the path
        path.add(id1)

        if reverse:
            # if we are looking for the path in transpose graph take all in edges of a node
            # else take all the out edges of a node
            neighbors = self.get_graph().all_in_edges_of_node(id1)
        else:
            neighbors = self.get_graph().all_out_edges_of_node(id1)
        if neighbors is not None:
            for ni in neighbors:
                # if we didn't visit the node visit him and his neighbors by recursive call to this method
                if not nodes.get(ni).get_visited():
                    self._dfs(ni, reverse, path)
        return path

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
