from __future__ import annotations
from ShowDF import *
from confirm_new_individual import *
import numpy as np

# TODO: unresolved names: unique_individual_generator

def random_population_modules_vectors_generator(n_nodes,
                                                population_matrix,
                                                population_size):
    
    population = []
    
    for individual_id in range(population_size):
        rng = np.random.default_rng()
        modules_vector = rng.choice(np.arange(n_nodes),
                                    size = n_nodes,
                                    replace = True)
        
        
        population_matrix, unique_vector = confirm_new_individual(population_matrix = population_matrix,
                                                                  new_individual = modules_vector)
        
        ShowDF(population_matrix)
        population.append(modules_vector)
        unique_individual_generator()
        
    return population    