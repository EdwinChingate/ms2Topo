from __future__ import annotations
import numpy as np
from silhouette_vector_calculator import *

def binary_modules_merging(module_1_id,
                           module_2_id,
                           CosineMat,
                           modules):

    module_1 = modules[module_1_id]
    modules_ids_set = set(np.arange(len(modules)).tolist())
    non_overlap_loc = list(modules_ids_set - set([module_1_id, module_2_id]))
    module_2 = modules[module_2_id]
    the_other_modules = modules[non_overlap_loc].copy().tolist()   
    new_modules = np.array(the_other_modules + [module_1 | module_2])
    
    silhouette_vector, closest_module_vector = silhouette_vector_calculator(CosineMat = CosineMat,
                                                                            modules = new_modules) 
    
    return [new_modules, silhouette_vector, closest_module_vector]