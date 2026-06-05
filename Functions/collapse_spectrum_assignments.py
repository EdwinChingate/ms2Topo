from __future__ import annotations

from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix

def collapse_spectrum_assignments(assigned_centroid_row,
                                  mz_vec,
                                  intensity_vec,
                                  posterior_vec,
                                  status_vec = None,
                                  confident_only = False,
                                  aggregation = "max"):
    """
    Collapse fragment assignments from one spectrum into one value per assigned
    centroid.

    Returns:
        centroid_rows
        collapsed_intensity
        representative_mz
        representative_posterior
        n_fragments_collapsed

    aggregation options:
        "max" -> keep the strongest assigned fragment for each centroid
        "sum" -> sum all fragments assigned to the same centroid; representative
                 m/z is the intensity-weighted mean of assigned observed m/z
    """

    assigned_centroid_row = np.asarray(assigned_centroid_row,
                                       dtype = np.int64)

    mz_vec = np.asarray(mz_vec,
                        dtype = float)

    intensity_vec = np.asarray(intensity_vec,
                               dtype = float)

    posterior_vec = np.asarray(posterior_vec,
                               dtype = float)

    keep_filter = assigned_centroid_row >= 0

    if status_vec is not None and confident_only:
        keep_filter = keep_filter & (status_vec == 2)

    keep_filter = (keep_filter &
                   np.isfinite(mz_vec) &
                   np.isfinite(intensity_vec) &
                   (intensity_vec > 0))

    if not np.any(keep_filter):
        return (np.array([], dtype = np.int64),
                np.array([], dtype = float),
                np.array([], dtype = float),
                np.array([], dtype = float),
                np.array([], dtype = np.int64))

    centroid_rows = assigned_centroid_row[keep_filter]
    mz_values = mz_vec[keep_filter]
    intensity_values = intensity_vec[keep_filter]
    posterior_values = posterior_vec[keep_filter]

    if aggregation == "sum":

        unique_rows, inverse_ids = np.unique(centroid_rows,
                                             return_inverse = True)

        collapsed_intensity = np.zeros(len(unique_rows),
                                       dtype = float)

        weighted_mz_sum = np.zeros(len(unique_rows),
                                   dtype = float)

        weighted_posterior_sum = np.zeros(len(unique_rows),
                                          dtype = float)

        n_fragments_collapsed = np.zeros(len(unique_rows),
                                         dtype = np.int64)

        np.add.at(collapsed_intensity,
                  inverse_ids,
                  intensity_values)

        np.add.at(weighted_mz_sum,
                  inverse_ids,
                  mz_values * intensity_values)

        np.add.at(weighted_posterior_sum,
                  inverse_ids,
                  posterior_values * intensity_values)

        np.add.at(n_fragments_collapsed,
                  inverse_ids,
                  1)

        representative_mz = weighted_mz_sum / collapsed_intensity
        representative_posterior = weighted_posterior_sum / collapsed_intensity

    elif aggregation == "max":

        order = np.lexsort((-intensity_values,
                            centroid_rows))

        sorted_rows = centroid_rows[order]
        sorted_mz = mz_values[order]
        sorted_intensity = intensity_values[order]
        sorted_posterior = posterior_values[order]

        unique_rows, start_ids, counts = np.unique(sorted_rows,
                                                   return_index = True,
                                                   return_counts = True)

        collapsed_intensity = sorted_intensity[start_ids]
        representative_mz = sorted_mz[start_ids]
        representative_posterior = sorted_posterior[start_ids]
        n_fragments_collapsed = counts.astype(np.int64)

    else:
        raise ValueError("aggregation must be 'max' or 'sum'.")

    return unique_rows, collapsed_intensity, representative_mz, representative_posterior, n_fragments_collapsed
