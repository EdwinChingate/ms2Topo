from __future__ import annotations
from best_merging4silhouette import *
from explore_overlapping import *
from modules_space_crafter import *

def silhouette_merging(CosineMat,
                       modules,
                       current_silhouette = 0):
        
    module_1_id, modules_explored, overlapping_vector = explore_overlapping(modules = modules)
    
    if len(modules_explored) == len(modules):
        return [modules, current_silhouette]
    
    modules_space = modules_space_crafter(module_1_id = module_1_id,
                                          overlapping_vector = overlapping_vector,
                                          modules = modules)
    
    modules, current_silhouette = best_merging4silhouette(CosineMat = CosineMat,
                                                          modules_space = modules_space)
        
    modules, current_silhouette = silhouette_merging(CosineMat = CosineMat,
                                                     modules = modules,
                                                     current_silhouette = current_silhouette) 
    
    return [modules, current_silhouette]