from __future__ import annotations
import numpy as np
from silhouette_vector_calculator import *

def silhouette_from_modules_vector(CosineMat,
                                          modules_vector):
    modules = []
    modules_ids = modules_ids = np.unique(modules_vector.astype(int))
    
    for module_id in modules_ids:
        module = set(np.where(modules_vector == module_id)[0].astype(int).tolist())
        modules.append(module)
        
    silhouette_vector, closest_module_vector = silhouette_vector_calculator(CosineMat = CosineMat,
                                                                            modules = modules) 
    return np.mean(silhouette_vector)