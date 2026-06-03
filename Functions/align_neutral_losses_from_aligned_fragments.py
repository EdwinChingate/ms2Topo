from __future__ import annotations

from AlignFragmentsEngine import *
from aligned_neutral_loss_matrices_to_dataframes import *
from neutral_loss_df_to_pseudo_all_ms2 import *
from neutral_losses_from_aligned_fragments import *

def align_neutral_losses_from_aligned_fragments(aligned_intensity_df,
                                                aligned_mz_df = None,
                                                feature_cols = None,
                                                aligned_fragment_mz_col = "aligned_fragment_mz",
                                                min_neutral_loss = 18.0,
                                                max_neutral_loss = None,
                                                min_fragment_intensity = 0,
                                                pair_intensity = "min",
                                                default_loss_std = 1.0,
                                                intensity_to_explain = 1.0,
                                                min_spectra = 1):

    neutral_loss_result = neutral_losses_from_aligned_fragments(aligned_intensity_df = aligned_intensity_df,
                                                                aligned_mz_df = aligned_mz_df,
                                                                feature_cols = feature_cols,
                                                                aligned_fragment_mz_col = aligned_fragment_mz_col,
                                                                min_neutral_loss = min_neutral_loss,
                                                                max_neutral_loss = max_neutral_loss,
                                                                min_fragment_intensity = min_fragment_intensity,
                                                                pair_intensity = pair_intensity)

    neutral_losses_df = neutral_loss_result["neutral_losses_df"]
    feature_id_map_df = neutral_loss_result["feature_id_map_df"]

    if len(neutral_losses_df) == 0:
        raise ValueError("No neutral losses were inferred from the aligned fragments.")

    pseudo_all_ms2 = neutral_loss_df_to_pseudo_all_ms2(neutral_losses_df = neutral_losses_df,
                                                       loss_mz_col = "neutral_loss_mz",
                                                       intensity_col = "neutral_loss_intensity",
                                                       spectrum_id_col = "spectrum_id",
                                                       default_loss_std = default_loss_std)

    aligned_neutral_losses_mat, aligned_neutral_losses_mz_mat, explained_fraction_int, n_features = AlignFragmentsEngine(all_ms2 = pseudo_all_ms2,
                                                                                                                        Intensity_to_explain = intensity_to_explain,
                                                                                                                        min_spectra = min_spectra)

    table_result = aligned_neutral_loss_matrices_to_dataframes(aligned_neutral_losses_mat = aligned_neutral_losses_mat,
                                                               aligned_neutral_losses_mz_mat = aligned_neutral_losses_mz_mat,
                                                               feature_id_map_df = feature_id_map_df)

    return {"aligned_neutral_losses_mat": aligned_neutral_losses_mat,
            "aligned_neutral_losses_mz_mat": aligned_neutral_losses_mz_mat,
            "aligned_neutral_loss_intensity_df": table_result["aligned_neutral_loss_intensity_df"],
            "aligned_neutral_loss_mz_df": table_result["aligned_neutral_loss_mz_df"],
            "aligned_neutral_losses_long_df": table_result["aligned_neutral_losses_long_df"],
            "explained_fraction_int": explained_fraction_int,
            "n_features": n_features,
            "pseudo_all_ms2": pseudo_all_ms2,
            "neutral_losses_df": neutral_losses_df,
            "feature_id_map_df": feature_id_map_df}
