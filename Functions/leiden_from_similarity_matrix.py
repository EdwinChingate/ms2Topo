from __future__ import annotations

import igraph as ig
import leidenalg as la
import numpy as np

def leiden_from_similarity_matrix(similarity_mat,
                                  feature_ids = None,
                                  min_similarity = 0.5,
                                  resolution_parameter = 0.3,
                                  n_iterations = -1):
    """
    Cluster features using Leiden over a sparsified Jaccard/Tanimoto similarity graph.
    """

    sim = np.asarray(similarity_mat, dtype=float).copy()

    # Remove self-loops explicitly
    np.fill_diagonal(sim, 0)

    # Keep only meaningful edges
    sim[sim < min_similarity] = 0

    sources, targets = np.where(np.triu(sim, k=1) > 0)
    weights = sim[sources, targets]

    g = ig.Graph()
    g.add_vertices(sim.shape[0])
    g.add_edges(list(zip(sources, targets)))
    g.es["weight"] = weights

    if feature_ids is not None:
        g.vs["feat_id"] = list(feature_ids)

    partition = la.find_partition(
        g,
        la.CPMVertexPartition,
        weights="weight",
        resolution_parameter=resolution_parameter,
        n_iterations=n_iterations
    )

    return g, partition
