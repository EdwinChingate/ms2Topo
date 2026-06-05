from __future__ import annotations

from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix
from column_to_array import *

def neutral_loss_centroids_to_index(neutral_loss_gmm_peaks,
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
    Convert neutral-loss GMM peaks into sorted NumPy arrays.

    neutral_loss_gmm_peaks can be:
        DataFrame, 2D ndarray, 1D vector of centroid m/z values.
    """

    centroid_mz = column_to_array(neutral_loss_gmm_peaks,
                                   centroid_mz_col,
                                   dtype = float)

    centroid_sigma = column_to_array(neutral_loss_gmm_peaks,
                                      centroid_std_col,
                                      default = sigma_floor,
                                      dtype = float)

    centroid_count = column_to_array(neutral_loss_gmm_peaks,
                                      centroid_count_col,
                                      default = 1.0,
                                      dtype = float)

    good_centroids = (np.isfinite(centroid_mz) &
                      np.isfinite(centroid_sigma) &
                      np.isfinite(centroid_count))

    centroid_mz = centroid_mz[good_centroids]
    centroid_sigma = centroid_sigma[good_centroids]
    centroid_count = centroid_count[good_centroids]

    centroid_sigma = np.maximum(centroid_sigma,
                                sigma_floor)

    if centroid_min_mz_col is not None and centroid_max_mz_col is not None:
        raw_min_mz = column_to_array(neutral_loss_gmm_peaks,
                                      centroid_min_mz_col,
                                      default = np.nan,
                                      dtype = float)[good_centroids]

        raw_max_mz = column_to_array(neutral_loss_gmm_peaks,
                                      centroid_max_mz_col,
                                      default = np.nan,
                                      dtype = float)[good_centroids]

        centroid_edge = np.maximum(np.abs(centroid_mz - raw_min_mz),
                                   np.abs(raw_max_mz - centroid_mz))

        bad_edge = (~np.isfinite(centroid_edge)) | (centroid_edge <= 0)

    else:
        centroid_edge = np.minimum(std_distance * centroid_sigma,
                                   ppm_tol / 1e6 * centroid_mz)

        bad_edge = (~np.isfinite(centroid_edge)) | (centroid_edge <= 0)

    fallback_edge = np.minimum(std_distance * centroid_sigma,
                               ppm_tol / 1e6 * centroid_mz)

    centroid_edge[bad_edge] = fallback_edge[bad_edge]

    if max_abs_tol is not None:
        centroid_edge = np.minimum(centroid_edge,
                                   max_abs_tol)

    centroid_prior = np.power(np.maximum(centroid_count, 1.0),
                              prior_power)

    centroid_order = np.argsort(centroid_mz)

    return {"centroid_mz": centroid_mz[centroid_order],
            "centroid_sigma": centroid_sigma[centroid_order],
            "centroid_edge": centroid_edge[centroid_order],
            "centroid_count": centroid_count[centroid_order],
            "centroid_prior": centroid_prior[centroid_order],
            "centroid_original_id": np.where(good_centroids)[0][centroid_order]}
