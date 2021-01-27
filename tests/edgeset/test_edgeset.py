import unittest
from typing import Generator, Iterator

from ga4stpg.edgeset import EdgeSet, UEdge


class TestEdgeSet(unittest.TestCase):

    def test_init_empty(self):
        edset = EdgeSet()
        self.assertFalse(len(edset))


if __name__ == '__main__':
    unittest.main()
