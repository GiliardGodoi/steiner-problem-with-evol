from operator import attrgetter

def normalize(individuals, key=attrgetter('cost')):

    major_individual = max(individuals, key=key)

    for individual in individuals:
        individual.fitness = major_individual.cost - individual.cost

    return individuals