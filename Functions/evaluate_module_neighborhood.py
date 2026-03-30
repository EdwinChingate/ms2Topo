from __future__ import annotations
from binary_modules_merging import *
import numpy as np

def evaluate_module_neighborhood(module_1_id,
                                 modules,
                                 CosineMat,
                                 silhouette_neighborhood_matrix,
                                 closest_module_vector):
    
    module = modules[module_1_id]
    neighbors = closest_module_vector[list(module)].astype(int)
    
    for module_2_id in neighbors:    
        #print(module_1_id, module_2_id)
        new_modules, silhouette_vector, closest_module_vector = binary_modules_merging(module_1_id = module_1_id,
                                                                                       module_2_id = module_2_id,
                                                                                       CosineMat = CosineMat,
                                                                                       modules = modules)    
        silhouette_neighborhood_matrix[module_1_id, module_2_id] = np.mean(silhouette_vector)
    
    return silhouette_neighborhood_matrix