from __future__ import annotations
import numpy as np

def overlapping_modules_vector_crafter(module_1,
                                       modules):
    return np.array([[module_1.issubset(module_2), module_2.issubset(module_1)] for module_2 in modules])
