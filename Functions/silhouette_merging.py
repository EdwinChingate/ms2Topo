from __future__ import annotations
from best_merging4silhouette import *
from explore_overlapping import *
from merge_full_overlapping import *
from modules_space_crafter import *
import numpy as np

def silhouette_merging(CosineMat,
                       modules,
                       silhouette_vector = np.zeros(2)):
        
    module_1_id, modules_explored, overlapping_vector = explore_overlapping(modules = modules)
    
    if len(modules_explored) == len(modules):
        return [modules, silhouette_vector]
    
    modules_space = modules_space_crafter(module_1_id = module_1_id,
                                          overlapping_vector = overlapping_vector,
                                          modules = modules)
    if len(modules_space) == 1:
        modules = modules_space[0]
    else:
        modules, silhouette_vector = best_merging4silhouette(CosineMat = CosineMat,
                                                             modules_space = modules_space)
    
    modules, silhouette_vector = silhouette_merging(CosineMat = CosineMat,
                                                    modules = modules,
                                                    silhouette_vector = silhouette_vector) 
    
    return [modules, silhouette_vector]
