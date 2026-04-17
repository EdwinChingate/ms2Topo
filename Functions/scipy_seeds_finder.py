from __future__ import annotations
from modules_from_labels import *
import numpy as np

# TODO: unresolved names: connected_components, sparse

def scipy_seeds_finder(cosine_matrix,
                       seed_cosine_tolerance,
                       min_nodes = 3):

    adjacency_matrix = (cosine_matrix > seed_cosine_tolerance).astype(int)
    np.fill_diagonal(adjacency_matrix,
                     0)

    adjacency_matrix = np.maximum(adjacency_matrix,
                                  adjacency_matrix.T)

    adjacency_sparse = sparse.csr_matrix(adjacency_matrix)

    n_modules, labels = connected_components(csgraph = adjacency_sparse,
                                             directed = False,
                                             return_labels = True)

    modules = modules_from_labels(n_modules = n_modules,
                                  labels = labels,
                                  min_nodes = min_nodes)

    return np.array(modules)