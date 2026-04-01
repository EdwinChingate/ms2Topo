from __future__ import annotations
import numpy as np

def modules_vector2modules_list(modules,
                                silhouette_vector):
    n_nodes = len(silhouette_vector)
    modules_vector = np.zeros(n_nodes)
    module_id = 0
    
    for module in modules:
        modules_vector[list(module)] = module_id
        module_id += 1
    return modules_vector