from __future__ import annotations
from nodes_modules_cosine_similarity import *
import numpy as np

def separation_vector_calculator(CosineMat,
                                 modules):
    
    nodes_modules_cosine_matrix, n_nodes = nodes_modules_cosine_similarity(CosineMat = CosineMat,
                                                                           modules = modules)    
    
    separation_vector = np.zeros(n_nodes)
    
    for node_id in range(n_nodes):
        closest_module2node_id = int(np.argmax(nodes_modules_cosine_matrix[node_id, :]))
        module = modules[closest_module2node_id]
        separation_vector[node_id] = np.mean(CosineMat[node_id, list(module)])
        
    return separation_vector