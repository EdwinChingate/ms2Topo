from __future__ import annotations
from best_merging4silhouette import *
from explore_overlapping import *
from modules_space_crafter import *

def silhouette_merging(CosineMat,
                       modules):
        
    module_1, modules_explored, overlapping_vector = explore_overlapping(modules = modules)
    
    if len(modules_explored) == len(modules):
        return modules
    
    modules_space = modules_space_crafter(module_1 = module_1,
                                          overlapping_vector = overlapping_vector,
                                          modules = modules)
    
    modules = best_merging4silhouette(CosineMat = CosineMat,
                                      modules_space = modules_space)
        
    modules = silhouette_merging(CosineMat = CosineMat,
                                 modules = modules) 
    
    return modules