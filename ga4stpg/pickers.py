from itertools import cycle, product
from random import choices

def random_picker(population):
    while True:
        yield tuple(choices(population, k=2))

def best_against_all(population):
    bestdocumented = population.documented_best

    if bestdocumented is None:
        yield from random_picker(population)

    for other in cycle(population):
        yield (bestdocumented, other)

def cartesian_product(population):
    container = product(population, repeat=2)

    for result in container:
        yield result