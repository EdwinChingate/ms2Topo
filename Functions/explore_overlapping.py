from __future__ import annotations
from overlaps_finder import *

def explore_overlapping(modules):
    
    modules_explored = []
    n_modules = len(modules) 
    
    for module_1 in modules:
        overlapping_vector, overlapping_vector_binary = overlaps_finder(module_1 = module_1,
                                                                        modules = modules)        
        
        if sum(overlapping_vector_binary) == 1:
            modules_explored.append(module_1)
        else:
            break 
            
    return [module_1, modules_explored, overlapping_vector]