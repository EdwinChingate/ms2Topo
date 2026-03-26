from __future__ import annotations
from modules_merging_evaluation import *

def similarity_overlaps_finder(module_1_id,
                               modules,
                               silhouette_vector,
                               IntramoduleSimilarity,
                               CompactCosineTen,
                               CosineMat,
                               cos_tol):
    
    lonely_module = True
    LowIntramoduleSimmilarity = IntramoduleSimilarity[module_1_id, 1].copy()
    
    if LowIntramoduleSimmilarity > cos_tol:
        LowIntramoduleSimmilarity = cos_tol
        
    for module_2_id in range(len(modules)):        
        if module_2_id == module_1_id:
            continue
            
        two_modules_similarity = CompactCosineTen[module_1_id, module_2_id, 2]
        
        if two_modules_similarity > LowIntramoduleSimmilarity:
            modules, silhouette_vector, merged = modules_merging_evaluation(module_1_id = module_1_id,
                                                                            module_2_id = module_2_id,
                                                                            modules = modules,
                                                                            CosineMat = CosineMat,
                                                                            silhouette_vector = silhouette_vector)                      
            if merged:
                lonely_module = False  
                break

    return [modules, silhouette_vector, lonely_module] 