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
        # All the situations that can happen in case the graph is empty
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
        self.assertEqual(g.v_size(), 5) # after add 5 nose
        g.remove_node(2)
        self.assertEqual(g.v_size(), 4) # after del 1 node

    def test_add_node(self):
        g: GraphInterface = DiGraph()
        g.add_node(0, (1, 1, 0))
        g.add_node(0, (2, 2, 0))
        self.assertEqual(g.v_size(), 1)  # add the same key and doesnt change
        self.assertEqual(g.get_mc(), 1)  # MC dont change
        # check if the "new node" don't switch node 0
        self.assertEqual(g.get_all_v().get(0).get_pos(), (1, 1, 0))

    def test_add_edge(self):
        g: GraphInterface = DiGraph()
        for n in range(4):
            g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(0, 2, 1)
        self.assertEqual(g.e_size(), 2)  # after add 2 edge
        self.assertEqual(g.get_mc(), 6)
        # the next 2 edge should not count.
        g.add_edge(0, 1, 1)
        g.add_edge(0, 1, 2.5)
        self.assertEqual(g.e_size(), 2)
        self.assertEqual(g.get_mc(), 6)
        self.assertFalse(g.add_edge(0, 0, 1.2))  # can not add edge between node to himself.

    def test_remove_edge(self,):
        g: GraphInterface = DiGraph()
        print(g.remove_edge(0, 4))
        for n in range(4):
            g.add_node(n)
        self.assertFalse(g.remove_edge(0, 1))  # edge dont exist
        g.add_edge(0, 1, 1)
        g.add_edge(0, 2, 1)
        g.remove_edge(0, 1)
        self.assertEqual(1, g.e_size())  # 2 - 1 = 1

    def test_remove_node(self):
        g: GraphInterface = DiGraph()
        for n in range(4):
            g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(0, 2, 1)
        g.add_edge(0, 3, 1.1)
        g.add_edge(1, 0, 4)
        self.assertEqual(4, g.e_size())  # after add 4 edge
        g.remove_node(0)
        self.assertEqual(0, g.e_size())  # all edge connect to node 0 so all need to remove

    def test_all_in_out_edges_of_node(self):
        g: GraphInterface = DiGraph()
        for n in range(4):
            g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(0, 2, 1)
        g.add_edge(0, 3, 1.1)

        print("should be {1: 1, 2: 1, 3: 1.1} we get:", g.all_out_edges_of_node(0))
        self.assertEqual({}, g.all_out_edges_of_node(1))  # only in edge to node 1, 0 out edge
        self.assertEqual({0: 1}, g.all_in_edges_of_node(1))
        self.assertEqual({}, g.all_out_edges_of_node(14))  # node dont exist should be empty

    def test_get_MC(self):
        g: GraphInterface = DiGraph()
        for n in range(4):
            g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(0, 2, 1)
        g.add_edge(0, 3, 1.1)
        self.assertEqual(7, g.get_mc())  # after 7 change in the graph
        g.remove_node(0)
        # 1 node delete and 3 edge but only 1 mode_count add
        self.assertEqual(0, g.e_size())
        self.assertEqual(8, g.get_mc())












if __name__ == '__main__':
    unittest.main()
