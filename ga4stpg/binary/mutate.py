from random import randrange, random

def flip_onebit(chromosome):
    flip = lambda x : '1' if x == '0' else '0'
    index = randrange(0, len(chromosome))
    return chromosome[:index] + flip(chromosome[index]) + chromosome[index+1:]

def flip_nbit(chromosome, flip_probability=0.2):
    flip = lambda x : '1' if x == '0' else '0'
    newchromosome = [ flip(gene) if random() < flip_probability else gene for gene in chromosome]
    return newchromosome