import unittest

from src import GraphInterface
from src.DiGraph import DiGraph


class TestGraphDi(unittest.TestCase):

    def test_add_edge(self):
        g: DiGraph = DiGraph()
        for n in range(4):
            g.add_node(n)
        self.assertFalse(g.add_edge(0, 11, 2.5))  # key not exist
        self.assertEqual(g.e_size(), 0, " should be 0")
        g.add_edge(0, 1, 1.1)
        g.add_edge(0, 2, 2.2)
        print(g.all_out_edges_of_node(0))
        self.assertEqual(g.e_size(), 2)

    def test_empty_graph(self):
        g: GraphInterface = DiGraph()

        self.assertEqual(0, g.v_size())
        self.assertEqual(0, g.e_size())
        self.assertEqual({}, g.get_all_v())
        self.assertEqual({}, g.all_out_edges_of_node(0))
        self.assertEqual({}, g.all_in_edges_of_node(0))
        self.assertEqual(0, g.get_mc())
        self.assertFalse(g.add_edge(0, 0, 0))

    def test_v_size(self):
        g: GraphInterface = DiGraph()
        for n in range(5):
            g.add_node(n)
        self.assertEqual(g.v_size(), 5)
        g.remove_node(2)
        self.assertEqual(g.v_size(), 4)

    def test_add_node(self):
        g: GraphInterface = DiGraph()
        g.add_node(0, (1, 1, 0))
        g.add_node(0, (2, 2, 0))
        self.assertEqual(g.v_size(), 1)
        self.assertEqual(g.get_mc(), 1)
        # check if the "new node" don't switch node 0
        self.assertEqual(g.get_all_v().get(0).get_pos(), (1, 1, 0))

    def test_add_edge(self):
        g: GraphInterface = DiGraph()
        for n in range(4):
            g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(0, 2, 1)
        self.assertEqual(g.e_size(), 2)
        self.assertEqual(g.get_mc(), 6)
        # the next 2 edge should not count.
        g.add_edge(0, 1, 1)
        g.add_edge(0, 1, 2.5)
        self.assertEqual(g.e_size(), 2)
        self.assertEqual(g.get_mc(), 6)
        # can not add edge between node to himself.
        self.assertFalse(g.add_edge(0, 0, 1.2))

    def test_remove_edge(self):
        g: GraphInterface = DiGraph()
        for n in range(4):
            g.add_node(n)
        self.assertFalse(g.remove_edge(0, 1))
        g.add_edge(0, 1, 1)
        g.add_edge(0, 2, 1)
        g.remove_edge(0, 1)
        self.assertEqual(1, g.e_size())

    def test_remove_node(self):
        g: GraphInterface = DiGraph()
        for n in range(4):
            g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(0, 2, 1)
        g.add_edge(0, 3, 1.1)
        g.add_edge(1, 0, 4)
        self.assertEqual(4, g.e_size())
        g.remove_node(0)
        self.assertEqual(0, g.e_size())

    def test_all_in_out_edges_of_node(self):
        g: GraphInterface = DiGraph()
        for n in range(4):
            g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(0, 2, 1)
        g.add_edge(0, 3, 1.1)

        print("should be {1: 1, 2: 1, 3: 1.1} we get:", g.all_out_edges_of_node(0))
        self.assertEqual({}, g.all_out_edges_of_node(1))
        self.assertEqual({}, g.all_out_edges_of_node(14))

        self.assertEqual({0: 1}, g.all_in_edges_of_node(1))















if __name__ == '__main__':
    unittest.main()
