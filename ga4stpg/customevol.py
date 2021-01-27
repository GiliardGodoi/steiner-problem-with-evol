
import time
from copy import copy
from random import choices, random, sample
from typing import Any, Callable, Generator, Iterable, Iterator, List, Optional, Sequence, Union
from uuid import uuid4

from evol import Evolution, Individual
from evol.conditions import Condition
from evol.exceptions import StopEvolution
from evol.population import BasePopulation
from evol.population import Population
from evol.step import EvolutionStep
from evol.utils import select_arguments


class GeneticEvolution(Evolution):

    def __copy__(self) :
        result = GeneticEvolution()
        result.chain = copy(self.chain)
        return result

    def select(self,
               selection_func: Callable,
               name: Optional[str] = 'selection',
               **kwargs) -> 'Evolution':

        return self._add_step(SelectStep(name=name, selection_func=selection_func, **kwargs))

    def crossover(self,
                  combiner: Callable,
                  name: Optional[str] = 'crossover',
                  **kwargs) -> 'Evolution':

        return self._add_step(CrossoverStep(name=name, combiner=combiner, **kwargs))

    def normalize(self,
                 norm_function: Callable,
                 name: Optional[str] = 'normalization',
                 **kwargs) -> 'Evolution' :

        return self._add_step(NormalizationStep(name=name, norm_function=norm_function, **kwargs))


class GeneticPopulation(BasePopulation):
    """Population of Individuals

    :param chromosomes: Iterable of initial chromosomes of the Population.
    :param eval_function: Function that reduces a chromosome to a fitness.
    :param maximize: If True, fitness will be maximized, otherwise minimized.
        Defaults to True.
    :param generation: Generation of the Population. This is incremented after
        each breed call. Defaults to 0.
    :param intended_size: Intended size of the Population. The population will
        be replenished to this size by .breed(). Defaults to the number of
        chromosomes provided.
    :param checkpoint_target: Target for the serializer of the Population. If
        a serializer is provided, this target is ignored. Defaults to None.
    :param serializer: Serializer for the Population. If None, a new
        SimpleSerializer is created. Defaults to None.
    :param concurrent_workers: If > 1, evaluate individuals in {concurrent_workers}
        separate processes. If None, concurrent_workers is set to n_cpus. Defaults to 1.
    """

    def __init__(self,
                 chromosomes: Iterable,
                 eval_function: Callable[..., float],
                 maximize: bool = True,
                 generation: int = 0,
                 intended_size: Optional[int] = None,
                 checkpoint_target: Optional[str] = None,
                 serializer=None,
                 concurrent_workers: Optional[int] = 1):
        super().__init__(chromosomes=[],
                         eval_function=eval_function,
                         checkpoint_target=checkpoint_target,
                         concurrent_workers=concurrent_workers,
                         maximize=maximize,
                         generation=generation,
                         intended_size=0,
                         serializer=serializer)

        self.individuals = [SteinerIndividual(chromosome=chromosome) for chromosome in chromosomes]
        self.intended_size = intended_size or len(self.individuals)
        self.stoppedby = None
        self.runtime = 0.0
        self.selected_individuals = None

    def __copy__(self):
        result = self.__class__(chromosomes=[],
                                eval_function=self.eval_function,
                                maximize=self.maximize,
                                serializer=self.serializer,
                                intended_size=self.intended_size,
                                generation=self.generation,
                                concurrent_workers=1)  # Prevent new pool from being made
        result.individuals = [copy(individual) for individual in self.individuals]
        result.concurrent_workers = self.concurrent_workers
        result.pool = self.pool
        result.documented_best = self.documented_best
        result.id = self.id
        result.stoppedby = self.stoppedby
        return result

    def breed(self,
              parent_picker: Callable[..., Sequence[Individual]],
              combiner: Callable,
              population_size: Optional[int] = None,
              **kwargs) -> 'BasePopulation':
        """Create new individuals by combining existing individuals.

        This increments the generation of the Population.

        :param parent_picker: Function that selects parents from a collection of individuals.
        :param combiner: Function that combines chromosomes into a new
            chromosome. Must be able to handle the number of chromosomes
            that the combiner returns.
        :param population_size: Intended population size after breeding.
            If None, take the previous intended population size.
            Defaults to None.
        :param kwargs: Kwargs to pass to the parent_picker and combiner.
            Arguments are only passed to the functions if they accept them.
        :return: self
        """
        # raise RuntimeWarning("offspring_generator instanciate with a Individual not a SteinerIndividual")
        # if population_size:
        #     self.intended_size = population_size
        # offspring = offspring_generator(parents=self.individuals,
        #                                 parent_picker=select_arguments(parent_picker),
        #                                 combiner=select_arguments(combiner),
        #                                 **kwargs)
        # self.individuals += list(islice(offspring, self.intended_size - len(self.individuals)))
        ####  self.generation += 1 ## generation should be counted here
        return self

    def evolve(self, evolution: 'Evolution', n: int = 1) -> 'BasePopulation':  # noqa: F821
        """Evolve the population according to an Evolution.

        :param evolution: Evolution to follow
        :param n: Times to apply the evolution. Defaults to 1.
        :return: Population
        """
        result = copy(self)
        start = time.perf_counter()
        try:
            for _ in range(n):
                Condition.check(result)
                for step in evolution:
                    result = step.apply(result)
            else :
                result.stoppedby = "IterationLimit"

        except StopEvolution as error :
            result.stoppedby = str(error)

        finally:
            result.runtime = time.perf_counter() - start

        # never put a return statement at finally block
        # altought you deserve everthing bad that to you
        return result

    #def _update_documented_best(self):
    def _update_documented_best(self):
        """Update the documented best"""
        current_best = self.current_best

        if (self.documented_best is None
            or (current_best.cost < self.documented_best.cost)):
            self.documented_best = copy(current_best)
            self.documented_best.last_improvement = self.generation

    def evaluate(self, lazy: bool = False) -> Population:
        """Evaluate the individuals in the population.

        This evaluates the fitness of all individuals. If lazy is True, the
        fitness is only evaluated when a fitness value is not yet known. In
        most situations adding an explicit evaluation step is not needed, as
        lazy evaluation is implicitly included in the operations that need it
        (most notably in the survive operation).

        :param lazy: If True, do no re-evaluate the fitness if the fitness is known.
        :return: self
        """
        for individual in self.individuals:
            individual.evaluate(eval_function=self.eval_function, lazy=False)

        return self

    def select(self,
               selection_func : Callable,
               **kwargs) -> 'Population':

        self.selected_individuals  = selection_func(self.individuals, **kwargs)

        return self

    def crossover(self,
                    combiner : Callable,
                    n_parents: Optional[int] = 2,
                    intended_size : Optional[int] = None,
                    **kwargs
                    ):
        if self.selected_individuals is None:
            raise RuntimeError("select individuals first")

        if not intended_size:
            intended_size = self.intended_size or len(self.individuals)

        count = 0
        new_population = list()

        while count < intended_size:

            try:
                parents = sample(self.selected_individuals, k=n_parents)
            except ValueError as error:
                raise error

            offspring = combiner(*[p.chromosome for p in parents], **kwargs)

            if isinstance(offspring, (Generator, list, tuple)):
                for chromosome in offspring:
                    new_population.append(SteinerIndividual(chromosome=chromosome))
                    count += 1
            else:
                new_population.append(SteinerIndividual(chromosome=offspring))
                count += 1

        self._update_population(new_population)

        return self

    def normalize(self,
                  norm_function : Callable):

        self.individuals = norm_function(self.individuals)

        return self

    def _update_population(self, new_population):
        assert len(new_population) == self.intended_size, "new populations has not the intended size"
        self.individuals = new_population

    def callback(self,
                 callback_function: Callable[..., None],
                 **kwargs) -> 'BasePopulation':
        """
        Performs a callback function on the population.
        Can be used for custom logging/checkpointing.
        :param callback_function: Function that accepts the population
        as a first argument.
        :return:
        """
        callback_function(self, **kwargs)
        return self


class SteinerIndividual:

    def __init__(self, chromosome: Any, cost: Optional[float] = None):
        self.id = f"{str(uuid4())[:6]}"

        self.age = 0
        self.last_improvement = 0
        self.chromosome = chromosome

        self._cost = cost
        self._fitness = None
        self.qtd_partitions = None

    def __copy__(self):
        result = self.__class__(self.chromosome, cost=self.cost)

        result.id = self.id
        result.age = self.age
        result.last_improvement = self.last_improvement
        result.qtd_partitions = self.qtd_partitions
        result.fitness = self.fitness

        return result

    @property
    def is_normal(self):
        return not self._fitness is None

    @property
    def is_evaluated(self):
        return not self._cost is None

    @property
    def fitness(self):
        return self._fitness

    @fitness.setter
    def fitness(self, value):
        self._fitness = value

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        self._cost = value
        self._fitness = None

    @property
    def is_connected(self):
        '''If the graph represented by the chromosome has only one partition,
        It means that it is connected.
        '''
        if self.qtd_partitions is None:
            RuntimeError('nro of components is unknow')

        return self.qtd_partitions == 1

    def evaluate(self, eval_function: Callable[..., float], lazy: bool = False):
        """Evaluate the fitness of the individual.

        :param eval_function: Function that reduces a chromosome to a fitness.
        :param lazy: If True, do no re-evaluate the fitness if the fitness is known.
        """
        # print(self.id, self.age, self.cost, self.is_evaluated)
        if self._cost is None or not lazy:
            result = eval_function(self.chromosome)

            if isinstance(result, tuple) and len(result) == 2:
                self.cost, self.qtd_partitions = result
            elif isinstance(result, (int, float)):
                self.cost = result
            else:
                raise RuntimeError(f"Problem to understand the evaluation return {result}")

            # print(self.id, self.age, self.cost, self.is_evaluated)


    def mutate(self,
                mutate_function: Callable[..., Any],
                probability: float = 1.0,
                **kwargs):
        """Mutate the chromosome of the individual.

        :param mutate_function: Function that accepts a chromosome and returns a mutated chromosome.
        :param probability: Probability that the individual mutates.
            The function is only applied in the given fraction of cases.
            Defaults to 1.0.
        :param kwargs: Arguments to pass to the mutation function.
        """
        if probability == 1.0 or random() < probability:
            self.chromosome = mutate_function(self.chromosome, **kwargs)
            self.cost = None


class SelectStep(EvolutionStep):

    def apply(self, population: GeneticPopulation) -> GeneticPopulation:
        return population.select(**self.kwargs)


class CrossoverStep(EvolutionStep):

    def apply(self, population: GeneticPopulation) -> GeneticPopulation:
        return population.crossover(**self.kwargs)


class NormalizationStep(EvolutionStep):

    def apply(self, population: BasePopulation) -> BasePopulation:
        return population.normalize(**self.kwargs)