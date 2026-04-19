from __future__ import annotations
from confirm_new_individual import *
import numpy as np

def unique_individual_generator(n_nodes,
                                population_matrix,
                                max_attempts = 5):
    
    duplicated = True
    checking_unique_count = 0
    
    while (duplicated | checking_unique_count < max_attempts):
        checking_unique_count += 1
        rng = np.random.default_rng()
        modules_vector = rng.choice(np.arange(n_nodes),
                                    size = n_nodes,
                                    replace = True)
        population_matrix, duplicated = confirm_new_individual(population_matrix = population_matrix,
                                                               new_individual = modules_vector)
    return [modules_vector, population_matrix, duplicated]