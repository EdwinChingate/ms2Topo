from __future__ import annotations
import numpy as np

def merging_combinations_mudules_space(modules,
                                       modules_space = None):
    
    if modules_space == None:
        modules_space = []
        
    n_modules = len(modules)
    modules_ids_set = set(range(n_modules))
    
    for module_1_id in range(n_modules):
        module_1 = modules[module_1_id]
        for module_2_id in range(module_1_id + 1, n_modules):
            module_2 = modules[module_2_id]
            non_overlap_loc = list(modules_ids_set - set([module_1_id, module_2_id]))
            the_other_modules = modules[non_overlap_loc].copy().tolist()
            alternative_modules = np.array(the_other_modules + [module_1 | module_2])
            modules_space.append(alternative_modules)
            modules_space = merging_combinations_mudules_space(modules = alternative_modules,
                                                               modules_space = modules_space)
    
    return modules_space