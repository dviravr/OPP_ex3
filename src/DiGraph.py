from src.GraphInterface import GraphInterface
from src.Node import Node


class DiGraph(GraphInterface):
    _graphNodes: dict
    _modeCount: int
    _edgeCount: int
    _edges: dict
    _inEdge: dict

    def __init__(self):
        self._graphNodes: dict = {}
        self._modeCount: int = 0
        self._edgeCount: int = 0
        self._edges: dict = {}
        self._inEdge: dict = {}

    def v_size(self) -> int:
        # Returns the number of edges in this graph
        if self._graphNodes is None:
            return 0
        return len(self._graphNodes)

    def e_size(self) -> int:
        # Returns the number of edges in this graph
        return self._edgeCount

    def get_all_v(self) -> dict:
        # return a dictionary of all the nodes in the Graph
        return self._graphNodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        # check if id1 in the graph, if true return a dictionary of all the nodes connected into id1
        if self._graphNodes.get(id1) is None:
            return {}
        return self._inEdge.get(id1)

    def all_out_edges_of_node(self, id1: int) -> dict:
        # # check if id1 in the graph, if true return a dictionary of all the nodes connected from id1
        if self._graphNodes.get(id1) is None:
            return {}
        return self._edges.get(id1)

    def get_mc(self) -> int:
        # Returns the current version of this graph, if the graph change the MC should be MC++
        return self._modeCount

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        # cannot have negative weight
        if weight < 0.0:
            return False
        # id1 or id2 don't exist
        elif id1 not in self._graphNodes or id2 not in self._graphNodes or id1 == id2:
            return False
        elif id2 in self._edges[id1]:
            # the edge already exist
            return False
        else:
            self._edgeCount += 1
            self._modeCount += 1
            self._edges[id1].update({id2: weight})
            self._inEdge[id2].update({id1: weight})
            return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        # IF THE NODE ALREADY EXIST SHOULD DO NOTHING.
        if node_id in self._graphNodes:
            return False
        self._modeCount += 1
        self._graphNodes[node_id] = Node(node_id, pos)
        self._edges[node_id] = {}
        self._inEdge[node_id] = {}
        return True

    def remove_node(self, node_id: int) -> bool:
        # the method removes a node from the graph
        if node_id not in self._graphNodes:
            return False
        self._modeCount += 1
        for x in self._edges[node_id]:
            del (self._inEdge[x][node_id])
            self._edgeCount -= 1
        for x in self._inEdge[node_id]:
            del (self._edges[x][node_id])
            self._edgeCount -= 1
        del (self._graphNodes[node_id])
        del (self._edges[node_id])
        del (self._inEdge[node_id])
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        # removes an edge from the graph.
        # the 2 next if check if the edge exist.
        if node_id1 not in self._graphNodes or node_id2 not in self._graphNodes:
            return False
        if node_id2 not in self.all_out_edges_of_node(node_id1):
            return False
        self._modeCount += 1
        self._edgeCount -= 1
        del (self._edges[node_id1][node_id2])
        del (self._inEdge[node_id2][node_id1])
        return True

    def __dict__(self):
        # TO STRING - used for save to json
        graph_nodes = self.get_all_v()
        json_nodes = []
        json_edges = []
        for n in graph_nodes:
            if graph_nodes.get(n).get_pos() is not None:
                json_node = {"id": n, "pos": graph_nodes.get(n).get_pos_str()}
            else:
                json_node = {"id": n}
            json_nodes.append(json_node)
            graph_edges: dict = self.all_out_edges_of_node(n)
            for e in graph_edges:
                json_edges.append({"src": n, "dest": e, "w": graph_edges.get(e)})
        return {"Nodes": json_nodes, "Edges": json_edges}

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.get_all_v() != other.get_all_v():
            return False
        for n in self.get_all_v():
            if self.all_out_edges_of_node(n) != other.all_out_edges_of_node(n):
                return False
        return True
