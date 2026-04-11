from __future__ import annotations
import numpy as np
from silhouette_vector_calculator import *

def merging_combinations_mudules_space(modules,
                                       CosineMat,
                                       silhouette_vector,
                                       silhouette):

    sharpest_modules = modules.copy()
    n_modules = len(modules)
    modules_ids_set = set(range(n_modules))

    for module_1_id in range(n_modules):
        module_1 = modules[module_1_id]
        for module_2_id in range(module_1_id + 1, n_modules):

            module_2 = modules[module_2_id]

            non_overlap_loc = list(modules_ids_set - set([module_1_id, module_2_id]))
            the_other_modules = modules[non_overlap_loc].copy().tolist()
            alternative_modules = np.array(the_other_modules + [module_1 | module_2])


            alternative_silhouette_vector, alternative_closest_module_vector = silhouette_vector_calculator(CosineMat = CosineMat,
                                                                                                            modules = alternative_modules)

            alternative_silhouette = np.mean(alternative_silhouette_vector)
            alternative_modules, alternative_silhouette_vector, alternative_silhouette = merging_combinations_mudules_space(modules = alternative_modules,            
                                                                                                                                                               silhouette_vector = alternative_silhouette_vector,
                                                                                                                                                               CosineMat = CosineMat,
                                                                                                                                                               silhouette = alternative_silhouette)            

            if alternative_silhouette > silhouette:
                sharpest_modules = alternative_modules
                silhouette_vector = alternative_silhouette_vector
                #closest_module_vector = alternative_closest_module_vector
                silhouette = alternative_silhouette

    return [modules, silhouette_vector, silhouette]


# In[5]: