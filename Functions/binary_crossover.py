from __future__ import annotations
import numpy as np

# TODO: unresolved names: n_crossover_nodes, nodes_ids_vector

def binary_crossover(individual_1,
                     individual_2):  
    
    child = individual_2.copy()
    rng = np.random.default_rng()
    nodes_from_individual_1 = rng.choice(nodes_ids_vector,
                                         size = n_crossover_nodes,
                                         replace = False).tolist()
    child[nodes_from_individual_1] = individual_1[nodes_from_individual_1].copy()
    
    return child