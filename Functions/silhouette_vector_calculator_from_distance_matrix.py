from __future__ import annotations

import numpy as np
from cohesion_distance_vector_calculator import *
from separation_distance_vector_calculator import *

def silhouette_vector_calculator_from_distance_matrix(modules,
                                                       DistanceMat):
    """
    Calculate the standard distance-based silhouette vector.

    a(i) = mean distance to own module
    b(i) = mean distance to closest external module

    silhouette(i) = (b(i) - a(i)) / max(a(i), b(i))
    """

    if DistanceMat is None:
        raise ValueError("DistanceMat must be provided.")

    if DistanceMat.shape[0] != DistanceMat.shape[1]:
        raise ValueError("DistanceMat must be a square matrix.")

    n_nodes = DistanceMat.shape[0]

    if len(modules) <= 1:
        silhouette_vector = np.zeros(n_nodes)
        closest_module_vector = np.zeros(n_nodes).astype(int)

        return [silhouette_vector,
                closest_module_vector]

    cohesion_vector = cohesion_distance_vector_calculator(DistanceMat = DistanceMat,
                                                          modules = modules)

    separation_vector, closest_module_vector = separation_distance_vector_calculator(DistanceMat = DistanceMat,
                                                                                    modules = modules)

    silhouette_vector = np.zeros(n_nodes)

    for node_id in range(n_nodes):
        a = cohesion_vector[node_id]
        b = separation_vector[node_id]

        denominator = max(a,
                          b)

        if denominator > 0:
            silhouette_vector[node_id] = (b - a) / denominator
        else:
            silhouette_vector[node_id] = 0

    return [silhouette_vector,
            closest_module_vector]
