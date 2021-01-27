import unittest
from os import path

from ga4stpg.binary.coder import Coder
from ga4stpg.graph import ReaderORLibrary
from ga4stpg.graph.algorithms import prim
from ga4stpg.graph.graph import UndirectedGraph as UGraph
from ga4stpg.graph.graph import UndirectedWeightedGraph as UWGraph
from ga4stpg.binary import random_binary
from ga4stpg.graph.steiner import (prunning_mst, shortest_path,
                           shortest_path_origin_prim,
                           shortest_path_with_origin)

class TestBinaryCoder(unittest.TestCase):

    def setUp(self):
        filename = path.join('datasets', 'ORLibrary', 'steinb15.txt')
        self.stpg  = ReaderORLibrary().parser(filename)

    def test_EncoderMST(self):

        stpg  = self.stpg
        graph = self.stpg.graph

        mst, cost = prim(graph, 1)
        tree = UGraph()

        for u, v in mst.items():
            tree.add_edge(v,u)

        coder = Coder(STPG=stpg)

        chromosome = coder.treegraph2binary(tree)

        self.assertIsInstance(chromosome, str)

        expected_lenght = stpg.nro_nodes - stpg.nro_terminals
        self.assertEqual(len(chromosome), expected_lenght)

        self.assertEqual(chromosome, '1' * expected_lenght)

    def test_DecoderRandomChromosome(self):

        stpg  = self.stpg
        graph = self.stpg.graph
        stpg_vertices = set(graph.vertices)

        expected_lenght = stpg.nro_nodes - stpg.nro_terminals

        random_chromosome = random_binary(expected_lenght)

        self.assertEqual(len(random_chromosome), expected_lenght)

        coder = Coder(STPG=stpg)
        subgraph = coder.binary2treegraph(random_chromosome)

        self.assertIsInstance(subgraph, UGraph)

        terminals = self.stpg.terminals

        sub_vertices = coder.vertices_from_chromosome(random_chromosome)

        self.assertTrue(terminals.issubset(sub_vertices))
        self.assertTrue(sub_vertices.issubset(stpg_vertices))



    @unittest.skip
    def test_DecoderHeuristic(self):

        stpg  = self.stpg
        graph = self.stpg.graph

        steiner_tree, cost = shortest_path_origin_prim(graph,1,stpg.terminals)

        coder = Coder(STPG=stpg)

        chromosome = coder.treegraph2binary(steiner_tree)

        self.assertIsInstance(chromosome, str)

        vertices_st = set(steiner_tree.vertices)
        vertices_cr = coder.vertices_from_chromosome(chromosome)

        self.assertEqual(vertices_cr, vertices_st)

        subtree = coder.binary2treegraph(chromosome)

        st_edges = set((min(edge), max(edge)) for edge in steiner_tree.gen_undirect_edges())
        sb_edges = set((min(edge), max(edge)) for edge in subtree.gen_undirect_edges())

        self.assertEqual(st_edges, sb_edges)






if __name__ == "__main__" :
    unittest.main()