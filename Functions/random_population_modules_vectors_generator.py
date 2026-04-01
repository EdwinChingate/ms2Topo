from __future__ import annotations
from unique_individual_generator import *

def random_population_modules_vectors_generator(n_nodes,
                                                population_matrix,
                                                population_size):
    
    population = []
    
    for individual_id in range(population_size):
        modules_vector, population_matrix, duplicated = unique_individual_generator(n_nodes = n_nodes,
                                                                                    population_matrix = population_matrix)
        if not duplicated:
            population.append(modules_vector)
        
    return [population, population_matrix]    