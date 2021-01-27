
from ga4stpg.graph.disjointsets import DisjointSets
from ga4stpg.graph.reader import SteinerTreeProblem

class EvaluateTreeGraph:

    def __init__(self,
                 stpg: SteinerTreeProblem,
                 penality_function=None,
                 apply_penalization = False):
        self.STPG = stpg

    def penality(self, factor):
        if self.apply_penalization:
            return self.penality_function()


    def __call__(self, tree):

        GRAPH = self.STPG.graph
        total_cost = 0
        qtd_partition = 0
        DS = DisjointSets()

        for v in tree.vertices:
            DS.make_set(v)

        for v, u in tree.gen_undirect_edges():
            if DS.find(v) == DS.find(u):
                ## trocar isso por um log
                print("FOI IDENTIFICADO UM CICLO EM UMA DAS SOLUÇÕES")
            DS.union(v,u)
            total_cost +=  GRAPH.weight(v, u)

        qtd_partition = len(DS.get_disjoint_sets())

        total_cost += self.penality(qtd_partition)

        return total_cost, qtd_partition