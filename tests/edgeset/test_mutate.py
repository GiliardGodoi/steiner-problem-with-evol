from os import path
import unittest

from ga4stpg.edgeset import EdgeSet
from ga4stpg.edgeset.generate import gen_random_prim
from ga4stpg.edgeset.mutate import MutateReconectingComponents
from ga4stpg.graph import UGraph
from ga4stpg.graph.reader import ReaderORLibrary
from ga4stpg.graph.util import is_steiner_tree


class TestMutateReconectingComponents(unittest.TestCase):

    def test_simpliest(self):
        filename = path.join('datasets', 'ORLibrary', 'steinb18.txt')
        stpg  = ReaderORLibrary().parser(filename)

        mutate = MutateReconectingComponents(stpg)

        after = gen_random_prim(stpg)
        self.assertIsInstance(after, EdgeSet)

        before = mutate(after)

        self.assertNotEqual(after, before)

        tree = UGraph()

        for edge in before:
            v, u = edge
            tree.add_edge(v, u)

        _, response = is_steiner_tree(tree, stpg)
        self.assertTrue(response['all_terminals_in'])
        self.assertFalse(response['has_cycle'])
        self.assertTrue(response['all_edges_are_reliable'])
        self.assertTrue(response['graph_is_connected'])
        # It is not possible to grant that 'all_leaves_are_terminals'

if __name__ == "__main__":
    unittest.main()
