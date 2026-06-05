from __future__ import annotations

from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix
from column_to_array import *

def clustered_fragments_to_centroid_index(clustered_fragments_df,
                                          centroid_mz_col = "6",
                                          centroid_std_col = "7",
                                          centroid_count_col = "1",
                                          centroid_min_mz_col = None,
                                          centroid_max_mz_col = None,
                                          std_distance = 3,
                                          ppm_tol = 20,
                                          max_abs_tol = 0.01,
                                          sigma_floor = 2e-4,
                                          prior_power = 0.5):
    """
    Convert a clustered-fragments table into sorted NumPy arrays for fast
    assignment.

    clustered_fragments_df can be a pandas DataFrame or a NumPy array.

    The default GMM columns follow the table you generated:
        column "6" or 6 = Gaussian m/z centroid
        column "7" or 7 = Gaussian standard deviation-like width
        column "1" or 1 = support/count-like value

    If centroid_min_mz_col and centroid_max_mz_col are provided, those limits
    are used as the assignment window. Otherwise, windows are rebuilt as:
        edge = min(std_distance * sigma, ppm_tol / 1e6 * mz)
    and optionally capped by max_abs_tol.
    """

    centroid_mz = column_to_array(table = clustered_fragments_df,
                                  col = centroid_mz_col,
                                  dtype = float)

    centroid_sigma = column_to_array(table = clustered_fragments_df,
                                     col = centroid_std_col,
                                     default = sigma_floor,
                                     dtype = float)

    centroid_count = column_to_array(table = clustered_fragments_df,
                                     col = centroid_count_col,
                                     default = 1.0,
                                     dtype = float)

    good_centroids = (np.isfinite(centroid_mz) &
                      np.isfinite(centroid_sigma) &
                      np.isfinite(centroid_count))

    centroid_original_id = np.where(good_centroids)[0]
    centroid_mz = centroid_mz[good_centroids]
    centroid_sigma = centroid_sigma[good_centroids]
    centroid_count = centroid_count[good_centroids]

    centroid_sigma = np.maximum(centroid_sigma,
                                sigma_floor)

    if centroid_min_mz_col is not None and centroid_max_mz_col is not None:
        centroid_min_mz_all = column_to_array(table = clustered_fragments_df,
                                              col = centroid_min_mz_col,
                                              default = np.nan,
                                              dtype = float)

        centroid_max_mz_all = column_to_array(table = clustered_fragments_df,
                                              col = centroid_max_mz_col,
                                              default = np.nan,
                                              dtype = float)

        centroid_min_mz = centroid_min_mz_all[good_centroids]
        centroid_max_mz = centroid_max_mz_all[good_centroids]

        centroid_edge = np.maximum(np.abs(centroid_mz - centroid_min_mz),
                                   np.abs(centroid_max_mz - centroid_mz))

        bad_edge = (~np.isfinite(centroid_edge)) | (centroid_edge <= 0)

        if np.any(bad_edge):
            fallback_edge = np.minimum(std_distance * centroid_sigma,
                                       ppm_tol / 1e6 * centroid_mz)

            if max_abs_tol is not None:
                fallback_edge = np.minimum(fallback_edge,
                                           max_abs_tol)

            centroid_edge[bad_edge] = fallback_edge[bad_edge]

    else:
        centroid_edge = np.minimum(std_distance * centroid_sigma,
                                   ppm_tol / 1e6 * centroid_mz)

        if max_abs_tol is not None:
            centroid_edge = np.minimum(centroid_edge,
                                       max_abs_tol)

    centroid_prior = np.power(np.maximum(centroid_count, 1.0),
                              prior_power)

    centroid_order = np.argsort(centroid_mz)

    centroid_index = {"centroid_mz": centroid_mz[centroid_order],
                      "centroid_sigma": centroid_sigma[centroid_order],
                      "centroid_edge": centroid_edge[centroid_order],
                      "centroid_count": centroid_count[centroid_order],
                      "centroid_prior": centroid_prior[centroid_order],
                      "centroid_original_id": centroid_original_id[centroid_order]}

    return centroid_index
