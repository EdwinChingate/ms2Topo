from __future__ import annotations
import numpy as np

def nodes_modules_cosine_similarity(CosineMat,
                                    modules):
    
    n_nodes = len(CosineMat)
    n_modules = len(modules)
    nodes_modules_cosine_matrix = np.zeros((n_nodes, n_modules))
    
    for node_id in range(n_nodes):
        for module_id in range(n_modules):
            module = modules[module_id]
            if int(node_id) in module:
                nodes_modules_cosine_matrix[node_id, module_id] = -1
            else:
                nodes_modules_cosine_matrix[node_id, module_id] = np.mean(CosineMat[node_id, list(module)])
    
    return [nodes_modules_cosine_matrix, n_nodes]