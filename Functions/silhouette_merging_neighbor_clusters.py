from __future__ import annotations
from binary_modules_merging import *
import numpy as np
from silhouette_neighborhood_matrix_crafter import *

def silhouette_merging_neighbor_clusters(modules,
                                         silhouette_vector,
                                         CosineMat,
                                         closest_module_vector):
        
    silhouette = np.mean(silhouette_vector)
    #print(modules)
    #print(silhouette)
    silhouette_neighborhood_matrix = silhouette_neighborhood_matrix_crafter(modules = modules,
                                                                            CosineMat = CosineMat,
                                                                            closest_module_vector = closest_module_vector)    
    max_silhouette = np.max(silhouette_neighborhood_matrix)
    
    if max_silhouette <= silhouette:
        return [modules, silhouette_vector, closest_module_vector]
    
    module_1_id_candidates, module_2_id_candidates = np.where(silhouette_neighborhood_matrix == max_silhouette)
    
    modules, silhouette_vector, closest_module_vector = binary_modules_merging(module_1_id = module_1_id_candidates[0],
                                                                               module_2_id = module_2_id_candidates[0],
                                                                               CosineMat = CosineMat,
                                                                               modules = modules)  
    
    modules, silhouette_vector, closest_module_vector = silhouette_merging_neighbor_clusters(modules = modules,
                                                                                             silhouette_vector = silhouette_vector,
                                                                                             CosineMat = CosineMat,
                                                                                             closest_module_vector = closest_module_vector)
    return [modules, silhouette_vector, closest_module_vector]