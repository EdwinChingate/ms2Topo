from __future__ import annotations
import numpy as np
from overlapping_modules_vector_crafter import *
from remove_contained_modules import *

def merge_full_overlapping(modules):
    
    modules_size_vector = np.array([len(module) for module in modules])
    sorted_size_indices = np.argsort(-modules_size_vector)
    merged_modules = []
    
    while len(sorted_size_indices) > 0:    
        module_1_id = sorted_size_indices[0]
        module_1 = modules[module_1_id]
        overlapping_modules_table = overlapping_modules_vector_crafter(module_1 = module_1,
                                                                       modules = modules)
        full_overlapping_loc = np.where(overlapping_modules_table[:, 0] | overlapping_modules_table[:, 1])[0].tolist()
        merged_modules.append(module_1)
        sorted_size_indices = remove_contained_modules(sorted_size_indices = sorted_size_indices,
                                                       full_overlapping_loc = full_overlapping_loc)

    return np.array(merged_modules)
