from __future__ import annotations
from cohesion_vector_calculator import *
import numpy as np
from separation_vector_calculator import *

def silhouette_vector_calculator(CosineMat,
                                 modules):
    
    n_nodes = len(CosineMat)
    
    cohesion_vector = cohesion_vector_calculator(CosineMat = CosineMat,
                                                 modules = modules)
    separation_vector = separation_vector_calculator(CosineMat = CosineMat,
                                                     modules = modules)  
    silhouette_vector = np.zeros(n_nodes)
    
    for node_id in range(n_nodes):
        silhouette_vector[node_id] = (cohesion_vector[node_id] - separation_vector[node_id]) / (1 - min([cohesion_vector[node_id], separation_vector[node_id]]))
      
    return silhouette_vector