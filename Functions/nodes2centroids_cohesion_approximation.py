from __future__ import annotations
import numpy as np

def nodes2centroids_cohesion_approximation(nodes_modules_cosine_matrix):

    n_spectra = nodes_modules_cosine_matrix.shape[0]
    cohesion_vector = np.zeros(n_spectra)

    for spectrum_local_id in range(n_spectra):
        best_module_id = int(np.argmax(nodes_modules_cosine_matrix[spectrum_local_id, :]))
        cohesion_vector[spectrum_local_id] = nodes_modules_cosine_matrix[spectrum_local_id, best_module_id]
        nodes_modules_cosine_matrix[spectrum_local_id, best_module_id] = -1

    return [cohesion_vector, nodes_modules_cosine_matrix]


# In[244]: