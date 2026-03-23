from __future__ import annotations
import numpy as np
def modules_space_crafter(module_1_id,
                          overlapping_vector,
                          modules):
    
    modules_space = []
    module_1 = modules[module_1_id]
    modules_ids_set = set(np.arange(len(modules)).tolist())
    module_2_id = np.where((overlapping_vector > 0) & (overlapping_vector < len(module_1)))[0][0].item()
    non_overlap_loc = list(modules_ids_set - set([module_1_id, module_2_id]))
    module_2 = modules[module_2_id]
    the_other_modules = modules[non_overlap_loc].copy().tolist()
    
    module_a = module_1 - module_2
    module_b = module_2 - module_1
    module_c = module_1 | module_2
    
    modules_space_branch_list = [[module_a, module_2], [module_1, module_b], [module_c]]
    
    for modules_space_branch in modules_space_branch_list:
        modules = np.array(the_other_modules + modules_space_branch)
        modules_space.append(modules)
    
    return modules_space
