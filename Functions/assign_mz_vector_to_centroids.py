from __future__ import annotations

from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix

def assign_mz_vector_to_centroids(mz_vec,
                                  centroid_index,
                                  sigma_obs_da_vec = None,
                                  min_posterior = 0.8,
                                  min_odds_ratio = 3.0,
                                  diagnostic_mode = None):
    """
    Assign a vector of observed fragment m/z values to clustered-fragment
    centroids.

    Returns arrays with one value per observed fragment:
        assigned_centroid_row -> row index in the sorted centroid vocabulary
        posterior_vec         -> posterior probability of the selected centroid
        n_candidates_vec      -> number of candidate centroids
        status_vec            -> 0 unassigned, 1 ambiguous, 2 confident

    diagnostic_mode options:
        None        -> no candidate-level diagnostic records
        "ambiguous" -> records candidate posteriors only for fragments with
                       more than one candidate or ambiguous final status
        "all"       -> records candidate posteriors for every assigned fragment
    """

    if diagnostic_mode not in [None, "ambiguous", "all"]:
        raise ValueError("diagnostic_mode must be None, 'ambiguous', or 'all'.")

    mz_vec = np.asarray(mz_vec,
                        dtype = float)

    n_fragments = len(mz_vec)

    if sigma_obs_da_vec is None:
        sigma_obs_da_vec = np.zeros(n_fragments,
                                    dtype = float)

    else:
        sigma_obs_da_vec = np.asarray(sigma_obs_da_vec,
                                      dtype = float)

        if len(sigma_obs_da_vec) != n_fragments:
            raise ValueError("sigma_obs_da_vec must have the same length as mz_vec.")

        sigma_obs_da_vec = np.where(np.isfinite(sigma_obs_da_vec) & (sigma_obs_da_vec > 0),
                                    sigma_obs_da_vec,
                                    0.0)

    assigned_centroid_row = np.full(n_fragments,
                                    -1,
                                    dtype = np.int64)

    posterior_vec = np.zeros(n_fragments,
                             dtype = float)

    n_candidates_vec = np.zeros(n_fragments,
                                dtype = np.int16)

    status_vec = np.zeros(n_fragments,
                          dtype = np.int8)

    candidate_diagnostic_rows = []

    centroid_mz = centroid_index["centroid_mz"]
    centroid_sigma = centroid_index["centroid_sigma"]
    centroid_edge = centroid_index["centroid_edge"]
    centroid_prior = centroid_index["centroid_prior"]
    centroid_count = centroid_index["centroid_count"]
    centroid_original_id = centroid_index["centroid_original_id"]

    if len(centroid_mz) == 0:
        return assigned_centroid_row, posterior_vec, n_candidates_vec, status_vec, candidate_diagnostic_rows

    search_edge = float(np.max(centroid_edge))

    for fragment_id in range(n_fragments):

        mz_value = mz_vec[fragment_id]

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

        distance_vec = mz_value - centroid_mz[candidate_rows]
        abs_distance_vec = np.abs(distance_vec)

        candidate_filter = abs_distance_vec <= centroid_edge[candidate_rows]
        candidate_rows = candidate_rows[candidate_filter]
        distance_vec = distance_vec[candidate_filter]
        abs_distance_vec = abs_distance_vec[candidate_filter]

        if len(candidate_rows) == 0:
            continue

        sigma_total = np.sqrt(centroid_sigma[candidate_rows] ** 2 +
                              sigma_obs_da_vec[fragment_id] ** 2)

        z_vec = distance_vec / sigma_total
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
            second_posterior = float(np.partition(posterior_candidate_vec,
                                                  -2)[-2])

            if second_posterior > 0:
                odds_ratio = best_posterior / second_posterior

            else:
                odds_ratio = np.inf

        else:
            odds_ratio = np.inf

        assigned_centroid_row[fragment_id] = best_centroid_row
        posterior_vec[fragment_id] = best_posterior
        n_candidates_vec[fragment_id] = len(candidate_rows)

        if (best_posterior >= min_posterior) and (odds_ratio >= min_odds_ratio):
            status_vec[fragment_id] = 2

        else:
            status_vec[fragment_id] = 1

        keep_diagnostic = False

        if diagnostic_mode == "all":
            keep_diagnostic = True

        elif diagnostic_mode == "ambiguous":
            keep_diagnostic = (len(candidate_rows) > 1) or (status_vec[fragment_id] == 1)

        if keep_diagnostic:
            for local_candidate_id, centroid_row in enumerate(candidate_rows):
                candidate_diagnostic_rows.append({"fragment_id_in_vector": fragment_id,
                                                  "candidate_rank_input": local_candidate_id,
                                                  "candidate_fragment_id": int(centroid_row),
                                                  "candidate_centroid_original_id": int(centroid_original_id[centroid_row]),
                                                  "candidate_mz": float(centroid_mz[centroid_row]),
                                                  "candidate_sigma": float(centroid_sigma[centroid_row]),
                                                  "candidate_edge": float(centroid_edge[centroid_row]),
                                                  "candidate_count": float(centroid_count[centroid_row]),
                                                  "candidate_prior": float(centroid_prior[centroid_row]),
                                                  "observed_mz": float(mz_value),
                                                  "mz_residual": float(distance_vec[local_candidate_id]),
                                                  "abs_mz_residual": float(abs_distance_vec[local_candidate_id]),
                                                  "sigma_total": float(sigma_total[local_candidate_id]),
                                                  "z_score": float(z_vec[local_candidate_id]),
                                                  "likelihood": float(likelihood_vec[local_candidate_id]),
                                                  "score": float(score_vec[local_candidate_id]),
                                                  "posterior": float(posterior_candidate_vec[local_candidate_id]),
                                                  "is_selected": bool(centroid_row == best_centroid_row),
                                                  "best_posterior": best_posterior,
                                                  "odds_ratio": float(odds_ratio)})

    return assigned_centroid_row, posterior_vec, n_candidates_vec, status_vec, candidate_diagnostic_rows
