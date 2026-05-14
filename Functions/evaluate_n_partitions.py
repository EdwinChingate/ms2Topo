from __future__ import annotations
import numpy as np
from silhouette_vector_calculator import *
from sklearn_spectral_modules_from_cosine_matrix import *

def evaluate_n_partitions(silhouette_evaluation_matrix,
                          cosine_matrix,
                          max_n_clusters,
                          iteration,
                          min_nodes = 1,
                          assign_labels = 'discretize',
                          random_state = 0):
    """
    Evaluate k = 1..max_n_clusters for a cosine matrix using mean silhouette.
    """

    n_nodes = cosine_matrix.shape[0]

    if n_nodes < 1:
        raise ValueError("cosine_matrix must contain at least one node.")

    max_n_clusters = min(int(max_n_clusters),
                         n_nodes)

    max_n_clusters = max(max_n_clusters,
                         1)

    modules_by_k = {}

    one_module_partition = np.array([set(range(n_nodes))],
                                    dtype = object)

    silhouette_vector, closest_module_vector = silhouette_vector_calculator(CosineMat = cosine_matrix,
                                                                            modules = one_module_partition)

    silhouette_evaluation_matrix[iteration, 0] = np.mean(silhouette_vector)
    modules_by_k[1] = one_module_partition

    for n_clusters in range(2, max_n_clusters + 1):
        modules = sklearn_spectral_modules_from_cosine_matrix(cosine_matrix = cosine_matrix,
                                                              n_clusters = n_clusters,
                                                              min_nodes = min_nodes,
                                                              assign_labels = assign_labels,
                                                              random_state = random_state)        

        silhouette_vector, closest_module_vector = silhouette_vector_calculator(modules = modules,
                                                                                CosineMat = cosine_matrix)

        silhouette_evaluation_matrix[iteration, n_clusters - 1] = np.mean(silhouette_vector)
        modules_by_k[n_clusters] = modules

    return [silhouette_evaluation_matrix,
            modules_by_k]