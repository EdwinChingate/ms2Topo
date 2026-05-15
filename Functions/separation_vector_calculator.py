from __future__ import annotations

from nodes_modules_cosine_similarity import nodes_modules_cosine_similarity
import numpy as np

def separation_vector_calculator(CosineMat,
                                 modules,
                                 aproximate_mean_with_centroid = False,
                                 nodes_modules_cosine_matrix = None):
    """
    Estimate each node's similarity to the closest external module.

    If aproximate_mean_with_centroid is False, separation is computed from the
    full cosine matrix. If True, nodes_modules_cosine_matrix is assumed to
    already contain node-to-centroid or node-to-module similarities.
    """

    if aproximate_mean_with_centroid:
        if nodes_modules_cosine_matrix is None:
            raise ValueError("nodes_modules_cosine_matrix is required when aproximate_mean_with_centroid=True.")

        n_nodes = nodes_modules_cosine_matrix.shape[0]
    else:
        if CosineMat is None:
            raise ValueError("CosineMat is required when aproximate_mean_with_centroid=False.")

        nodes_modules_cosine_matrix, n_nodes = nodes_modules_cosine_similarity(CosineMat = CosineMat,
                                                                               modules = modules)

    separation_vector = np.zeros(n_nodes)
    closest_module_vector = np.zeros(n_nodes).astype(int)

    for node_id in range(n_nodes):
        closest_module2node_id = int(np.argmax(nodes_modules_cosine_matrix[node_id, :]))
        closest_module_vector[node_id] = closest_module2node_id

        if aproximate_mean_with_centroid:
            separation_vector[node_id] = nodes_modules_cosine_matrix[node_id, closest_module2node_id]
        else:
            module = modules[closest_module2node_id]
            separation_vector[node_id] = np.mean(CosineMat[node_id, list(module)])

    return [separation_vector, closest_module_vector]