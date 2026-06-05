from __future__ import annotations

from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix
from assign_mz_vector_to_centroids import *
from centroid_index_to_dataframe import *
from clustered_fragments_to_centroid_index import *
from collapse_spectrum_assignments import *
from summarize_centroid_assignments import *
from summarize_fragment_assignments import *

def assign_loaded_consensus_fragments_to_centroids(loaded_consensus_fragments_df,
                                                   feature_id_map_df,
                                                   clustered_fragments_df,
                                                   mz_col = "median_mz(Da)",
                                                   intensity_col = "median_Int",
                                                   mz_std_col = "IQR_mz(Da)",
                                                   spectrum_id_col = "spectrum_id",
                                                   centroid_mz_col = "6",
                                                   centroid_std_col = "7",
                                                   centroid_count_col = "1",
                                                   centroid_min_mz_col = None,
                                                   centroid_max_mz_col = None,
                                                   std_distance = 3,
                                                   ppm_tol = 20,
                                                   max_abs_tol = 0.01,
                                                   sigma_floor = 2e-4,
                                                   prior_power = 0.5,
                                                   use_observed_mz_uncertainty = True,
                                                   min_posterior = 0.8,
                                                   min_odds_ratio = 3.0,
                                                   confident_only = False,
                                                   aggregation = "max",
                                                   diagnostic_mode = "ambiguous"):
    """
    Assign loaded consensus fragments to an already learned GMM centroid
    vocabulary.

    Main outputs:
        aligned_intensity_sparse_mat -> centroid rows x spectra columns
        aligned_mz_sparse_mat        -> representative observed m/z per cell
        fragment_assignment_df       -> one row per observed fragment
        candidate_diagnostic_df      -> one row per candidate centroid for
                                        ambiguous/all diagnostic cases
    """

    centroid_index = clustered_fragments_to_centroid_index(clustered_fragments_df = clustered_fragments_df,
                                                          centroid_mz_col = centroid_mz_col,
                                                          centroid_std_col = centroid_std_col,
                                                          centroid_count_col = centroid_count_col,
                                                          centroid_min_mz_col = centroid_min_mz_col,
                                                          centroid_max_mz_col = centroid_max_mz_col,
                                                          std_distance = std_distance,
                                                          ppm_tol = ppm_tol,
                                                          max_abs_tol = max_abs_tol,
                                                          sigma_floor = sigma_floor,
                                                          prior_power = prior_power)

    centroid_df = centroid_index_to_dataframe(centroid_index = centroid_index)

    feature_id_map_df = feature_id_map_df.sort_values(spectrum_id_col).reset_index(drop = True)

    n_centroids = len(centroid_index["centroid_mz"])
    n_spectra = len(feature_id_map_df)

    intensity_row_chunks = []
    intensity_col_chunks = []
    intensity_data_chunks = []

    mz_row_chunks = []
    mz_col_chunks = []
    mz_data_chunks = []

    assignment_rows = []
    candidate_diagnostic_rows = []
    collapse_rows = []

    spectrum_id_vec = loaded_consensus_fragments_df[spectrum_id_col].to_numpy(dtype = int)

    for spectrum_id in range(n_spectra):

        spectrum_filter = spectrum_id_vec == spectrum_id

        if not np.any(spectrum_filter):
            continue

        spectrum_df = loaded_consensus_fragments_df.loc[spectrum_filter]

        mz_vec = pd.to_numeric(spectrum_df[mz_col],
                               errors = "coerce").to_numpy(dtype = float)

        intensity_vec = pd.to_numeric(spectrum_df[intensity_col],
                                      errors = "coerce").to_numpy(dtype = float)

        if use_observed_mz_uncertainty and mz_std_col in spectrum_df.columns:
            sigma_obs_da_vec = pd.to_numeric(spectrum_df[mz_std_col],
                                             errors = "coerce").to_numpy(dtype = float)

        else:
            sigma_obs_da_vec = None

        assigned_rows, posterior_vec, n_candidates_vec, status_vec, candidate_rows = assign_mz_vector_to_centroids(
            mz_vec = mz_vec,
            centroid_index = centroid_index,
            sigma_obs_da_vec = sigma_obs_da_vec,
            min_posterior = min_posterior,
            min_odds_ratio = min_odds_ratio,
            diagnostic_mode = diagnostic_mode)

        centroid_rows, collapsed_intensity, representative_mz, representative_posterior, n_fragments_collapsed = collapse_spectrum_assignments(
            assigned_centroid_row = assigned_rows,
            mz_vec = mz_vec,
            intensity_vec = intensity_vec,
            posterior_vec = posterior_vec,
            status_vec = status_vec,
            confident_only = confident_only,
            aggregation = aggregation)

        if len(centroid_rows) > 0:
            intensity_row_chunks.append(centroid_rows)
            intensity_col_chunks.append(np.full(len(centroid_rows),
                                                spectrum_id,
                                                dtype = np.int64))
            intensity_data_chunks.append(collapsed_intensity)

            mz_row_chunks.append(centroid_rows)
            mz_col_chunks.append(np.full(len(centroid_rows),
                                         spectrum_id,
                                         dtype = np.int64))
            mz_data_chunks.append(representative_mz)

            feat_id = feature_id_map_df.loc[spectrum_id, "feat_id"]

            for local_id in range(len(centroid_rows)):
                collapse_rows.append({"spectrum_id": spectrum_id,
                                      "feat_id": feat_id,
                                      "aligned_fragment_id": int(centroid_rows[local_id]),
                                      "aligned_fragment_mz": float(centroid_index["centroid_mz"][centroid_rows[local_id]]),
                                      "representative_observed_mz": float(representative_mz[local_id]),
                                      "aligned_intensity": float(collapsed_intensity[local_id]),
                                      "representative_posterior": float(representative_posterior[local_id]),
                                      "n_fragments_collapsed": int(n_fragments_collapsed[local_id])})

        feat_id = feature_id_map_df.loc[spectrum_id, "feat_id"]

        assignment_df = pd.DataFrame({"spectrum_id": spectrum_id,
                                      "feat_id": feat_id,
                                      "fragment_id_in_spectrum": spectrum_df["fragment_id_in_spectrum"].to_numpy(dtype = int),
                                      "fragment_mz": mz_vec,
                                      "fragment_intensity": intensity_vec,
                                      "assigned_fragment_id": assigned_rows,
                                      "assigned_centroid_original_id": np.where(assigned_rows >= 0,
                                                                                 centroid_index["centroid_original_id"][np.maximum(assigned_rows, 0)],
                                                                                 -1),
                                      "assigned_fragment_mz": np.where(assigned_rows >= 0,
                                                                        centroid_index["centroid_mz"][np.maximum(assigned_rows, 0)],
                                                                        np.nan),
                                      "mz_residual": np.where(assigned_rows >= 0,
                                                              mz_vec - centroid_index["centroid_mz"][np.maximum(assigned_rows, 0)],
                                                              np.nan),
                                      "assignment_posterior": posterior_vec,
                                      "n_candidate_fragments": n_candidates_vec,
                                      "assignment_status": status_vec})

        assignment_rows.append(assignment_df)

        if len(candidate_rows) > 0:
            candidate_df = pd.DataFrame(candidate_rows)
            candidate_df["spectrum_id"] = spectrum_id
            candidate_df["feat_id"] = feat_id
            candidate_df["fragment_id_in_spectrum"] = candidate_df["fragment_id_in_vector"].map(
                lambda fragment_id: int(spectrum_df["fragment_id_in_spectrum"].iloc[fragment_id]))
            candidate_df = candidate_df.drop(columns = ["fragment_id_in_vector"])
            candidate_diagnostic_rows.append(candidate_df)

    if len(intensity_data_chunks) == 0:
        aligned_intensity_sparse_mat = csr_matrix((n_centroids,
                                                   n_spectra),
                                                  dtype = float)

        aligned_mz_sparse_mat = csr_matrix((n_centroids,
                                            n_spectra),
                                           dtype = float)

    else:
        aligned_intensity_sparse_mat = coo_matrix((np.concatenate(intensity_data_chunks),
                                                   (np.concatenate(intensity_row_chunks),
                                                    np.concatenate(intensity_col_chunks))),
                                                  shape = (n_centroids,
                                                           n_spectra)).tocsr()

        aligned_mz_sparse_mat = coo_matrix((np.concatenate(mz_data_chunks),
                                            (np.concatenate(mz_row_chunks),
                                             np.concatenate(mz_col_chunks))),
                                           shape = (n_centroids,
                                                    n_spectra)).tocsr()

    if len(assignment_rows) > 0:
        fragment_assignment_df = pd.concat(assignment_rows,
                                           axis = 0,
                                           ignore_index = True)

    else:
        fragment_assignment_df = pd.DataFrame()

    if len(candidate_diagnostic_rows) > 0:
        candidate_diagnostic_df = pd.concat(candidate_diagnostic_rows,
                                            axis = 0,
                                            ignore_index = True)

    else:
        candidate_diagnostic_df = pd.DataFrame()

    if len(collapse_rows) > 0:
        collapsed_assignment_df = pd.DataFrame(collapse_rows)

    else:
        collapsed_assignment_df = pd.DataFrame()

    assignment_summary_df = summarize_fragment_assignments(fragment_assignment_df = fragment_assignment_df,
                                                           feature_id_map_df = feature_id_map_df)

    centroid_diagnostic_df = summarize_centroid_assignments(fragment_assignment_df = fragment_assignment_df,
                                                           centroid_df = centroid_df)

    return {"aligned_intensity_sparse_mat": aligned_intensity_sparse_mat,
            "aligned_mz_sparse_mat": aligned_mz_sparse_mat,
            "aligned_fragment_mz_vec": centroid_index["centroid_mz"],
            "centroid_index": centroid_index,
            "centroid_df": centroid_df,
            "fragment_assignment_df": fragment_assignment_df,
            "candidate_diagnostic_df": candidate_diagnostic_df,
            "collapsed_assignment_df": collapsed_assignment_df,
            "assignment_summary_df": assignment_summary_df,
            "centroid_diagnostic_df": centroid_diagnostic_df}
