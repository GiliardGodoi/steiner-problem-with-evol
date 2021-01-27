from ga4stpg.graph.disjointsets import DisjointSets
from ga4stpg.graph.priorityqueue import PriorityQueue
from ga4stpg.graph.reader import SteinerTreeProblem

class EvaluateKruskalBased:

    def __init__(self, stpg : SteinerTreeProblem, penality_function=None) :
        self.STPG = stpg

        if callable(penality_function):
            self.penality_function = penality_function
        else:
            self.penality_function = lambda k : (k - 1) * 1_000


    def vertices_from_chromosome(self, chromosome):
        ''' Identifica todos os vértices da solução candidata (terminais e não terminais)
        '''

        nro_vertices = self.STPG.nro_nodes
        terminals = self.STPG.terminals

        non_terminals = (v for v in range(1, nro_vertices+1) if v not in terminals)

        vertices = set(v for v, g in zip(non_terminals, chromosome) if int(g)).union(terminals)

        return vertices

    def __call__(self, chromosome, **kwargs):

        GRAPH = self.STPG.graph

        penality = self.penality_function

        vertices = self.vertices_from_chromosome(chromosome)

        # instânciando variáveis e funções auxiliares
        queue = PriorityQueue()
        dones = set()

        # adiciona uma aresta se os vértices extremos da aresta
        # estão contidos no conjunto vertices
        # mantém essas arestas em uma fila de prioridades para
        # formar uma MST baseado no algoritmo de Kruskal
        # (o trabalho de Kapsalis utilizava o algoritmo de Prim)
        for v in vertices:
            dones.add(v)
            for u in GRAPH.adjacent_to(v):
                if (u in vertices) and (u not in dones):
                    weight = GRAPH.weight(v,u)
                    queue.push(weight, (v, u, weight))

        ## Monta a MST baseado no algoritmo de Kruskal
        DS = DisjointSets()
        for v in vertices:
            DS.make_set(v)

        total_cost = 0
        while queue:
            v, u, weight = queue.pop()
            if DS.find(v) != DS.find(u):
                total_cost  += weight
                DS.union(v, u)
        # Repare que não construimos a MST mas apenas
        # definimos os conjuntos disjuntos.

        # a quantidade de partições se refere a
        # quantidade de parents distintos temos no conjunto disjunto.
        qtd_partition = len(DS.get_disjoint_sets())

        total_cost += penality(qtd_partition)

        return total_cost, qtd_partition

