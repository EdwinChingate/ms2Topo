from __future__ import annotations
import numpy as np

def cohesion_vector_calculator(CosineMat,
                               modules):
    
    n_nodes = len(CosineMat)
    cohesion_vector = np.zeros(n_nodes)
    
    for module in modules:
        for node in module:
            node_id = int(node)
            if len(module) > 1:
                cohesion_vector[node_id] = (np.sum(CosineMat[node_id, list(module)]) - 1) / (len(module) - 1)
            else:
                cohesion_vector[node_id] = 0
            
    return cohesion_vector        