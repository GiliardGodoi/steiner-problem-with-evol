import unittest
from os import path

from ga4stpg.graph.graph import UndirectedWeightedGraph as Graph
from ga4stpg.graph.algorithms import prim
from ga4stpg.graph.reader import ReaderORLibrary

class TestMinimumSpanningTree(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        arquivo = path.join("datasets", "ORLibrary", "steinb1.txt")
        reader = ReaderORLibrary()
        cls.stp = reader.parser(arquivo)
        cls.graph = cls.stp.graph

    def test_mst_cost(self):
        start_node = 34
        _, cost = prim(self.graph, start_node)

        self.assertGreater(cost,0)
        self.assertEqual(cost,238)


if __name__ == "__main__" :
    unittest.main()