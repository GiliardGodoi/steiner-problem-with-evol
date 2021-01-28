from random import sample

from ga4stpg.edgeset import EdgeSet
from ga4stpg.graph import UGraph

class CrossoverPrimRST:

    def __init__(self, stpg):
        self.stpg = stpg

    def __call__(self, parent_a, parent_b):
        assert isinstance(parent_a, EdgeSet), f'parent_a has to be EdgeSet type. Give was {type(parent_a)}'
        assert isinstance(parent_b, EdgeSet), f'parent_b has to be EdgeSet type. Give was {type(parent_b)}'
        stpg = self.stpg
        terminals = set(stpg.terminals)
        done = set()
        result = EdgeSet()

        subgraph = UGraph()
        for edge in parent_a:
            u, v = edge
            subgraph.add_edge(u, v)
        for edge in parent_b:
            u, v = edge
            subgraph.add_edge(u, v)

        vi = terminals.pop()
        done.add(vi)

        edges = set()
        for u in subgraph.adjacent_to(vi):
            edges.add((vi, u))

        while edges and terminals:
            edge = sample(edges, k=1)[0]
            v, w = edge
            if w not in done:
                done.add(w)
                result.add(v, w)
                terminals.discard(w)
                for u in subgraph.adjacent_to(w):
                    if u not in done: edges.add(w, u)
            edges.discard((v, w))

        return result
