from __future__ import annotations
import numpy as np

def modules_vector_from_modules_list(modules,
                                     silhouette_vector = None):
    n_nodes = np.max(np.array([[np.max(list(module))] for module in modules])).astype(int) + 1
    modules_vector = -1 * np.ones(n_nodes)
    module_id = 0

    for module in modules:
        modules_vector[list(module)] = module_id
        module_id += 1
    return modules_vector


# In[6]: