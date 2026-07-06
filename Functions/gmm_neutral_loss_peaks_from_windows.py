# Extracted from notebook: 904937b2-026f-4f59-b3c0-21112b1589f8.ipynb
# One function per file. Auto-generated from top-level function definitions.
from __future__ import annotations

from pathlib import Path
import os
import re
import glob
import sys

import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None

try:
    import networkx as nx
except Exception:
    nx = None

try:
    from sklearn.mixture import GaussianMixture
except Exception:
    GaussianMixture = None

# Local function dependencies extracted from the same notebook.
from gmm_variances_1d import gmm_variances_1d
from search_neutral_loss_gmm_components import search_neutral_loss_gmm_components


def gmm_neutral_loss_peaks_from_windows(neutral_losses_array,
                                        mz_windows,
                                        target_component_iqr_da = 1e-3,
                                        target_component_iqr_ppm = 3,
                                        min_counts = 3,
                                        min_points_per_component = 5,
                                        max_components_cap = 10,
                                        covariance_type = "full",
                                        reg_covar = (1e-5)**2,
                                        max_iter = 1000,
                                        random_state = 7,
                                        std_distance = 3,
                                        skip_gmm_for_tolerable_iqr = True,
                                        assignment_window_padding_da = 0.0,
                                        assignment_window_padding_ppm = 0.0):
    """
    Refine m/z windows with local GMMs and return an extended m/z-object table.

    Important:
        mz_windows[:, 0:2] are start/stop indexes into neutral_losses_array.
        Therefore neutral_losses_array must be in the same sorted order used
        to create the compressed windows.

        If the windows were created with compress_fragment_intervals_by_overlap,
        use:

            neutral_losses_array = result["sorted_fragment_mz_table"][:, mz_col]

        not the original unsorted all_fragment_mz_table[:, mz_col].

    This function is meant to define an alignment vocabulary, not to filter
    fragments. For this reason it also reports assignment windows based on the
    observed component members:

        output[:, 19] = assignment min m/z
        output[:, 20] = assignment max m/z

    Those columns can be passed to align_consensus_spectra_to_fragment_centroids
    as centroid_min_mz_col and centroid_max_mz_col to guarantee that training
    fragments remain inside at least one centroid window.

    Output:
        neutral_loss_gmm_peaks[:, 0]  = median mz
        neutral_loss_gmm_peaks[:, 1]  = count
        neutral_loss_gmm_peaks[:, 2]  = start index
        neutral_loss_gmm_peaks[:, 3]  = stop index, exclusive
        neutral_loss_gmm_peaks[:, 4]  = IQR mz, Da
        neutral_loss_gmm_peaks[:, 5]  = IQR mz, ppm

        neutral_loss_gmm_peaks[:, 6]  = Gaussian mz, Da
        neutral_loss_gmm_peaks[:, 7]  = Gaussian std, Da
        neutral_loss_gmm_peaks[:, 8]  = Gaussian std, ppm
        neutral_loss_gmm_peaks[:, 9]  = Gaussian min mz, mean - std_distance * std
        neutral_loss_gmm_peaks[:, 10] = Gaussian max mz, mean + std_distance * std

        neutral_loss_gmm_peaks[:, 11] = component weight
        neutral_loss_gmm_peaks[:, 12] = expected count
        neutral_loss_gmm_peaks[:, 13] = mean responsibility
        neutral_loss_gmm_peaks[:, 14] = min responsibility

        neutral_loss_gmm_peaks[:, 15] = local n components
        neutral_loss_gmm_peaks[:, 16] = local BIC
        neutral_loss_gmm_peaks[:, 17] = local AIC
        neutral_loss_gmm_peaks[:, 18] = delta BIC vs one-component model

        neutral_loss_gmm_peaks[:, 19] = assignment min mz, observed component min - padding
        neutral_loss_gmm_peaks[:, 20] = assignment max mz, observed component max + padding
    """

    if target_component_iqr_da <= 0:
        raise ValueError("target_component_iqr_da must be > 0")

    if target_component_iqr_ppm <= 0:
        raise ValueError("target_component_iqr_ppm must be > 0")

    if assignment_window_padding_da < 0:
        raise ValueError("assignment_window_padding_da must be >= 0")

    if assignment_window_padding_ppm < 0:
        raise ValueError("assignment_window_padding_ppm must be >= 0")

    neutral_losses_array = np.asarray(neutral_losses_array,
                                      dtype = float)

    mz_windows = np.asarray(mz_windows,
                            dtype = float)

    rows = []

    for window_id, mz_window in enumerate(mz_windows):

        low_id_mz = int(mz_window[0])
        high_id_mz = int(mz_window[1])
        iqr_mz_da = float(mz_window[2])

        mz_vec = neutral_losses_array[low_id_mz: high_id_mz]

        mz_vec = np.asarray(mz_vec,
                            dtype = float)

        mz_vec = mz_vec[np.isfinite(mz_vec)]

        n_points = len(mz_vec)

        if n_points < min_counts:
            continue

        median_mz_window = np.median(mz_vec)

        target_iqr_da = max(target_component_iqr_da,
                            target_component_iqr_ppm / 1e6 * median_mz_window)

        if skip_gmm_for_tolerable_iqr and iqr_mz_da <= target_iqr_da:

            median_mz = median_mz_window

            q1_mz = np.percentile(mz_vec,
                                  25)

            q3_mz = np.percentile(mz_vec,
                                  75)

            component_iqr_mz_da = q3_mz - q1_mz

            if median_mz != 0:
                component_iqr_mz_ppm = component_iqr_mz_da / median_mz * 1e6

            else:
                component_iqr_mz_ppm = np.nan

            gaussian_mz = np.mean(mz_vec)

            if n_points > 1:
                gaussian_std = np.std(mz_vec,
                                      ddof = 1)

            else:
                gaussian_std = 0

            gaussian_std = max(gaussian_std,
                               np.sqrt(reg_covar))

            gaussian_std_ppm = gaussian_std / gaussian_mz * 1e6

            gaussian_min_mz = gaussian_mz - std_distance * gaussian_std
            gaussian_max_mz = gaussian_mz + std_distance * gaussian_std

            assignment_padding = max(assignment_window_padding_da,
                                     assignment_window_padding_ppm / 1e6 * gaussian_mz)

            assignment_min_mz = np.min(mz_vec) - assignment_padding
            assignment_max_mz = np.max(mz_vec) + assignment_padding

            rows.append([median_mz,
                         n_points,
                         low_id_mz,
                         high_id_mz,
                         component_iqr_mz_da,
                         component_iqr_mz_ppm,
                         gaussian_mz,
                         gaussian_std,
                         gaussian_std_ppm,
                         gaussian_min_mz,
                         gaussian_max_mz,
                         1.0,
                         float(n_points),
                         1.0,
                         1.0,
                         1,
                         np.nan,
                         np.nan,
                         np.nan,
                         assignment_min_mz,
                         assignment_max_mz])

            continue

        max_by_points = n_points // min_points_per_component

        if iqr_mz_da <= 0:
            max_by_iqr = 1

        else:
            max_by_iqr = int(np.ceil(iqr_mz_da / target_iqr_da))

        max_components = min(max_by_points,
                             max_by_iqr,
                             max_components_cap)

        max_components = max(max_components,
                             1)

        best_gmm, gmm_search_df, models_dict = search_neutral_loss_gmm_components(mz_vec = mz_vec,
                                                                                  min_components = 1,
                                                                                  max_components = max_components,
                                                                                  covariance_type = covariance_type,
                                                                                  reg_covar = reg_covar,
                                                                                  max_iter = max_iter,
                                                                                  random_state = random_state)

        x = mz_vec.reshape(-1, 1)

        labels = best_gmm.predict(x)
        responsibilities = best_gmm.predict_proba(x)

        gaussian_mz_vec = best_gmm.means_.reshape(-1)
        gaussian_std_vec = np.sqrt(gmm_variances_1d(best_gmm))
        component_weight_vec = best_gmm.weights_

        local_bic = np.min(gmm_search_df["BIC"])
        local_aic = np.min(gmm_search_df["AIC"])

        one_component_bic = gmm_search_df.loc[gmm_search_df["n_components"] == 1,
                                              "BIC"].iloc[0]

        delta_bic_vs_one = local_bic - one_component_bic

        for component_id in range(best_gmm.n_components):

            component_local_ids = np.where(labels == component_id)[0]

            if len(component_local_ids) < min_counts:
                continue

            component_mz_vec = mz_vec[component_local_ids]

            component_mz_vec = np.asarray(component_mz_vec,
                                          dtype = float)

            component_mz_vec = component_mz_vec[np.isfinite(component_mz_vec)]

            if len(component_mz_vec) < min_counts:
                continue

            component_start_idx = low_id_mz + int(np.min(component_local_ids))
            component_stop_idx = low_id_mz + int(np.max(component_local_ids)) + 1

            median_mz = np.median(component_mz_vec)

            q1_mz = np.percentile(component_mz_vec,
                                  25)

            q3_mz = np.percentile(component_mz_vec,
                                  75)

            component_iqr_mz_da = q3_mz - q1_mz

            if median_mz != 0:
                component_iqr_mz_ppm = component_iqr_mz_da / median_mz * 1e6

            else:
                component_iqr_mz_ppm = np.nan

            gaussian_mz = gaussian_mz_vec[component_id]
            gaussian_std = gaussian_std_vec[component_id]
            gaussian_std_ppm = gaussian_std / gaussian_mz * 1e6

            gaussian_min_mz = gaussian_mz - std_distance * gaussian_std
            gaussian_max_mz = gaussian_mz + std_distance * gaussian_std

            assignment_padding = max(assignment_window_padding_da,
                                     assignment_window_padding_ppm / 1e6 * gaussian_mz)

            assignment_min_mz = np.min(component_mz_vec) - assignment_padding
            assignment_max_mz = np.max(component_mz_vec) + assignment_padding

            component_responsibility_vec = responsibilities[component_local_ids,
                                                            component_id]

            expected_count = np.sum(responsibilities[:, component_id])
            mean_responsibility = np.mean(component_responsibility_vec)
            min_responsibility = np.min(component_responsibility_vec)

            rows.append([median_mz,
                         len(component_mz_vec),
                         component_start_idx,
                         component_stop_idx,
                         component_iqr_mz_da,
                         component_iqr_mz_ppm,
                         gaussian_mz,
                         gaussian_std,
                         gaussian_std_ppm,
                         gaussian_min_mz,
                         gaussian_max_mz,
                         component_weight_vec[component_id],
                         expected_count,
                         mean_responsibility,
                         min_responsibility,
                         best_gmm.n_components,
                         local_bic,
                         local_aic,
                         delta_bic_vs_one,
                         assignment_min_mz,
                         assignment_max_mz])

    if len(rows) == 0:
        return np.zeros((0, 21))

    neutral_loss_gmm_peaks = np.array(rows,
                                      dtype = float)

    neutral_loss_gmm_peaks = neutral_loss_gmm_peaks[neutral_loss_gmm_peaks[:, 0].argsort(), :]

    return neutral_loss_gmm_peaks
