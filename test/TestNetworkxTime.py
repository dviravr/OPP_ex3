import time
import random
import unittest
import sys
import json
import networkx as nx
from DiGraph import DiGraph
from GraphAlgo import GraphAlgo
from GraphInterface import GraphInterface
from GraphAlgoInterface import GraphAlgoInterface


class TestNetworkxTime(unittest.TestCase):

    def setUp(self):
        file_name = '../data/G_10_80_0.json'
        file_name = '../data/G_100_800_0.json'
        file_name = '../data/G_1000_8000_0.json'
        file_name = '../data/G_10000_80000_0.json'
        file_name = '../data/G_20000_160000_0.json'
        file_name = '../data/G_30000_240000_0.json'
        self.g = nx.DiGraph()
        with open(file_name, 'r') as json_file:
            data = json.load(json_file)
            self.g.add_nodes_from(
                elem['id']
                for elem in data['Nodes']
            )
            for elem in data['Edges']:
                self.g.add_edges_from([(elem['src'], elem['dest'])], weight=elem['w'])
        nodes: list = list(self.g)
        self.n1 = random.choice(nodes)
        self.n2 = random.choice(nodes)
        while self.n1 == self.n2:
            self.n2 = random.choice(nodes)
        print(self.n1, self.n2)
        sys.setrecursionlimit(len(nodes) + 1000)
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))

    def test_shortest_path_time(self):
        print(nx.shortest_path(self.g, self.n1, self.n2))

    # def test_connected_component_time(self):
    #     print(nx.node_connected_component(self.g, self.n1))

    def test_connected_components_time(self):
        print(nx.strongly_connected_components(self.g))


if __name__ == '__main__':
    unittest.main()
