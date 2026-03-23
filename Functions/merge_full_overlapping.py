from __future__ import annotations
import numpy as np
from overlapping_modules_vector_crafter import *

def merge_full_overlapping(modules):
    
    merged_modules = []
    modules_ids_set = set(np.arange(len(modules)).astype(int).tolist())
    
    while len(modules_ids_set) > 0:
        
        module_id = list(modules_ids_set)[0]
        module = modules[module_id]
        
        if len(module) == 1:
            modules_ids_set -= module
            merged_modules.append(module)
            continue
        
        overlapping_modules_table = overlapping_modules_vector_crafter(module_1 = module,
                                                                       modules = modules)
        
        full_overlapping_loc = np.where((overlapping_modules_table[:, 0] > 0) & (overlapping_modules_table[:, 1] == 0))[0].tolist()
        
        if len(full_overlapping_loc) > 1:
            merged_modules.append(set(full_overlapping_loc))
            modules_ids_set -= set(full_overlapping_loc)
        else:
            modules_ids_set -= set([module_id])
            merged_modules.append(module)
            
    return np.array(merged_modules)