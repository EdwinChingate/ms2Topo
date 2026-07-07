# Extracted from notebook: 713031fb-407a-42c5-b338-3c1aba9bdf96.ipynb
# One unique top-level function per file. Auto-generated from top-level function definitions.
from __future__ import annotations
import numpy as np
from assign_loaded_consensus_fragments_to_centroids import assign_loaded_consensus_fragments_to_centroids
from sparse_alignment_to_wide_df import sparse_alignment_to_wide_df
from write_sparse_alignment_to_wide_csv import write_sparse_alignment_to_wide_csv
from add_neutral_loss_global_summary_aliases import add_neutral_loss_global_summary_aliases
from load_consensus_neutral_losses_from_folder import load_consensus_neutral_losses_from_folder
from rename_neutral_loss_assignment_columns import rename_neutral_loss_assignment_columns


def align_consensus_spectra_to_neutral_loss_centroids(consensus_spectra_folder,
                                                       clustered_neutral_losses_df,
                                                       selected_feat_ids = None,
                                                       file_name_template = "Consensus_ms2-spectra_{feat_id}.csv",
                                                       mz_col = "median_mz(Da)",
                                                       intensity_col = "median_Int",
                                                       mz_std_col = "IQR_mz(Da)",
                                                       mz_iqr_ppm_col = "IQR_mz(ppm)",
                                                       min_mz_col = "min_mz(Da)",
                                                       max_mz_col = "max_mz(Da)",
                                                       min_source_fragment_intensity = 0.0,
                                                       min_neutral_loss = 18.0,
                                                       max_neutral_loss = None,
                                                       neutral_loss_iqr_rule = "max_fragment_iqr",
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
                                                       diagnostic_mode = "ambiguous",
                                                       print_assignment_report = True,
                                                       return_wide_df = False,
                                                       return_loaded_neutral_losses_df = False,
                                                       output_presence_path = None,
                                                       output_mz_path = None):
    """
    Align generated neutral losses from consensus MS2 spectra to a neutral-loss
    centroid vocabulary.

    This function is intentionally separate from
    align_consensus_spectra_to_fragment_centroids. Fragments are directly read
    from consensus spectra and yield an intensity matrix. Neutral losses are
    generated from fragment pairs and yield a presence/absence matrix.

    Output matrix semantics:
        rows    = aligned neutral-loss centroids
        columns = consensus spectra / feat_id
        values  = 1 if one or more fragment pairs in the consensus spectrum
                  were assigned to the neutral-loss centroid, else 0
    """

    loaded_result = load_consensus_neutral_losses_from_folder(consensus_spectra_folder = consensus_spectra_folder,
                                                              selected_feat_ids = selected_feat_ids,
                                                              file_name_template = file_name_template,
                                                              mz_col = mz_col,
                                                              intensity_col = intensity_col,
                                                              mz_std_col = mz_std_col,
                                                              mz_iqr_ppm_col = mz_iqr_ppm_col,
                                                              min_mz_col = min_mz_col,
                                                              max_mz_col = max_mz_col,
                                                              min_source_fragment_intensity = min_source_fragment_intensity,
                                                              min_neutral_loss = min_neutral_loss,
                                                              max_neutral_loss = max_neutral_loss,
                                                              neutral_loss_iqr_rule = neutral_loss_iqr_rule,
                                                              continue_on_error = continue_on_error)

    loaded_neutral_losses_df = loaded_result["loaded_consensus_fragments_df"]
    feature_id_map_df = loaded_result["feature_id_map_df"]
    summary_df = loaded_result["summary_df"]

    if len(loaded_neutral_losses_df) == 0:
        raise ValueError("No neutral-loss observations were generated. Check summary_df for failed or empty spectra.")

    assignment_result = assign_loaded_consensus_fragments_to_centroids(
        loaded_consensus_fragments_df = loaded_neutral_losses_df,
        feature_id_map_df = feature_id_map_df,
        clustered_fragments_df = clustered_neutral_losses_df,
        mz_col = "neutral_loss_mz",
        intensity_col = "neutral_loss_presence",
        mz_std_col = "neutral_loss_iqr_da",
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
        aggregation = "max",
        diagnostic_mode = diagnostic_mode)

    aligned_presence_sparse_mat = assignment_result["aligned_intensity_sparse_mat"].copy()

    if aligned_presence_sparse_mat.nnz > 0:
        aligned_presence_sparse_mat.data[:] = 1.0

    aligned_neutral_loss_mz_sparse_mat = assignment_result["aligned_mz_sparse_mat"]
    aligned_neutral_loss_mz_vec = assignment_result["aligned_fragment_mz_vec"]

    neutral_loss_assignment_df = rename_neutral_loss_assignment_columns(assignment_result["fragment_assignment_df"])
    unassigned_neutral_loss_df = rename_neutral_loss_assignment_columns(assignment_result["unassigned_fragment_df"])
    candidate_diagnostic_df = assignment_result["candidate_diagnostic_df"].copy()
    collapsed_presence_df = assignment_result["collapsed_assignment_df"].copy()

    if len(collapsed_presence_df) > 0:
        collapsed_presence_df = collapsed_presence_df.rename(columns = {"aligned_fragment_id": "aligned_neutral_loss_id",
                                                                        "aligned_fragment_mz": "aligned_neutral_loss_mz",
                                                                        "aligned_intensity": "aligned_presence"})
        collapsed_presence_df["aligned_presence"] = 1.0

    neutral_loss_summary_df = assignment_result["assignment_summary_df"].copy()
    neutral_loss_global_summary_df = add_neutral_loss_global_summary_aliases(assignment_result["assignment_global_summary_df"])

    if print_assignment_report:
        report_row = neutral_loss_global_summary_df.iloc[0]

        raw_total = int(summary_df["n_raw_fragment_rows"].sum()) if "n_raw_fragment_rows" in summary_df.columns else np.nan
        source_total = int(summary_df["n_source_fragments_for_neutral_losses"].sum()) if "n_source_fragments_for_neutral_losses" in summary_df.columns else np.nan
        generated_total = int(summary_df["n_generated_neutral_losses"].sum()) if "n_generated_neutral_losses" in summary_df.columns else np.nan
        assigned_total = int(report_row["n_assigned_neutral_losses"])
        unassigned_total = int(report_row["n_unassigned_neutral_losses"])
        no_candidate_total = int(report_row["n_neutral_losses_with_no_candidate_centroid"])

        print("Consensus MS2 neutral-loss assignment report")
        print(f"  Raw fragment rows read: {raw_total}")
        print(f"  Source fragments used for neutral-loss generation: {source_total}")
        print(f"  Neutral-loss observations generated: {generated_total}")
        print(f"  Neutral-loss observations tested against centroids: {int(report_row['n_generated_neutral_losses_tested'])}")
        print(f"  Assigned neutral-loss observations: {assigned_total}")
        print(f"  Unassigned neutral-loss observations: {unassigned_total}")
        print(f"  Neutral losses with no candidate centroid in the m/z window: {no_candidate_total}")
        print(f"  Assigned fraction by neutral-loss count: {report_row['assigned_fraction_fragments']:.6f}")
        print("  Aligned value type: presence_absence")

        if bool(report_row["all_neutral_losses_assigned"]):
            print("  OK: all generated neutral-loss observations were assigned to a centroid.")

        else:
            print("  WARNING: some generated neutral-loss observations did not match any centroid.")
            print("  Inspect result['unassigned_neutral_loss_df'] for the unmatched neutral losses.")

    if output_presence_path is not None:
        write_sparse_alignment_to_wide_csv(aligned_sparse_mat = aligned_presence_sparse_mat,
                                           aligned_mz_vec = aligned_neutral_loss_mz_vec,
                                           feature_id_map_df = feature_id_map_df,
                                           output_path = output_presence_path,
                                           id_col = "aligned_neutral_loss_id",
                                           mz_col = "aligned_neutral_loss_mz")

    if output_mz_path is not None:
        write_sparse_alignment_to_wide_csv(aligned_sparse_mat = aligned_neutral_loss_mz_sparse_mat,
                                           aligned_mz_vec = aligned_neutral_loss_mz_vec,
                                           feature_id_map_df = feature_id_map_df,
                                           output_path = output_mz_path,
                                           id_col = "aligned_neutral_loss_id",
                                           mz_col = "aligned_neutral_loss_mz")

    if return_wide_df:
        aligned_presence_df = sparse_alignment_to_wide_df(aligned_sparse_mat = aligned_presence_sparse_mat,
                                                          aligned_mz_vec = aligned_neutral_loss_mz_vec,
                                                          feature_id_map_df = feature_id_map_df,
                                                          id_col = "aligned_neutral_loss_id",
                                                          mz_col = "aligned_neutral_loss_mz")

        aligned_neutral_loss_mz_df = sparse_alignment_to_wide_df(aligned_sparse_mat = aligned_neutral_loss_mz_sparse_mat,
                                                                 aligned_mz_vec = aligned_neutral_loss_mz_vec,
                                                                 feature_id_map_df = feature_id_map_df,
                                                                 id_col = "aligned_neutral_loss_id",
                                                                 mz_col = "aligned_neutral_loss_mz")

    else:
        aligned_presence_df = None
        aligned_neutral_loss_mz_df = None

    result = {"aligned_presence_sparse_mat": aligned_presence_sparse_mat,
              "aligned_neutral_loss_mz_sparse_mat": aligned_neutral_loss_mz_sparse_mat,
              "aligned_neutral_loss_mz_vec": aligned_neutral_loss_mz_vec,
              "aligned_presence_df": aligned_presence_df,
              "aligned_neutral_loss_mz_df": aligned_neutral_loss_mz_df,
              "neutral_loss_assignment_df": neutral_loss_assignment_df,
              "unassigned_neutral_loss_df": unassigned_neutral_loss_df,
              "candidate_diagnostic_df": candidate_diagnostic_df,
              "collapsed_presence_df": collapsed_presence_df,
              "neutral_loss_summary_df": neutral_loss_summary_df,
              "neutral_loss_global_summary_df": neutral_loss_global_summary_df,
              "centroid_diagnostic_df": assignment_result["centroid_diagnostic_df"],
              "centroid_df": assignment_result["centroid_df"],
              "centroid_index": assignment_result["centroid_index"],
              "feature_id_map_df": feature_id_map_df,
              "summary_df": summary_df}

    if return_loaded_neutral_losses_df:
        result["loaded_neutral_losses_df"] = loaded_neutral_losses_df

    return result
