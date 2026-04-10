from __future__ import annotations
import numpy as np

def modules_from_labels(n_modules,
                        labels,
                        min_nodes = 3):
    modules = []

    for module_id in range(n_modules):
        module = set(np.where(labels == module_id)[0].tolist())
        if len(module) >= min_nodes:
            modules.append(module)

    return modules