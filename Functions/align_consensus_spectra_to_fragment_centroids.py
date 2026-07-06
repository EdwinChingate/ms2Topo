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
from assign_loaded_consensus_fragments_to_centroids import assign_loaded_consensus_fragments_to_centroids
from load_consensus_ms2_spectra_from_folder import load_consensus_ms2_spectra_from_folder
from sparse_alignment_to_wide_df import sparse_alignment_to_wide_df
from write_sparse_alignment_to_wide_csv import write_sparse_alignment_to_wide_csv


def align_consensus_spectra_to_fragment_centroids(consensus_spectra_folder,
                                                  clustered_fragments_df,
                                                  selected_feat_ids = None,
                                                  file_name_template = "Consensus_ms2-spectra_{feat_id}.csv",
                                                  mz_col = "median_mz(Da)",
                                                  intensity_col = "median_Int",
                                                  mz_std_col = "IQR_mz(Da)",
                                                  mz_iqr_ppm_col = "IQR_mz(ppm)",
                                                  drop_nonpositive_intensity = True,
                                                  min_fragment_intensity = 0.0,
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
                                                  max_z_score = 3.0,
                                                  min_z_score_gap = 0.5,
                                                  confident_only = False,
                                                  aggregation = "max",
                                                  diagnostic_mode = "ambiguous",
                                                  print_assignment_report = True,
                                                  return_wide_df = False,
                                                  return_loaded_consensus_fragments_df = False,
                                                  output_intensity_path = None,
                                                  output_mz_path = None):
    """
    Align consensus MS2 spectra by assigning observed positive-intensity
    fragments to an existing centroid vocabulary.

    This is the clean centroid-assignment pathway:
        consensus spectra -> nonzero intensity filter -> fragment assignment
        -> aligned intensity/mz matrices

    The default input filter keeps only fragments with median_Int > 0 before
    assignment. The returned summary tables report whether all loaded nonzero
    fragments found at least one centroid match.
    """

    loaded_result = load_consensus_ms2_spectra_from_folder(consensus_spectra_folder = consensus_spectra_folder,
                                                           selected_feat_ids = selected_feat_ids,
                                                           file_name_template = file_name_template,
                                                           mz_col = mz_col,
                                                           intensity_col = intensity_col,
                                                           mz_std_col = mz_std_col,
                                                           mz_iqr_ppm_col = mz_iqr_ppm_col,
                                                           drop_nonpositive_intensity = drop_nonpositive_intensity,
                                                           min_fragment_intensity = min_fragment_intensity,
                                                           normalization = normalization,
                                                           continue_on_error = continue_on_error)

    loaded_consensus_fragments_df = loaded_result["loaded_consensus_fragments_df"]
    feature_id_map_df = loaded_result["feature_id_map_df"]
    summary_df = loaded_result["summary_df"]

    if len(loaded_consensus_fragments_df) == 0:
        raise ValueError("No consensus MS2 spectra were loaded after the positive-intensity filter. Check summary_df for errors or empty_after_filter spectra.")

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
        max_z_score = max_z_score,
        min_z_score_gap = min_z_score_gap,
        confident_only = confident_only,
        aggregation = aggregation,
        diagnostic_mode = diagnostic_mode)

    aligned_intensity_sparse_mat = assignment_result["aligned_intensity_sparse_mat"]
    aligned_mz_sparse_mat = assignment_result["aligned_mz_sparse_mat"]
    aligned_fragment_mz_vec = assignment_result["aligned_fragment_mz_vec"]
    assignment_global_summary_df = assignment_result["assignment_global_summary_df"]
    unassigned_fragment_df = assignment_result["unassigned_fragment_df"]

    if print_assignment_report:
        report_row = assignment_global_summary_df.iloc[0]

        raw_total = int(summary_df.get("n_raw_fragment_rows", pd.Series(dtype = float)).sum()) if "n_raw_fragment_rows" in summary_df.columns else np.nan
        missing_mz_total = int(summary_df.get("n_missing_mz_fragments", pd.Series(dtype = float)).sum()) if "n_missing_mz_fragments" in summary_df.columns else np.nan
        missing_intensity_total = int(summary_df.get("n_missing_intensity_fragments", pd.Series(dtype = float)).sum()) if "n_missing_intensity_fragments" in summary_df.columns else np.nan
        intensity_filtered_total = int(summary_df.get("n_fragments_filtered_by_intensity", pd.Series(dtype = float)).sum()) if "n_fragments_filtered_by_intensity" in summary_df.columns else np.nan
        loaded_total = int(report_row["n_loaded_positive_intensity_fragments"])
        assigned_total = int(report_row["n_assigned_fragments"])
        unassigned_total = int(report_row["n_unassigned_fragments"])
        no_candidate_total = int(report_row["n_no_candidate_fragments"])

        print("Consensus MS2 fragment assignment report")
        print(f"  Raw fragment rows read: {raw_total}")
        print(f"  Removed because m/z was missing/non-numeric: {missing_mz_total}")
        print(f"  Removed because intensity was missing/non-numeric: {missing_intensity_total}")
        print(f"  Removed by intensity filter ({intensity_col} > {min_fragment_intensity}): {intensity_filtered_total}")
        print(f"  Positive-intensity fragments tested against centroids: {loaded_total}")
        print(f"  Assigned fragments: {assigned_total}")
        print(f"  Unassigned fragments: {unassigned_total}")
        print(f"  Fragments with no candidate centroid in the m/z window: {no_candidate_total}")
        print(f"  Assigned fraction by fragment count: {report_row['assigned_fraction_fragments']:.6f}")
        print(f"  Assigned fraction by normalized intensity: {report_row['assigned_fraction_intensity']:.6f}")

        if bool(report_row["all_positive_intensity_fragments_assigned"]):
            print("  OK: all loaded positive-intensity fragments were assigned to a centroid.")

        else:
            print("  WARNING: some loaded positive-intensity fragments did not match any centroid.")
            print("  Inspect result['unassigned_fragment_df'] for the unmatched fragments.")

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
              "unassigned_fragment_df": unassigned_fragment_df,
              "candidate_diagnostic_df": assignment_result["candidate_diagnostic_df"],
              "collapsed_assignment_df": assignment_result["collapsed_assignment_df"],
              "assignment_summary_df": assignment_result["assignment_summary_df"],
              "assignment_global_summary_df": assignment_global_summary_df,
              "centroid_diagnostic_df": assignment_result["centroid_diagnostic_df"],
              "centroid_df": assignment_result["centroid_df"],
              "centroid_index": assignment_result["centroid_index"],
              "feature_id_map_df": feature_id_map_df,
              "summary_df": summary_df}

    if return_loaded_consensus_fragments_df:
        result["loaded_consensus_fragments_df"] = loaded_consensus_fragments_df

    return result
