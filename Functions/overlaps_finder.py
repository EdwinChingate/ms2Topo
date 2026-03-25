from __future__ import annotations
import numpy as np

def overlaps_finder(module_1,
                    modules):
    
    overlapping_vector = np.array([len(module_1 & module_2) for module_2 in modules])
    overlapping_vector_binary = overlapping_vector.copy()
    overlapping_vector_binary[overlapping_vector_binary > 0] = 1
    
    return [overlapping_vector, overlapping_vector_binary]
