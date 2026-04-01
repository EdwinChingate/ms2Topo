from __future__ import annotations
import numpy as np

def modules_mutator(individual,
                    n_nodes,
                    size):
    
    modules_ids = list(set(individual.tolist()))
    rng = np.random.default_rng()
    nodes2mutate = rng.choice(np.arange(n_nodes),
                              size = size,
                              replace = True).tolist()                      
    modules_vector = rng.choice(modules_ids,
                                size = size,
                                replace = True).tolist()  
    mutated_individual = individual.copy()
    mutated_individual[nodes2mutate] = modules_vector  
        
    return mutated_individual