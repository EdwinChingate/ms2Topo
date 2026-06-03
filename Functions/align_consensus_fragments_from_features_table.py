from __future__ import annotations

from AlignFragmentsEngine import *
from aligned_matrices_to_dataframes import *
from consensus_df_to_pseudo_all_ms2 import *
from load_consensus_ms2_spectra_from_features_table import *

def align_consensus_fragments_from_features_table(features_table_df,
                                                  consensus_spectra_folder,
                                                  feat_id_col = "feat_id",
                                                  selected_feat_ids = None,
                                                  file_name_template = "Consensus_ms2-spectra_{feat_id}.csv",
                                                  mz_col = "median_mz(Da)",
                                                  intensity_col = "median_Int",
                                                  mz_std_col = "IQR_mz(Da)",
                                                  mz_iqr_ppm_col = "IQR_mz(ppm)",
                                                  drop_nonpositive_intensity = True,
                                                  normalization = "l2",
                                                  intensity_to_explain = 1.0,
                                                  min_spectra = 1,
                                                  continue_on_error = True):
    """
    Retrieve saved consensus spectra by feat_id and align their fragments.

    This function reuses:
        consensus_df_to_pseudo_all_ms2
        AlignFragmentsEngine
    """

    loaded_result = load_consensus_ms2_spectra_from_features_table(features_table_df = features_table_df,
                                                                   consensus_spectra_folder = consensus_spectra_folder,
                                                                   feat_id_col = feat_id_col,
                                                                   selected_feat_ids = selected_feat_ids,
                                                                   file_name_template = file_name_template,
                                                                   mz_col = mz_col,
                                                                   intensity_col = intensity_col,
                                                                   mz_std_col = mz_std_col,
                                                                   mz_iqr_ppm_col = mz_iqr_ppm_col,
                                                                   drop_nonpositive_intensity = drop_nonpositive_intensity,
                                                                   normalization = normalization,
                                                                   continue_on_error = continue_on_error)

    all_consensus_ms2_df = loaded_result["all_consensus_ms2_df"]
    summary_df = loaded_result["summary_df"]
    feature_id_map_df = loaded_result["feature_id_map_df"]

    if len(all_consensus_ms2_df) == 0:
        raise ValueError("No consensus MS2 spectra were loaded. Check summary_df for errors.")

    pseudo_all_ms2 = consensus_df_to_pseudo_all_ms2(consensus_spectra_df = all_consensus_ms2_df,
                                                    mz_col = mz_col,
                                                    mz_std_col = mz_std_col,
                                                    intensity_col = intensity_col,
                                                    spectrum_id_col = "spectrum_id")

    aligned_fragments_mat, aligned_fragments_mz_mat, explained_fraction_int, n_features = AlignFragmentsEngine(all_ms2 = pseudo_all_ms2,
                                                                                                               Intensity_to_explain = intensity_to_explain,
                                                                                                               min_spectra = min_spectra)

    table_result = aligned_matrices_to_dataframes(aligned_fragments_mat = aligned_fragments_mat,
                                                  aligned_fragments_mz_mat = aligned_fragments_mz_mat,
                                                  feature_id_map_df = feature_id_map_df)

    return {"aligned_fragments_mat": aligned_fragments_mat,
            "aligned_fragments_mz_mat": aligned_fragments_mz_mat,
            "aligned_intensity_df": table_result["aligned_intensity_df"],
            "aligned_mz_df": table_result["aligned_mz_df"],
            "aligned_fragments_long_df": table_result["aligned_fragments_long_df"],
            "explained_fraction_int": explained_fraction_int,
            "n_features": n_features,
            "pseudo_all_ms2": pseudo_all_ms2,
            "all_consensus_ms2_df": all_consensus_ms2_df,
            "feature_id_map_df": feature_id_map_df,
            "summary_df": summary_df}
