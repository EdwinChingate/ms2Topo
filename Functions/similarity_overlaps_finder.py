from __future__ import annotations
from modules_merging_evaluation import *

def similarity_overlaps_finder(module_1_id,
                               modules,
                               current_silhouette,
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
            modules, current_silhouette, merged = modules_merging_evaluation(module_1_id = module_1_id,
                                                                             module_2_id = module_2_id,
                                                                             modules = modules,
                                                                             CosineMat = CosineMat,
                                                                             current_silhouette = current_silhouette)                      
            if merged:
                lonely_module = False  
                break

    return [modules, current_silhouette, lonely_module] 