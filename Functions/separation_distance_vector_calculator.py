from __future__ import annotations

import numpy as np
from distance_values_from_matrix import *

def separation_distance_vector_calculator(DistanceMat,
                                          modules):
    """
    Calculate b(i): mean distance from each node to the closest external module.
    """

    n_nodes = DistanceMat.shape[0]

    separation_vector = np.zeros(n_nodes)
    closest_module_vector = np.zeros(n_nodes).astype(int)

    node_module_vector = np.full(n_nodes,
                                 -1,
                                 dtype = int)

    for module_id, module in enumerate(modules):
        for node_id in module:
            node_module_vector[int(node_id)] = int(module_id)

    for node_id in range(n_nodes):
        own_module_id = node_module_vector[node_id]

        closest_distance = np.inf
        closest_module_id = -1

        for module_id, module in enumerate(modules):
            if module_id == own_module_id:
                continue

            module = [int(node) for node in module]

            if len(module) == 0:
                continue

            distances = distance_values_from_matrix(DistanceMat = DistanceMat,
                                                    node_id = node_id,
                                                    target_nodes = module)

            mean_distance = np.mean(distances)

            if mean_distance < closest_distance:
                closest_distance = mean_distance
                closest_module_id = module_id

        if np.isfinite(closest_distance):
            separation_vector[node_id] = closest_distance
            closest_module_vector[node_id] = closest_module_id
        else:
            separation_vector[node_id] = 0
            closest_module_vector[node_id] = own_module_id

    return [separation_vector,
            closest_module_vector]
