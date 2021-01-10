import unittest
from src.GraphAlgo import GraphAlgo
from src.GraphAlgoInterface import GraphAlgoInterface


class TestGraphAlgo(unittest.TestCase):

    def setUp(self):
        self.ga: GraphAlgoInterface = GraphAlgo()
        self.ga.load_from_json('../data/D0.json')

    def test_save_load(self):
        g = self.ga.get_graph()
        self.ga.save_to_json('../data/D0-saved.json')
        self.ga.load_from_json('../data/D0-saved.json')
        assert g == self.ga.get_graph()

    def test_shortest_path(self):
        assert self.ga.shortest_path(0, 4) == (5.4, [0, 1, 3, 2, 4])

    def test_connected_component(self):
        assert self.ga.connected_component(4) == [4, 5]

    def test_connected_components(self):
        assert len(self.ga.connected_components()) == 4

    def test_plot(self):
        self.ga.plot_graph()


if __name__ == '__main__':
    unittest.main()
