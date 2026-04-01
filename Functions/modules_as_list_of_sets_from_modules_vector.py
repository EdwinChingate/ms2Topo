from __future__ import annotations
import numpy as np

def modules_as_list_of_sets_from_modules_vector(modules_vector):
    
    modules_ids = list(set(modules_vector.tolist()))
    modules = []
    
    for module_id in modules_ids:
        module = set(np.where(modules_vector == module_id)[0].tolist())
        modules.append(module)
        
    return np.array(modules)