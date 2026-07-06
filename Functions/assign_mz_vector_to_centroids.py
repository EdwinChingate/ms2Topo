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


def assign_mz_vector_to_centroids(mz_vec,
                                  centroid_index,
                                  sigma_obs_da_vec = None,
                                  min_posterior = 0.8,
                                  min_odds_ratio = 3.0,
                                  diagnostic_mode = None,
                                  max_z_score = 3.0,
                                  min_z_score_gap = 0.5):
    """
    Assign a vector of observed fragment m/z values to clustered-fragment
    centroids using closest z-score assignment.

    Returns arrays with one value per observed fragment:
        assigned_centroid_row -> row index in the sorted centroid vocabulary
        posterior_vec         -> compatibility field. It now stores a bounded
                                 z-score similarity for the selected centroid:
                                     exp(-0.5 * abs_z_score ** 2)
                                 It is not a Bayesian posterior.
        n_candidates_vec      -> number of candidate centroids
        status_vec            -> 0 unassigned, 1 ambiguous, 2 confident

    Assignment logic:
        1. Candidate centroids are selected by the hard centroid m/z window.
        2. For each candidate:
               sigma_total = sqrt(centroid_sigma ** 2 + observed_sigma ** 2)
               abs_z_score = abs(observed_mz - centroid_mz) / sigma_total
        3. The selected centroid is the candidate with the smallest abs_z_score.

    Confidence logic:
        A selected assignment is confident when:
            best_abs_z_score <= max_z_score
        and
            second_best_abs_z_score - best_abs_z_score >= min_z_score_gap

        For one-candidate assignments, the z-score gap is treated as infinity.

    min_posterior and min_odds_ratio are retained only for backwards
    compatibility with older notebooks. They are not used by the z-score
    assignment workflow.

    diagnostic_mode options:
        None        -> no candidate-level diagnostic records
        "ambiguous" -> records candidate diagnostics only for fragments with
                       more than one candidate or ambiguous final status
        "all"       -> records candidate diagnostics for every assigned fragment
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

        good_sigma_filter = np.isfinite(sigma_total) & (sigma_total > 0)
        candidate_rows = candidate_rows[good_sigma_filter]
        distance_vec = distance_vec[good_sigma_filter]
        abs_distance_vec = abs_distance_vec[good_sigma_filter]
        sigma_total = sigma_total[good_sigma_filter]

        if len(candidate_rows) == 0:
            continue

        z_vec = distance_vec / sigma_total
        abs_z_vec = np.abs(z_vec)
        z_score_similarity_vec = np.exp(-0.5 * abs_z_vec * abs_z_vec)

        best_local_id = int(np.argmin(abs_z_vec))
        best_abs_z_score = float(abs_z_vec[best_local_id])
        best_z_score = float(z_vec[best_local_id])
        best_z_score_similarity = float(z_score_similarity_vec[best_local_id])
        best_centroid_row = int(candidate_rows[best_local_id])

        if len(abs_z_vec) > 1:
            second_best_abs_z_score = float(np.partition(abs_z_vec,
                                                         1)[1])
            z_score_gap = second_best_abs_z_score - best_abs_z_score

        else:
            second_best_abs_z_score = np.inf
            z_score_gap = np.inf

        if max_z_score is None:
            passes_z_score = True

        else:
            passes_z_score = best_abs_z_score <= max_z_score

        if min_z_score_gap is None:
            passes_gap = True

        else:
            passes_gap = z_score_gap >= min_z_score_gap

        assigned_centroid_row[fragment_id] = best_centroid_row
        posterior_vec[fragment_id] = best_z_score_similarity
        n_candidates_vec[fragment_id] = len(candidate_rows)

        if passes_z_score and passes_gap:
            status_vec[fragment_id] = 2

        else:
            status_vec[fragment_id] = 1

        keep_diagnostic = False

        if diagnostic_mode == "all":
            keep_diagnostic = True

        elif diagnostic_mode == "ambiguous":
            keep_diagnostic = (len(candidate_rows) > 1) or (status_vec[fragment_id] == 1)

        if keep_diagnostic:
            candidate_rank_by_z = np.argsort(abs_z_vec)
            rank_lookup = np.empty(len(candidate_rank_by_z),
                                   dtype = int)
            rank_lookup[candidate_rank_by_z] = np.arange(len(candidate_rank_by_z),
                                                         dtype = int)

            for local_candidate_id, centroid_row in enumerate(candidate_rows):
                candidate_diagnostic_rows.append({"fragment_id_in_vector": fragment_id,
                                                  "candidate_rank_input": local_candidate_id,
                                                  "candidate_rank_by_z_score": int(rank_lookup[local_candidate_id]),
                                                  "candidate_fragment_id": int(centroid_row),
                                                  "candidate_centroid_original_id": int(centroid_original_id[centroid_row]),
                                                  "candidate_mz": float(centroid_mz[centroid_row]),
                                                  "candidate_sigma": float(centroid_sigma[centroid_row]),
                                                  "candidate_edge": float(centroid_edge[centroid_row]),
                                                  "candidate_count": float(centroid_count[centroid_row]),
                                                  "observed_mz": float(mz_value),
                                                  "mz_residual": float(distance_vec[local_candidate_id]),
                                                  "abs_mz_residual": float(abs_distance_vec[local_candidate_id]),
                                                  "sigma_total": float(sigma_total[local_candidate_id]),
                                                  "z_score": float(z_vec[local_candidate_id]),
                                                  "abs_z_score": float(abs_z_vec[local_candidate_id]),
                                                  "z_score_similarity": float(z_score_similarity_vec[local_candidate_id]),
                                                  "is_selected": bool(centroid_row == best_centroid_row),
                                                  "best_z_score": best_z_score,
                                                  "best_abs_z_score": best_abs_z_score,
                                                  "second_best_abs_z_score": float(second_best_abs_z_score),
                                                  "z_score_gap": float(z_score_gap),
                                                  "best_z_score_similarity": best_z_score_similarity})

    return assigned_centroid_row, posterior_vec, n_candidates_vec, status_vec, candidate_diagnostic_rows
