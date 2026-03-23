from __future__ import annotations
import numpy as np

def overlapping_modules_vector_crafter(module_1,
                                       modules):
    return np.array([[len(set(module_1) & set(module_2)), len(set(module_1) ^ set(module_2)), set(module_1) & set(module_2), set(module_1) ^ set(module_2)] for module_2 in modules])
