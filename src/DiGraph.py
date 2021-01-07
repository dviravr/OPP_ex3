from src import GraphInterface
from Node import Node

class DiGraph(GraphInterface):

    _graphNodes : dict
    _modeCount : int
    _edgeCount : int
    _edges : dict
    _inEdge : dict


    def __init__(self):
        self._graphNodes = {}
        self._modeCount = 0
        self._edgeCount = 0
        self._edges = {}
        self._inEdge = {}


    def v_size(self) -> int:
        if self._graphNodes is None :
            return 0
        return len(self._graphNodes)



    def e_size(self) -> int:
        return self._edgeCount


    def get_all_v(self) -> dict:
        return self._graphNodes


    def all_in_edges_of_node(self, id1: int) -> dict:
        if self._graphNodes is None or self._graphNodes.get(id1) is None :
            return None
        return self._inEdge.get(id1)

    def all_out_edges_of_node(self, id1: int) -> dict:
        if self._graphNodes is None or self._graphNodes.get(id1) is None:
            return None
        return self._edges.get(id1)

    def get_mc(self) -> int:
        return self._modeCount

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if self._graphNodes is None :
            return False
        if id1 not in self._graphNodes or id2 not in self._graphNodes :
            return False
        if id2 in self.all_out_edges_of_node(id1) :
            return False
        self._modeCount +=1
        self._edgeCount+=1
      #  tmp : dict= {id2 : weight , id1 : weight}
        self._edges[id1] = {id2 : weight}

        self._inEdge[id2]= {id1 : weight}
        return True






    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id in self._graphNodes :
            return False
        self._modeCount+=1
        self._graphNodes[node_id] = Node(node_id, pos)
                                         #pos if pos is not None else None)

        self._edges[node_id]= None
        self._inEdge[node_id]= None
        return True


    def remove_node(self, node_id: int) -> bool:
        if node_id not in self._graphNodes :
            return False
        self._modeCount += 1
        for x in self._edges[node_id] :
            del(self._inEdge[x][node_id])
        for x in self._inEdge[node_id] :
            del(self._edges[x][node_id])
        del (self._graphNodes[node_id])
        del (self._edges[node_id])
        del (self._inEdge[node_id])
        return True






        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if self._graphNodes is None:
            return False
        if node_id1 not in self._graphNodes or node_id2 not in self._graphNodes:
            return False
        if id2 not in self.all_out_edges_of_node(id1):
            return False
        self._modeCount+=1
        self._edgeCount-=1
        del(self._edges[node_id1][node_id2])
        del(self._inEdge[node_id2][node_id1])
        return True



