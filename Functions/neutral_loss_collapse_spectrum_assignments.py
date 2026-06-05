from __future__ import annotations

from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix

def neutral_loss_collapse_spectrum_assignments(assigned_centroid_row,
                                  observed_mz_vec,
                                  intensity_vec,
                                  status_vec = None,
                                  confident_only = False,
                                  aggregation = "max"):
    """
    Collapse neutral-loss assignments from one spectrum into one value per
    centroid.

    aggregation:
        'max' -> use the strongest neutral loss assigned to a centroid
        'sum' -> sum intensities and report intensity-weighted mean m/z
    """

    assigned_centroid_row = np.asarray(assigned_centroid_row,
                                       dtype = np.int64)

    observed_mz_vec = np.asarray(observed_mz_vec,
                                 dtype = float)

    intensity_vec = np.asarray(intensity_vec,
                               dtype = float)

    keep_filter = assigned_centroid_row >= 0

    if status_vec is not None and confident_only:
        keep_filter = keep_filter & (status_vec == 2)

    keep_filter = (keep_filter &
                   np.isfinite(observed_mz_vec) &
                   np.isfinite(intensity_vec) &
                   (intensity_vec > 0))

    if not np.any(keep_filter):
        return np.array([], dtype = np.int64), np.array([], dtype = float), np.array([], dtype = float)

    centroid_rows = assigned_centroid_row[keep_filter]
    observed_mz_values = observed_mz_vec[keep_filter]
    intensity_values = intensity_vec[keep_filter]

    if aggregation == "sum":
        unique_rows, inverse_ids = np.unique(centroid_rows,
                                             return_inverse = True)

        collapsed_intensity = np.zeros(len(unique_rows),
                                       dtype = float)

        weighted_mz_sum = np.zeros(len(unique_rows),
                                   dtype = float)

        np.add.at(collapsed_intensity,
                  inverse_ids,
                  intensity_values)

        np.add.at(weighted_mz_sum,
                  inverse_ids,
                  intensity_values * observed_mz_values)

        collapsed_mz = weighted_mz_sum / collapsed_intensity

    elif aggregation == "max":
        order = np.lexsort((-intensity_values, centroid_rows))
        sorted_rows = centroid_rows[order]
        sorted_intensity = intensity_values[order]
        sorted_mz = observed_mz_values[order]
        unique_rows, start_ids = np.unique(sorted_rows,
                                           return_index = True)
        collapsed_intensity = sorted_intensity[start_ids]
        collapsed_mz = sorted_mz[start_ids]

    else:
        raise ValueError("aggregation must be 'max' or 'sum'.")

    return unique_rows, collapsed_intensity, collapsed_mz
