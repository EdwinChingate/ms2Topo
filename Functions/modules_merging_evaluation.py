from __future__ import annotations
from binary_modules_merging import *
import numpy as np

def modules_merging_evaluation(module_1_id,
                               module_2_id,
                               modules,
                               CosineMat,
                               silhouette_vector):
    
    silhouette = np.mean(silhouette_vector)
    
    new_modules, new_silhouette_vector, closest_module_vector = binary_modules_merging(module_1_id = module_1_id,
                                                                                       module_2_id = module_2_id,
                                                                                       CosineMat = CosineMat,
                                                                                       modules = modules)
    
    new_silhouette = np.mean(new_silhouette_vector)

    if new_silhouette > silhouette:
        return [new_modules, new_silhouette_vector, True]
    
    return [modules, silhouette_vector, False]