from __future__ import annotations

import numpy as np
import pandas as pd

def tanimoto_from_binary_matrix(binary_fragment_mat,
                                feature_cols):
    """
    Calculate an unweighted Tanimoto similarity matrix between features.

    Rows of binary_fragment_mat:
        aligned fragments

    Columns of binary_fragment_mat:
        features
    """

    # Tanimoto compares features, so transpose:
    # rows = features
    # cols = aligned fragments
    X = binary_fragment_mat.T

    intersection_mat = X @ X.T

    feature_sizes = X.sum(axis = 1)

    union_mat = (feature_sizes[:, None] +
                 feature_sizes[None, :] -
                 intersection_mat)

    tanimoto_mat = np.divide(intersection_mat,
                             union_mat,
                             out = np.zeros_like(intersection_mat,
                                                 dtype = float),
                             where = union_mat > 0)

    tanimoto_df = pd.DataFrame(tanimoto_mat,
                               index = feature_cols,
                               columns = feature_cols)

    return tanimoto_df
