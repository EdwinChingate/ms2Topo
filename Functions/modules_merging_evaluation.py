from __future__ import annotations
import numpy as np
from silhouette_vector_calculator import *

def modules_merging_evaluation(module_1_id,
                               module_2_id,
                               modules,
                               CosineMat,
                               current_silhouette):
    
    module_1 = modules[module_1_id]
    modules_ids_set = set(np.arange(len(modules)).tolist())
    non_overlap_loc = list(modules_ids_set - set([module_1_id, module_2_id]))
    module_2 = modules[module_2_id]
    the_other_modules = modules[non_overlap_loc].copy().tolist()   
    new_modules = np.array(the_other_modules + [module_1 | module_2])
    
    silhouette_vector = silhouette_vector_calculator(CosineMat = CosineMat,
                                                     modules = new_modules)  
    silhouette = np.mean(silhouette_vector)

    if silhouette > current_silhouette:
        return [new_modules, silhouette, True]
    
    return [modules, current_silhouette, False]
