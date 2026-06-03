from __future__ import annotations

import numpy as np
from distance_values_from_matrix import *

def cohesion_distance_vector_calculator(DistanceMat,
                                         modules):
    """
    Calculate a(i): mean distance from each node to its own module.

    Singleton modules receive cohesion distance = 0.
    """

    n_nodes = DistanceMat.shape[0]
    cohesion_vector = np.zeros(n_nodes)

    for module in modules:
        module = [int(node) for node in module]

        for node_id in module:
            if len(module) <= 1:
                cohesion_vector[node_id] = 0
                continue

            other_nodes = [node for node in module
                           if node != node_id]

            distances = distance_values_from_matrix(DistanceMat = DistanceMat,
                                                    node_id = node_id,
                                                    target_nodes = other_nodes)

            cohesion_vector[node_id] = np.mean(distances)

    return cohesion_vector
