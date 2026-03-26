from __future__ import annotations
from silhouette_vector_calculator import *

def modules_merging_evaluation(module_1_id,
                               module_2_id,
                               modules,
                               CosineMat,
                               silhouette_vector):
    
    silhouette = np.mean(silhouette_vector)
    module_1 = modules[module_1_id]
    modules_ids_set = set(np.arange(len(modules)).tolist())
    non_overlap_loc = list(modules_ids_set - set([module_1_id, module_2_id]))
    module_2 = modules[module_2_id]
    the_other_modules = modules[non_overlap_loc].copy().tolist()   
    new_modules = np.array(the_other_modules + [module_1 | module_2])
    
    new_silhouette_vector = silhouette_vector_calculator(CosineMat = CosineMat,
                                                         modules = new_modules)  
    new_silhouette = np.mean(new_silhouette_vector)

    if new_silhouette > silhouette:
        return [new_modules, new_silhouette_vector, True]
    
    return [modules, silhouette_vector, False]