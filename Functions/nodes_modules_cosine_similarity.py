from __future__ import annotations

import numpy as np

def nodes_modules_cosine_similarity(CosineMat,
                                    modules):
    """
    Compute the mean cosine similarity between every node and every module.

    The similarity between a node and its own module is marked as -1 so this
    matrix can be used directly for nearest-other-module separation.
    """

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