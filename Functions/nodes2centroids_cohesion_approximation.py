from __future__ import annotations

import numpy as np

def nodes2centroids_cohesion_approximation(nodes_modules_cosine_matrix):
    """
    Approximate cohesion as similarity to the best centroid/module.

    The best module value is then masked as -1 so the same matrix can be reused
    to estimate separation as similarity to the closest non-own centroid/module.
    """

    nodes_modules_cosine_matrix = np.array(nodes_modules_cosine_matrix,
                                           dtype = float).copy()

    n_spectra = nodes_modules_cosine_matrix.shape[0]
    cohesion_vector = np.zeros(n_spectra)

    for spectrum_local_id in range(n_spectra):
        best_module_id = int(np.argmax(nodes_modules_cosine_matrix[spectrum_local_id, :]))
        cohesion_vector[spectrum_local_id] = nodes_modules_cosine_matrix[spectrum_local_id, best_module_id]
        nodes_modules_cosine_matrix[spectrum_local_id, best_module_id] = -1

    return [cohesion_vector, nodes_modules_cosine_matrix]