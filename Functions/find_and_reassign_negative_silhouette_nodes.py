from __future__ import annotations
from modules_as_list_of_sets_from_modules_vector import *
import numpy as np
from silhouette_vector_calculator import *

def find_and_reassign_negative_silhouette_nodes(modules_vector,
                                                CosineMat):
    
    modules = modules_as_list_of_sets_from_modules_vector(modules_vector = modules_vector)
    silhouette_vector, closest_module_vector = silhouette_vector_calculator(CosineMat = CosineMat,
                                                                            modules = modules)    
    node2reassign = np.argmin(silhouette_vector)
    if silhouette_vector[node2reassign] >= 0:
        return modules
    
    modules_vector[node2reassign] = closest_module_vector[node2reassign]
    modules = find_and_reassign_negative_silhouette_nodes(modules_vector = modules_vector,
                                                          CosineMat = CosineMat)
    
    return modules