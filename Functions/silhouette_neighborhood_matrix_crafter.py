from __future__ import annotations
from evaluate_module_neighborhood import *
import numpy as np

def silhouette_neighborhood_matrix_crafter(modules,
                                           CosineMat,
                                           closest_module_vector):
    
    n_modules = len(modules)
    silhouette_neighborhood_matrix = np.zeros((n_modules, n_modules))
    
    for module_1_id in range(n_modules):
        silhouette_neighborhood_matrix = evaluate_module_neighborhood(module_1_id = int(module_1_id),
                                                                      modules = modules,
                                                                      CosineMat = CosineMat,
                                                                      silhouette_neighborhood_matrix = silhouette_neighborhood_matrix,
                                                                      closest_module_vector = closest_module_vector)
        
    return silhouette_neighborhood_matrix