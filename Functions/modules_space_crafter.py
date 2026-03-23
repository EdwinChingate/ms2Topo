from __future__ import annotations
import numpy as np

def modules_space_crafter(module_1,
                          overlapping_vector,
                          modules):
    
    modules_space = []
    overlap_loc = np.where((overlapping_vector > 0) & (overlapping_vector < len(module_1)))[0][0].item()
    non_overlap_loc = np.where(overlapping_vector == 0)[0]
    module_2 = modules[overlap_loc]
    the_other_modules = modules[non_overlap_loc].copy().tolist()
    
    module_a = module_1 - module_2
    module_b = module_2 - module_1
    module_c = module_1 | module_2
    
    modules_space_branch_list = [[module_a, module_2], [module_1, module_b], [module_c]]
    
    for modules_space_branch in modules_space_branch_list:
        module = np.array(the_other_modules + modules_space_branch)
        modules_space.append(module)
    
    return modules_space