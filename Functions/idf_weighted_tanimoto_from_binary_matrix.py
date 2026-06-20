from __future__ import annotations

import numpy as np
import pandas as pd

def idf_weighted_tanimoto_from_binary_matrix(binary_fragment_mat,
                                             IDF,
                                             feature_cols):
    """
    Calculate an IDF-weighted Tanimoto similarity matrix between features.

    Rows of binary_fragment_mat:
        aligned fragments

    Columns of binary_fragment_mat:
        features

    IDF:
        fragment-level weights, one value per aligned fragment.
    """

    # Tanimoto compares features, so transpose:
    # rows = features
    # cols = aligned fragments
    X = binary_fragment_mat.T

    weighted_X = X * IDF[None, :]

    weighted_intersection_mat = weighted_X @ X.T

    weighted_feature_sizes = np.sum(weighted_X,
                                    axis = 1)

    weighted_union_mat = (weighted_feature_sizes[:, None] +
                          weighted_feature_sizes[None, :] -
                          weighted_intersection_mat)

    weighted_tanimoto_mat = np.divide(weighted_intersection_mat,
                                      weighted_union_mat,
                                      out = np.zeros_like(weighted_intersection_mat,
                                                          dtype = float),
                                      where = weighted_union_mat > 0)

    weighted_tanimoto_df = pd.DataFrame(weighted_tanimoto_mat,
                                        index = feature_cols,
                                        columns = feature_cols)

    return weighted_tanimoto_df
