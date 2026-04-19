from __future__ import annotations
from modules_mutator import *
import numpy as np

def mutating_population(population_matrix,
                        population):
    
    new_population = []
    n_individuals = len(population)
    n_nodes = len(population[0])
    rng = np.random.default_rng()
    mutation_size_vector = rng.choice(np.arange(n_nodes),
                                      size = n_individuals,
                                      replace = True)     
    
    for individual_1_id in range(n_individuals):
        individual = population[individual_1_id]
        size = mutation_size_vector[individual_1_id]
        mutated_individual, population_matrix, duplicated = modules_mutator(population_matrix = population_matrix,
                                                                            individual = individual,
                                                                            n_nodes = n_nodes,
                                                                            size = size)
        if not duplicated:
            new_population.append(mutated_individual)
        
    return [population + new_population, population_matrix]