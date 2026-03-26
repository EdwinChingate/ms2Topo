from __future__ import annotations
from similarity_overlaps_finder import *

def explore_similarity_overlapping(modules,
                                   silhouette_vector,
                                   IntramoduleSimilarity,
                                   CompactCosineTen,
                                   CosineMat,
                                   cos_tol):
    
    modules_explored_count = 0
    n_modules = len(modules) 
    
    for module_1_id in range(len(modules)):
        
        module_1 = modules[module_1_id]        
        modules, silhouette_vector, lonely_module = similarity_overlaps_finder(module_1_id = module_1_id,
                                                                               modules = modules,
                                                                               silhouette_vector = silhouette_vector,
                                                                               IntramoduleSimilarity = IntramoduleSimilarity,
                                                                               CompactCosineTen = CompactCosineTen,
                                                                               CosineMat = CosineMat,
                                                                               cos_tol = cos_tol)           
        
        if lonely_module:
            modules_explored_count += 1
        else:
            break 
            
    return [modules, silhouette_vector, modules_explored_count]