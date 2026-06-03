from __future__ import annotations

import numpy as np
import pandas as pd

def tanimoto_matrix_from_binary_features(binary_features_df,
                                         force_diagonal_one = True):
    """
    Calculate feature-by-feature Tanimoto similarity from a binary annotation
    matrix.

    Input:
        rows    -> annotation IDs
        columns -> feat_id
        values  -> 0/1 or numeric values convertible to presence/absence
    """

    feature_ids = list(binary_features_df.columns)

    X = binary_features_df.copy()
    X = X.apply(pd.to_numeric, errors = "coerce").fillna(0)
    X = (X > 0).astype(int)

    X = X.T.values.astype(int)

    intersection = X @ X.T

    row_sums = X.sum(axis = 1)

    union = row_sums[:, None] + row_sums[None, :] - intersection

    tanimoto_mat = np.divide(intersection,
                             union,
                             out = np.zeros_like(intersection, dtype = float),
                             where = union != 0)

    if force_diagonal_one:
        non_empty_features = row_sums > 0
        diag_loc = np.arange(len(feature_ids))

        tanimoto_mat[diag_loc[non_empty_features],
                     diag_loc[non_empty_features]] = 1.0

    tanimoto_df = pd.DataFrame(tanimoto_mat,
                               index = feature_ids,
                               columns = feature_ids)

    return tanimoto_df
