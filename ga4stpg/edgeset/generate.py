from ga4stpg.edgeset import EdgeSet, UEdge
from ga4stpg.graph import SteinerTreeProblem
from ga4stpg.graph.disjointsets import DisjointSets
from random import randint, sample

def gen_random_kruskal(stpg : SteinerTreeProblem):
    pass

def gen_random_prim(stpg : SteinerTreeProblem):

    terminals = set(stpg.terminals)
    graph = stpg.graph

    vi = sample(range(1, stpg.nro_nodes + 1), k=1)[0]

    done   = set()
    edges  = set()
    result = EdgeSet()

    done.add(vi)
    terminals.discard(vi)
    for w in graph.adjacent_to(vi):
        edges.add((vi, w))

    while edges and terminals:
        edge = sample(edges, k=1)[0]
        v, w = edge
        if w not in done:
            done.add(w)
            result.add(v, w)
            terminals.discard(w)
            for u in graph.adjacent_to(w):
                if u not in done: edges.add((w, u))
        edges.discard((v, w))

    return result

def gen_random_walk(stpg : SteinerTreeProblem):
    pass
