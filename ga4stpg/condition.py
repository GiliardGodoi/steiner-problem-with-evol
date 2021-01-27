
from evol.conditions import Condition
from evol.exceptions import StopEvolution
from ga4stpg.graph import SteinerTreeProblem
from ga4stpg.graph.util import is_steiner_tree

from .customevol import GeneticPopulation as Population

class IterationLimit(Condition):

    def __init__(self, limit : int):
        super().__init__(None)
        self.limit = limit

    def __call__(self, population : Population):
        if population.generation >= self.limit:
            raise StopEvolution("max_generation_reached")


class Stagnation(Condition):

    def __init__(self, interval : int):
        self.interval = interval

    def __call__(self, population : Population):
        generation = population.generation
        last_time_improvement = population.documented_best.last_improvement

        if (generation - last_time_improvement) > self.interval:
            raise StopEvolution("Stagnation")

class BestKnownReached(Condition):

    def __init__(self, global_optimum : int):
        self.global_optimum = global_optimum

    def __call__(self, population : Population):
        if (population.documented_best
           and population.documented_best.cost == self.global_optimum):
           raise StopEvolution("BestKnowReached")


class BestSteinerTreeReachead(Condition):

    def __init__(self,
                 global_optimum : int,
                 STPG : SteinerTreeProblem,
                 decoder=None):

        self.global_optimum = global_optimum
        self.STPG = STPG

        if callable(decoder):
            self.decoder = decoder
            self.is_to_use_decoder_function = True
        else:
            self.is_to_use_decoder_function = False

    def __call__(self, population : Population):

        best_solution = population.documented_best

        if (best_solution is not None and best_solution.cost == self.global_optimum):

            if self.is_to_use_decoder_function :
                steiner_tree = self.decoder(best_solution.chromosome)
            else:
                steiner_tree = best_solution.chromosome

            result, _ = is_steiner_tree(steiner_tree, self.STPG)

            if result :
                raise StopEvolution("BestKnownSteinerTreeReached")
