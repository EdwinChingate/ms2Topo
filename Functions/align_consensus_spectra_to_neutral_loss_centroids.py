from __future__ import annotations

from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix
from neutral_loss_assign_mz_vector_to_centroids import *
from build_centroid_diagnostic_df import *
from centroid_index_to_dataframe import *
from neutral_loss_collapse_spectrum_assignments import *
from get_consensus_spectrum_paths import *
from neutral_loss_centroids_to_index import *
from neutral_losses_from_spectrum_arrays import *
from read_consensus_spectrum_arrays import *
from sparse_alignment_to_wide_df import *
from write_sparse_alignment_to_wide_csv import *

def align_consensus_spectra_to_neutral_loss_centroids(consensus_spectra_folder,
                                                       neutral_loss_gmm_peaks,
                                                       selected_feat_ids = None,
                                                       file_name_template = "Consensus_ms2-spectra_{feat_id}.csv",
                                                       mz_col = "median_mz(Da)",
                                                       intensity_col = "median_Int",
                                                       mz_std_col = "IQR_mz(Da)",
                                                       mz_iqr_ppm_col = "IQR_mz(ppm)",
                                                       drop_nonpositive_intensity = True,
                                                       normalization = "l2",
                                                       min_neutral_loss = 18.0,
                                                       max_neutral_loss = None,
                                                       min_fragment_intensity = 0,
                                                       pair_intensity = "min",
                                                       continue_on_error = True,
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
                                                       diagnostic_mode = "ambiguous",
                                                       return_wide_df = False,
                                                       return_loss_assignment_df = False,
                                                       output_intensity_path = None,
                                                       output_mz_path = None):
    """
    Align within-spectrum neutral losses to an already learned GMM neutral-loss
    centroid vocabulary.

    This function is the neutral-loss analogue of fragment centroid assignment:
        consensus spectra -> fragment differences -> GMM centroid assignment ->
        aligned neutral-loss intensity/mz matrices.

    Key outputs:
        aligned_loss_intensity_sparse_mat
        aligned_loss_mz_sparse_mat
        loss_assignment_df                 optional, potentially large
        candidate_diagnostic_df            ambiguous/all GMM decisions
        centroid_diagnostic_df             centroid-level behavior
        assignment_summary_df              spectrum-level coverage
    """

    spectrum_rows = get_consensus_spectrum_paths(consensus_spectra_folder = consensus_spectra_folder,
                                                 selected_feat_ids = selected_feat_ids,
                                                 file_name_template = file_name_template)

    if len(spectrum_rows) == 0:
        raise ValueError("No consensus spectra were found.")

    centroid_index = neutral_loss_centroids_to_index(neutral_loss_gmm_peaks = neutral_loss_gmm_peaks,
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

    centroid_df = centroid_index_to_dataframe(centroid_index = centroid_index,
                                                  id_col = "aligned_loss_id",
                                                  mz_col = "aligned_loss_mz")

    n_centroids = len(centroid_index["centroid_mz"])

    row_chunks = []
    col_chunks = []
    intensity_chunks = []
    mz_chunks = []
    assignment_rows = []
    diagnostic_rows = []
    summary_rows = []
    feature_id_map_rows = []

    spectrum_id = 0

    for spectrum_row in spectrum_rows:

        feat_id = spectrum_row["feat_id"]
        consensus_spectrum_path = spectrum_row["consensus_spectrum_path"]

        try:
            spectrum_arrays = read_consensus_spectrum_arrays(consensus_spectrum_path = consensus_spectrum_path,
                                                             mz_col = mz_col,
                                                             intensity_col = intensity_col,
                                                             mz_std_col = mz_std_col,
                                                             mz_iqr_ppm_col = mz_iqr_ppm_col,
                                                             drop_nonpositive_intensity = drop_nonpositive_intensity,
                                                             normalization = normalization)

            fragment_mz = spectrum_arrays["fragment_mz"]
            fragment_intensity = spectrum_arrays["fragment_intensity"]
            fragment_mz_std = spectrum_arrays["fragment_mz_std"]
            fragment_id = spectrum_arrays["fragment_id"]

            if len(fragment_mz) > 0 and min_fragment_intensity > 0:
                keep_fragment = fragment_intensity > min_fragment_intensity
                fragment_mz = fragment_mz[keep_fragment]
                fragment_intensity = fragment_intensity[keep_fragment]
                fragment_mz_std = fragment_mz_std[keep_fragment]
                fragment_id = fragment_id[keep_fragment]

            losses = neutral_losses_from_spectrum_arrays(fragment_mz = fragment_mz,
                                                         fragment_intensity = fragment_intensity,
                                                         fragment_mz_std = fragment_mz_std,
                                                         fragment_id = fragment_id,
                                                         min_neutral_loss = min_neutral_loss,
                                                         max_neutral_loss = max_neutral_loss,
                                                         pair_intensity = pair_intensity)

            neutral_loss_mz = losses["neutral_loss_mz"]
            neutral_loss_intensity = losses["neutral_loss_intensity"]
            neutral_loss_mz_std = losses["neutral_loss_mz_std"]

            if use_observed_mz_uncertainty:
                sigma_obs_vec = neutral_loss_mz_std

            else:
                sigma_obs_vec = None

            assigned_rows, posterior_vec, n_candidates_vec, status_vec, residual_vec, z_vec, current_diagnostic_rows = neutral_loss_assign_mz_vector_to_centroids(
                mz_vec = neutral_loss_mz,
                centroid_index = centroid_index,
                sigma_obs_vec = sigma_obs_vec,
                min_posterior = min_posterior,
                min_odds_ratio = min_odds_ratio,
                diagnostic_mode = diagnostic_mode)

            centroid_rows, collapsed_intensity, collapsed_mz = neutral_loss_collapse_spectrum_assignments(
                assigned_centroid_row = assigned_rows,
                observed_mz_vec = neutral_loss_mz,
                intensity_vec = neutral_loss_intensity,
                status_vec = status_vec,
                confident_only = confident_only,
                aggregation = aggregation)

            if len(centroid_rows) > 0:
                row_chunks.append(centroid_rows)
                col_chunks.append(np.full(len(centroid_rows),
                                          spectrum_id,
                                          dtype = np.int64))
                intensity_chunks.append(collapsed_intensity)
                mz_chunks.append(collapsed_mz)

            for diagnostic_row in current_diagnostic_rows:
                value_id = diagnostic_row.pop("value_id")
                diagnostic_row["spectrum_id"] = int(spectrum_id)
                diagnostic_row["feat_id"] = feat_id
                diagnostic_row["neutral_loss_pair_id"] = int(value_id)
                diagnostic_rows.append(diagnostic_row)

            if return_loss_assignment_df:
                assignment_df = pd.DataFrame({"spectrum_id": int(spectrum_id),
                                              "feat_id": feat_id,
                                              "neutral_loss_pair_id": np.arange(len(neutral_loss_mz), dtype = int),
                                              "neutral_loss_mz": neutral_loss_mz,
                                              "neutral_loss_intensity": neutral_loss_intensity,
                                              "neutral_loss_mz_std": neutral_loss_mz_std,
                                              "fragment_low_id": losses["fragment_low_id"],
                                              "fragment_high_id": losses["fragment_high_id"],
                                              "fragment_low_mz": losses["fragment_low_mz"],
                                              "fragment_high_mz": losses["fragment_high_mz"],
                                              "fragment_low_intensity": losses["fragment_low_intensity"],
                                              "fragment_high_intensity": losses["fragment_high_intensity"],
                                              "assigned_loss_id": assigned_rows,
                                              "assigned_loss_mz": np.where(assigned_rows >= 0,
                                                                           centroid_index["centroid_mz"][np.maximum(assigned_rows, 0)],
                                                                           np.nan),
                                              "assignment_posterior": posterior_vec,
                                              "n_candidate_losses": n_candidates_vec,
                                              "assignment_status": status_vec,
                                              "mz_residual": residual_vec,
                                              "z_score": z_vec})

                assignment_rows.append(assignment_df)

            total_loss_intensity = float(np.sum(neutral_loss_intensity[np.isfinite(neutral_loss_intensity)]))

            assigned_filter = assigned_rows >= 0

            if confident_only:
                assigned_filter = assigned_filter & (status_vec == 2)

            assigned_loss_intensity = float(np.sum(neutral_loss_intensity[assigned_filter])) if len(neutral_loss_intensity) > 0 else 0.0

            if total_loss_intensity > 0:
                assigned_fraction_int = assigned_loss_intensity / total_loss_intensity

            else:
                assigned_fraction_int = np.nan

            summary_rows.append({"spectrum_id": int(spectrum_id),
                                 "feat_id": feat_id,
                                 "status": "ok",
                                 "n_fragments": int(len(fragment_mz)),
                                 "n_neutral_losses": int(len(neutral_loss_mz)),
                                 "n_assigned_losses": int(np.sum(assigned_rows >= 0)),
                                 "n_confident_losses": int(np.sum(status_vec == 2)),
                                 "n_ambiguous_losses": int(np.sum(status_vec == 1)),
                                 "total_loss_intensity": total_loss_intensity,
                                 "assigned_loss_intensity": assigned_loss_intensity,
                                 "assigned_fraction_int": assigned_fraction_int,
                                 "source_file": consensus_spectrum_path.name,
                                 "error_message": ""})

            feature_id_map_rows.append({"spectrum_id": int(spectrum_id),
                                        "feat_id": feat_id,
                                        "consensus_spectrum_file": str(consensus_spectrum_path)})

            spectrum_id += 1

        except Exception as error:
            summary_rows.append({"spectrum_id": np.nan,
                                 "feat_id": feat_id,
                                 "status": "failed",
                                 "n_fragments": 0,
                                 "n_neutral_losses": 0,
                                 "n_assigned_losses": 0,
                                 "n_confident_losses": 0,
                                 "n_ambiguous_losses": 0,
                                 "total_loss_intensity": 0.0,
                                 "assigned_loss_intensity": 0.0,
                                 "assigned_fraction_int": np.nan,
                                 "source_file": Path(consensus_spectrum_path).name,
                                 "error_message": str(error)})

            if not continue_on_error:
                raise

    n_spectra = spectrum_id

    if len(intensity_chunks) == 0:
        aligned_loss_intensity_sparse_mat = csr_matrix((n_centroids, n_spectra), dtype = float)
        aligned_loss_mz_sparse_mat = csr_matrix((n_centroids, n_spectra), dtype = float)

    else:
        rows = np.concatenate(row_chunks)
        cols = np.concatenate(col_chunks)

        aligned_loss_intensity_sparse_mat = coo_matrix((np.concatenate(intensity_chunks),
                                                        (rows, cols)),
                                                       shape = (n_centroids, n_spectra)).tocsr()

        aligned_loss_mz_sparse_mat = coo_matrix((np.concatenate(mz_chunks),
                                                 (rows, cols)),
                                                shape = (n_centroids, n_spectra)).tocsr()

    feature_id_map_df = pd.DataFrame(feature_id_map_rows)
    assignment_summary_df = pd.DataFrame(summary_rows)
    candidate_diagnostic_df = pd.DataFrame(diagnostic_rows)

    if len(assignment_rows) > 0:
        loss_assignment_df = pd.concat(assignment_rows,
                                       axis = 0,
                                       ignore_index = True)

    else:
        loss_assignment_df = pd.DataFrame()

    centroid_diagnostic_df = build_centroid_diagnostic_df(loss_assignment_df = loss_assignment_df,
                                                          centroid_df = centroid_df)

    aligned_loss_mz_vec = centroid_index["centroid_mz"]

    if output_intensity_path is not None:
        write_sparse_alignment_to_wide_csv(aligned_sparse_mat = aligned_loss_intensity_sparse_mat,
                                           aligned_mz_vec = aligned_loss_mz_vec,
                                           feature_id_map_df = feature_id_map_df,
                                           output_path = output_intensity_path,
                                           id_col = "aligned_loss_id",
                                           mz_col = "aligned_loss_mz")

    if output_mz_path is not None:
        write_sparse_alignment_to_wide_csv(aligned_sparse_mat = aligned_loss_mz_sparse_mat,
                                           aligned_mz_vec = aligned_loss_mz_vec,
                                           feature_id_map_df = feature_id_map_df,
                                           output_path = output_mz_path,
                                           id_col = "aligned_loss_id",
                                           mz_col = "aligned_loss_mz")

    if return_wide_df:
        aligned_loss_intensity_df = sparse_alignment_to_wide_df(aligned_sparse_mat = aligned_loss_intensity_sparse_mat,
                                                                aligned_mz_vec = aligned_loss_mz_vec,
                                                                feature_id_map_df = feature_id_map_df,
                                                                id_col = "aligned_loss_id",
                                                                mz_col = "aligned_loss_mz")

        aligned_loss_observed_mz_df = sparse_alignment_to_wide_df(aligned_sparse_mat = aligned_loss_mz_sparse_mat,
                                                                  aligned_mz_vec = aligned_loss_mz_vec,
                                                                  feature_id_map_df = feature_id_map_df,
                                                                  id_col = "aligned_loss_id",
                                                                  mz_col = "aligned_loss_mz")

    else:
        aligned_loss_intensity_df = None
        aligned_loss_observed_mz_df = None

    return {"aligned_loss_intensity_sparse_mat": aligned_loss_intensity_sparse_mat,
            "aligned_loss_mz_sparse_mat": aligned_loss_mz_sparse_mat,
            "aligned_loss_mz_vec": aligned_loss_mz_vec,
            "aligned_loss_intensity_df": aligned_loss_intensity_df,
            "aligned_loss_observed_mz_df": aligned_loss_observed_mz_df,
            "loss_assignment_df": loss_assignment_df,
            "candidate_diagnostic_df": candidate_diagnostic_df,
            "centroid_diagnostic_df": centroid_diagnostic_df,
            "assignment_summary_df": assignment_summary_df,
            "centroid_df": centroid_df,
            "centroid_index": centroid_index,
            "feature_id_map_df": feature_id_map_df,
            "summary_df": assignment_summary_df}
