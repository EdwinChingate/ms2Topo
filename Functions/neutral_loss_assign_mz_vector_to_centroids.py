from __future__ import annotations

from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix

def neutral_loss_assign_mz_vector_to_centroids(mz_vec,
                                  centroid_index,
                                  sigma_obs_vec = None,
                                  min_posterior = 0.8,
                                  min_odds_ratio = 3.0,
                                  diagnostic_mode = "ambiguous"):
    """
    Assign observed neutral-loss m/z values to centroid vocabulary.

    status_vec:
        0 = unassigned
        1 = ambiguous
        2 = confident
    """

    mz_vec = np.asarray(mz_vec,
                        dtype = float)

    n_values = len(mz_vec)

    if sigma_obs_vec is None:
        sigma_obs_vec = np.zeros(n_values,
                                 dtype = float)

    else:
        sigma_obs_vec = np.asarray(sigma_obs_vec,
                                   dtype = float)

    assigned_centroid_row = np.full(n_values,
                                    -1,
                                    dtype = np.int64)

    posterior_vec = np.zeros(n_values,
                             dtype = float)

    n_candidates_vec = np.zeros(n_values,
                                dtype = np.int16)

    status_vec = np.zeros(n_values,
                          dtype = np.int8)

    selected_residual_vec = np.full(n_values,
                                    np.nan,
                                    dtype = float)

    selected_z_vec = np.full(n_values,
                             np.nan,
                             dtype = float)

    diagnostic_rows = []

    centroid_mz = centroid_index["centroid_mz"]
    centroid_sigma = centroid_index["centroid_sigma"]
    centroid_edge = centroid_index["centroid_edge"]
    centroid_count = centroid_index["centroid_count"]
    centroid_prior = centroid_index["centroid_prior"]

    if len(centroid_mz) == 0:
        return assigned_centroid_row, posterior_vec, n_candidates_vec, status_vec, selected_residual_vec, selected_z_vec, diagnostic_rows

    search_edge = float(np.max(centroid_edge))

    for value_id in range(n_values):

        mz_value = mz_vec[value_id]

        if not np.isfinite(mz_value):
            continue

        left_id = np.searchsorted(centroid_mz,
                                  mz_value - search_edge,
                                  side = "left")

        right_id = np.searchsorted(centroid_mz,
                                   mz_value + search_edge,
                                   side = "right")

        if right_id <= left_id:
            continue

        candidate_rows = np.arange(left_id,
                                   right_id,
                                   dtype = np.int64)

        residual_vec = mz_value - centroid_mz[candidate_rows]
        distance_vec = np.abs(residual_vec)
        candidate_filter = distance_vec <= centroid_edge[candidate_rows]
        candidate_rows = candidate_rows[candidate_filter]
        residual_vec = residual_vec[candidate_filter]

        if len(candidate_rows) == 0:
            continue

        sigma_obs = sigma_obs_vec[value_id]

        if not np.isfinite(sigma_obs):
            sigma_obs = 0.0

        sigma_total = np.sqrt(centroid_sigma[candidate_rows] ** 2 + sigma_obs ** 2)
        z_vec = residual_vec / sigma_total
        likelihood_vec = np.exp(-0.5 * z_vec * z_vec) / sigma_total
        score_vec = likelihood_vec * centroid_prior[candidate_rows]
        score_sum = np.sum(score_vec)

        if (score_sum <= 0) or (not np.isfinite(score_sum)):
            continue

        posterior_candidate_vec = score_vec / score_sum
        best_local_id = int(np.argmax(posterior_candidate_vec))
        best_posterior = float(posterior_candidate_vec[best_local_id])
        best_centroid_row = int(candidate_rows[best_local_id])

        if len(posterior_candidate_vec) > 1:
            second_posterior = float(np.partition(posterior_candidate_vec, -2)[-2])
            odds_ratio = best_posterior / second_posterior if second_posterior > 0 else np.inf

        else:
            odds_ratio = np.inf

        assigned_centroid_row[value_id] = best_centroid_row
        posterior_vec[value_id] = best_posterior
        n_candidates_vec[value_id] = len(candidate_rows)
        selected_residual_vec[value_id] = residual_vec[best_local_id]
        selected_z_vec[value_id] = z_vec[best_local_id]

        if (best_posterior >= min_posterior) and (odds_ratio >= min_odds_ratio):
            status_vec[value_id] = 2

        else:
            status_vec[value_id] = 1

        keep_diagnostic = False

        if diagnostic_mode == "all":
            keep_diagnostic = True

        elif diagnostic_mode == "ambiguous":
            keep_diagnostic = (status_vec[value_id] == 1) or (len(candidate_rows) > 1)

        elif diagnostic_mode in [None, "none"]:
            keep_diagnostic = False

        else:
            raise ValueError("diagnostic_mode must be 'ambiguous', 'all', 'none', or None.")

        if keep_diagnostic:
            for local_id, candidate_row in enumerate(candidate_rows):
                diagnostic_rows.append({"value_id": int(value_id),
                                        "observed_mz": float(mz_value),
                                        "candidate_loss_id": int(candidate_row),
                                        "candidate_loss_mz": float(centroid_mz[candidate_row]),
                                        "candidate_sigma": float(centroid_sigma[candidate_row]),
                                        "candidate_edge": float(centroid_edge[candidate_row]),
                                        "candidate_count": float(centroid_count[candidate_row]),
                                        "candidate_prior": float(centroid_prior[candidate_row]),
                                        "mz_residual": float(residual_vec[local_id]),
                                        "z_score": float(z_vec[local_id]),
                                        "likelihood": float(likelihood_vec[local_id]),
                                        "score": float(score_vec[local_id]),
                                        "posterior": float(posterior_candidate_vec[local_id]),
                                        "is_selected": bool(local_id == best_local_id),
                                        "odds_ratio": float(odds_ratio)})

    return assigned_centroid_row, posterior_vec, n_candidates_vec, status_vec, selected_residual_vec, selected_z_vec, diagnostic_rows
