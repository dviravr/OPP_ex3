import unittest

from DiGraph import DiGraph


class TestGraphDi(unittest.TestCase):

    def test_add_edge(self):
        g = DiGraph()
        for n in range(4):
            g.add_node(n)
        self.assertFalse(g.add_edge(0, 11, 2.5))  # key not exist
        self.assertEqual(g.e_size(), 0, " should be 0")
        g.add_edge(0, 1, 1.1)
        g.add_edge(0, 2, 2.2)
        print(g.all_out_edges_of_node(0))
        self.assertEqual(g.e_size(), 2)

    def test_empty_graph(self):
        g = DiGraph()
        self.assertEqual(0, g.v_size())
        self.assertEqual(0, g.e_size())
        self.assertEqual({}, g.get_all_v())
        self.assertEqual({}, g.all_out_edges_of_node(0))
        self.assertEqual({}, g.all_in_edges_of_node(0))
        self.assertEqual(0, g.get_mc())
        self.assertFalse(g.add_edge(0, 0, 0))


if __name__ == '__main__':
    unittest.main()
