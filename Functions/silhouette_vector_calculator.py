from __future__ import annotations
from cohesion_vector_calculator import *
import numpy as np
from separation_vector_calculator import *

def silhouette_vector_calculator(CosineMat,
                                 modules):
    
    n_nodes = len(CosineMat)
    
    if n_nodes == 1:
        cohesion_vector = np.array([1])
    else:    
        cohesion_vector = cohesion_vector_calculator(CosineMat = CosineMat,
                                                     modules = modules)
    if len(modules) > 1:
        separation_vector, closest_module_vector = separation_vector_calculator(CosineMat = CosineMat,
                                                                                modules = modules)  
    else:
        separation_vector = np.zeros(n_nodes)
        closest_module_vector = np.zeros(n_nodes).astype(int)
    silhouette_vector = np.zeros(n_nodes)
    
    for node_id in range(n_nodes):
        if cohesion_vector[node_id] > 0:
            silhouette_vector[node_id] = (cohesion_vector[node_id] - separation_vector[node_id]) / (1 - min([cohesion_vector[node_id], separation_vector[node_id]]))
        else:
            silhouette_vector[node_id] = 0
    return [silhouette_vector, closest_module_vector]