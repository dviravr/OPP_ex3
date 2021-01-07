import unittest
from GraphAlgo import GraphAlgo
from GraphAlgoInterface import GraphAlgoInterface


class TestGraphAlgo(unittest.TestCase):

    def setUp(self):
        self.ga: GraphAlgoInterface = GraphAlgo()
        self.ga.load_from_json('../data/D0.json')

    def test_get_graph(self):
        # todo: complete
        pass

    def test_save(self):
        # todo: complete
        pass

    def test_shortest_path(self):
        self.assertEqual(self.ga.shortest_path(0, 4), (5.4, [0, 1, 3, 2, 4]))

    def test_connected_component(self):
        self.assertEqual(self.ga.connected_component(4), [4, 5])

    def test_connected_components(self):
        self.assertEqual(len(self.ga.connected_components()), 4)


if __name__ == '__main__':
    unittest.main()
