from __future__ import annotations
from confirm_new_individual import *
import numpy as np

def modules_mutator(population_matrix,
                    individual,
                    n_nodes,
                    size,
                    max_attempts = 5):
    
    duplicated = True
    modules_ids = list(set(individual.tolist()))
    
    rng = np.random.default_rng()
    mutated_individual = individual.copy()
    checking_unique_count = 0
    
    while (duplicated | checking_unique_count < max_attempts):
        checking_unique_count += 1
        nodes2mutate = rng.choice(np.arange(n_nodes),
                                  size = size,
                                  replace = True).tolist()                      
        modules_vector = rng.choice(modules_ids,
                                    size = size,
                                    replace = True).tolist()      
        mutated_individual[nodes2mutate] = modules_vector  
        population_matrix, duplicated = confirm_new_individual(population_matrix = population_matrix,
                                                               new_individual = mutated_individual)
            
    return [mutated_individual, population_matrix, duplicated]