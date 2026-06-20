from __future__ import annotations

import numpy as np
import pandas as pd

def feature_weighted_mean_fragment_idf(aligned_intensity_df,
                                       feature_cols,
                                       IDF):
    """
    Calculate the intensity-weighted mean fragment IDF for each feature.

    Rows of aligned_intensity_df:
        aligned fragments

    Columns:
        features

    IDF:
        fragment-level IDF values, one value per aligned fragment.

    The intensity values of each feature are normalized to sum to one before
    weighting the fragment IDF values.
    """

    intensity_mat = aligned_intensity_df[feature_cols].apply(pd.to_numeric,
                                                             errors = "coerce").fillna(0)

    intensity_mat = intensity_mat.to_numpy(dtype = float)

    intensity_mat[intensity_mat < 0] = 0

    feature_intensity_sums = np.sum(intensity_mat,
                                    axis = 0)

    normalized_intensity_mat = np.divide(intensity_mat,
                                         feature_intensity_sums[None, :],
                                         out = np.zeros_like(intensity_mat,
                                                             dtype = float),
                                         where = feature_intensity_sums[None, :] > 0)

    weighted_mean_IDF = np.sum(normalized_intensity_mat * IDF[:, None],
                               axis = 0)

    feature_idf_df = pd.DataFrame({"feat_id": feature_cols,
                                   "weighted_mean_fragment_IDF": weighted_mean_IDF,
                                   "total_fragment_intensity": feature_intensity_sums})

    return feature_idf_df
