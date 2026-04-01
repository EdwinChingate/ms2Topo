from __future__ import annotations
from confirm_new_individual import *
import numpy as np

def binary_crossover(population_matrix,
                     nodes_ids_vector,
                     n_crossover_nodes,
                     individual_1,
                     individual_2,
                     max_attempts = 5):  

    duplicated = True
    child = individual_2.copy()
    checking_unique_count = 0
    
    while (duplicated | checking_unique_count < max_attempts):
        checking_unique_count += 1
        rng = np.random.default_rng()
        nodes_from_individual_1 = rng.choice(nodes_ids_vector,
                                             size = n_crossover_nodes,
                                             replace = False).tolist()
        child[nodes_from_individual_1] = individual_1[nodes_from_individual_1].copy()
        population_matrix, duplicated = confirm_new_individual(population_matrix = population_matrix,
                                                               new_individual = child)
        
    return [child, population_matrix, duplicated]