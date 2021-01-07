import unittest
from src.DiGraph import DiGraph


class MyTestCase(unittest.TestCase):
    def test_addNode(self):
        g = DiGraph()
        for n in range(4):
            g.add_node(n)
        self.assertFalse(g.add_edge(0, 11, 2.5))
        self.assertEqual(g.e_size(), 0, " should be 0")
        g.add_edge(0, 1, 1.1)
        g.add_edge(0, 2, 2.2)
        print(g.all_out_edges_of_node(0))
        self.assertEqual(g.e_size(), 2)



if __name__ == '__main__':
    unittest.main()
