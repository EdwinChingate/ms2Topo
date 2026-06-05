from __future__ import annotations

from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix
from assign_loaded_consensus_fragments_to_centroids import *
from load_consensus_ms2_spectra_from_folder import *
from sparse_alignment_to_wide_df import *
from write_sparse_alignment_to_wide_csv import *

def align_consensus_spectra_to_fragment_centroids(consensus_spectra_folder,
                                                  clustered_fragments_df,
                                                  selected_feat_ids = None,
                                                  file_name_template = "Consensus_ms2-spectra_{feat_id}.csv",
                                                  mz_col = "median_mz(Da)",
                                                  intensity_col = "median_Int",
                                                  mz_std_col = "IQR_mz(Da)",
                                                  mz_iqr_ppm_col = "IQR_mz(ppm)",
                                                  drop_nonpositive_intensity = True,
                                                  normalization = "l2",
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
                                                  return_loaded_consensus_fragments_df = False,
                                                  output_intensity_path = None,
                                                  output_mz_path = None):
    """
    Align consensus MS2 spectra by assigning observed fragments to an existing
    GMM centroid vocabulary.

    This is the clean centroid-assignment pathway:
        consensus spectra -> fragment assignment -> aligned intensity/mz matrices

    It does not use pseudo_all_ms2 and it does not compute explained_fraction_int.
    The coverage metric is assigned_fraction_int in assignment_summary_df.
    """

    loaded_result = load_consensus_ms2_spectra_from_folder(consensus_spectra_folder = consensus_spectra_folder,
                                                           selected_feat_ids = selected_feat_ids,
                                                           file_name_template = file_name_template,
                                                           mz_col = mz_col,
                                                           intensity_col = intensity_col,
                                                           mz_std_col = mz_std_col,
                                                           mz_iqr_ppm_col = mz_iqr_ppm_col,
                                                           drop_nonpositive_intensity = drop_nonpositive_intensity,
                                                           normalization = normalization,
                                                           continue_on_error = continue_on_error)

    loaded_consensus_fragments_df = loaded_result["loaded_consensus_fragments_df"]
    feature_id_map_df = loaded_result["feature_id_map_df"]
    summary_df = loaded_result["summary_df"]

    if len(loaded_consensus_fragments_df) == 0:
        raise ValueError("No consensus MS2 spectra were loaded. Check summary_df for errors.")

    assignment_result = assign_loaded_consensus_fragments_to_centroids(
        loaded_consensus_fragments_df = loaded_consensus_fragments_df,
        feature_id_map_df = feature_id_map_df,
        clustered_fragments_df = clustered_fragments_df,
        mz_col = mz_col,
        intensity_col = intensity_col,
        mz_std_col = mz_std_col,
        spectrum_id_col = "spectrum_id",
        centroid_mz_col = centroid_mz_col,
        centroid_std_col = centroid_std_col,
        centroid_count_col = centroid_count_col,
        centroid_min_mz_col = centroid_min_mz_col,
        centroid_max_mz_col = centroid_max_mz_col,
        std_distance = std_distance,
        ppm_tol = ppm_tol,
        max_abs_tol = max_abs_tol,
        sigma_floor = sigma_floor,
        prior_power = prior_power,
        use_observed_mz_uncertainty = use_observed_mz_uncertainty,
        min_posterior = min_posterior,
        min_odds_ratio = min_odds_ratio,
        confident_only = confident_only,
        aggregation = aggregation,
        diagnostic_mode = diagnostic_mode)

    aligned_intensity_sparse_mat = assignment_result["aligned_intensity_sparse_mat"]
    aligned_mz_sparse_mat = assignment_result["aligned_mz_sparse_mat"]
    aligned_fragment_mz_vec = assignment_result["aligned_fragment_mz_vec"]

    if output_intensity_path is not None:
        write_sparse_alignment_to_wide_csv(aligned_sparse_mat = aligned_intensity_sparse_mat,
                                           aligned_mz_vec = aligned_fragment_mz_vec,
                                           feature_id_map_df = feature_id_map_df,
                                           output_path = output_intensity_path)

    if output_mz_path is not None:
        write_sparse_alignment_to_wide_csv(aligned_sparse_mat = aligned_mz_sparse_mat,
                                           aligned_mz_vec = aligned_fragment_mz_vec,
                                           feature_id_map_df = feature_id_map_df,
                                           output_path = output_mz_path)

    if return_wide_df:
        aligned_intensity_df = sparse_alignment_to_wide_df(aligned_sparse_mat = aligned_intensity_sparse_mat,
                                                           aligned_mz_vec = aligned_fragment_mz_vec,
                                                           feature_id_map_df = feature_id_map_df)

        aligned_mz_df = sparse_alignment_to_wide_df(aligned_sparse_mat = aligned_mz_sparse_mat,
                                                    aligned_mz_vec = aligned_fragment_mz_vec,
                                                    feature_id_map_df = feature_id_map_df)

    else:
        aligned_intensity_df = None
        aligned_mz_df = None

    result = {"aligned_intensity_sparse_mat": aligned_intensity_sparse_mat,
              "aligned_mz_sparse_mat": aligned_mz_sparse_mat,
              "aligned_fragment_mz_vec": aligned_fragment_mz_vec,
              "aligned_intensity_df": aligned_intensity_df,
              "aligned_mz_df": aligned_mz_df,
              "fragment_assignment_df": assignment_result["fragment_assignment_df"],
              "candidate_diagnostic_df": assignment_result["candidate_diagnostic_df"],
              "collapsed_assignment_df": assignment_result["collapsed_assignment_df"],
              "assignment_summary_df": assignment_result["assignment_summary_df"],
              "centroid_diagnostic_df": assignment_result["centroid_diagnostic_df"],
              "centroid_df": assignment_result["centroid_df"],
              "centroid_index": assignment_result["centroid_index"],
              "feature_id_map_df": feature_id_map_df,
              "summary_df": summary_df}

    if return_loaded_consensus_fragments_df:
        result["loaded_consensus_fragments_df"] = loaded_consensus_fragments_df

    return result
