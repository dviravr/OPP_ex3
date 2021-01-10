import random
import sys
import time
import unittest

from GraphAlgo import GraphAlgo
from GraphAlgoInterface import GraphAlgoInterface


class TestAlgoTime(unittest.TestCase):

    def setUp(self):
        file_name = '../data/G_30000_240000_0.json'
        self.ga: GraphAlgoInterface = GraphAlgo()
        self.ga.load_from_json(file_name)
        nodes: list = list(self.ga.get_graph().get_all_v())
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
        print(self.ga.shortest_path(self.n1, self.n2))

    def test_connected_component_time(self):
        print(self.ga.connected_component(self.n2))

    def test_connected_components_time(self):
        print(self.ga.connected_components())


if __name__ == '__main__':
    unittest.main()
