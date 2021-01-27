'''
Code : class
    Enconde
'''
from ga4stpg.graph import SteinerTreeProblem
from ga4stpg.graph.disjointsets import DisjointSets
from ga4stpg.graph.graph import UndirectedGraph as UGraph
from ga4stpg.graph.graph import UndirectedWeightedGraph as UWGraph
from ga4stpg.graph.priorityqueue import PriorityQueue


class Coder:
    '''Coder : class
    '''
    def __init__(self, STPG : SteinerTreeProblem):
        '''STPG hold the graph instance from the problem'''
        self.STPG = STPG

    def vertices_from_chromosome(self, chromosome):
        '''Computes the steiner vertices from a binary chromosome'''
        nro_vertices = self.STPG.nro_nodes
        terminals = self.STPG.terminals

        non_terminals = (v for v in range(1, nro_vertices+1) if v not in terminals)

        vertices = set(v for v, g in zip(non_terminals, chromosome) if int(g)).union(terminals)

        return vertices

    def treegraph2binary(self, subgraph):
        '''Encode a tree graph into a binary string'''

        terminals = set(self.STPG.terminals)
        nro_vertices = self.STPG.nro_nodes

        genes = ['0'] * nro_vertices # all vertices in the instance problem

        # vertices in the subgraph (partial solution)
        # include terminals and non-terminals
        for v in subgraph.vertices:
            genes[v-1] = '1'

        # choosing only the non_terminals positions
        genes = (gene for node, gene in enumerate(genes, start=1) if node not in terminals)

        return ''.join(genes)

    def binary2treegraph(self, chromosome):
        '''Converts from BinaryChromosome to TreeChromosome'''

        GRAPH = self.STPG.graph

        queue = PriorityQueue()
        disjointset = DisjointSets()
        subgraph = UGraph()
        dones = set()

        # todos os vértices esperados na solução parcial
        vertices = self.vertices_from_chromosome(chromosome)

        # adiciona uma aresta se os vértices extremos da aresta
        # estão contidos no conjunto vertices
        # mantém essas arestas em uma fila de prioridades para
        # formar uma MST baseado no algoritmo de Kruskal
        for v in vertices:
            dones.add(v)
            disjointset.make_set(v) # para construir a MST
            subgraph.add_node(v) # garantir a inserção de um vértice isolado
            for u in GRAPH.adjacent_to(v):
                if (u in vertices) and (u not in dones):
                    weight = GRAPH.weight(v, u)
                    queue.push(weight, (v, u))

        while queue:
            v, u = queue.pop()
            if disjointset.find(v) != disjointset.find(u):
                subgraph.add_edge(v, u)
                disjointset.union(v, u)

        return subgraph
