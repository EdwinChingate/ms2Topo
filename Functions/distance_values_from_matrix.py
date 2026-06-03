from __future__ import annotations

import numpy as np
from scipy import sparse

def distance_values_from_matrix(DistanceMat,
                                node_id,
                                target_nodes):

    target_nodes = list(target_nodes)

    if sparse.issparse(DistanceMat):
        values = DistanceMat[node_id, target_nodes].toarray().flatten()
    else:
        values = DistanceMat[node_id, target_nodes]

    return np.asarray(values,
                      dtype = float)
