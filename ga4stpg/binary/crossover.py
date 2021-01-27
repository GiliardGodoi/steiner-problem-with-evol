from random import sample, choice, random

def pb_cx2_points(parent_a, parent_b, probability=1, **kwargs):
    if random() < probability:
        yield from cx2_points(parent_a, parent_b)
    else:
        yield parent_a
        yield parent_b

def pb_cx1_point(parent_a, parent_b, probability=1, **kwargs):
    if random() < probability:
        yield from cx1_point(parent_a, parent_b)
    else:
        yield parent_a
        yield parent_b

def cx2_points(parent_a, parent_b, **kwargs):
    length_a, length_b = len(parent_a), len(parent_b)
    assert length_a == length_b, "chromosomes doesn't have the same length"
    assert length_a > 0, "chromosome must have length greater than 0"
    points = sample(range(0, length_a), k=2)
    points.sort()
    p1, p2 = points

    yield parent_a[:p1] + parent_b[p1:p2] + parent_a[p2:]
    yield parent_b[:p1] + parent_a[p1:p2] + parent_b[p2:]

def cx1_point(parent_a, parent_b, **kwargs):
    length_a, length_b = len(parent_a), len(parent_b)
    assert length_a == length_b, "chromosomes doesn't have the same length"
    index = choice(range(0, length_a))

    yield parent_a[:index] + parent_b[index:]
    yield parent_b[:index] + parent_a[index:]

def n_points(parent_a, parent_b, n=2, **kwargs):

    length_a, length_b = len(parent_a), len(parent_b)
    assert length_a == length_b, "chromosomes doesn't have the same length"
    assert n <= (length_a - 1) , f"It is allowed only {(length_a - 1)} cuts. It was given {n}"

    def chunck(parent,start, end):
        return parent[start:end]

    points = [0] + sample(range(length_a), k=n) + [length_a]
    points.sort()
    flag = True
    newchromosome = list()
    for start, end in zip(points, points[1:]):
        if flag:
            newchromosome.append(chunck(parent_a, start, end))
        else:
            newchromosome.append(chunck(parent_b, start, end))
        flag = not flag

    return ''.join(newchromosome)

def uniform(chromosome_a, chromosome_b, pbcrossover=0.5, **kwargs):

    assert len(chromosome_a) == len(chromosome_b), "chromosome must have the same length"

    # list comprehension
    chromosome = [ a if random() < pbcrossover else b
                        for a, b in zip(chromosome_a, chromosome_b) ]

    # desta forma se o chromosomo receber uma lista de números inteiros ele também vai funcionar
    if isinstance(chromosome_a, str) or isinstance(chromosome_b, str):
        chromosome = ''.join(chromosome)

    return chromosome
