from operator import attrgetter
from random import choice

from graph import Graph
from graph.util import compose
from graph.steiner import prunning_mst

class PrunningCrossover:

    def __init__(self, stpg):
        self.STPG = stpg
        self.terminals = list(stpg.terminals)

    def __call__(self, red : Graph, blue : Graph):

        g_union, _a, _b = compose(red, blue)

        z = choice(self.terminals)

        g_child, _ = prunning_mst(g_union, z, self.STPG.terminals)

        return g_child
