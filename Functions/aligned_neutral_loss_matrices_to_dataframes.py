from __future__ import annotations

import numpy as np
import pandas as pd

def aligned_neutral_loss_matrices_to_dataframes(aligned_neutral_losses_mat,
                                                aligned_neutral_losses_mz_mat,
                                                feature_id_map_df,
                                                feature_col = "feature_col"):

    feature_cols = feature_id_map_df.sort_values("spectrum_id")[feature_col].tolist()

    output_cols = ["aligned_neutral_loss_mz"] + feature_cols

    aligned_neutral_loss_intensity_df = pd.DataFrame(aligned_neutral_losses_mat,
                                                     columns = output_cols)

    aligned_neutral_loss_mz_df = pd.DataFrame(aligned_neutral_losses_mz_mat,
                                              columns = output_cols)

    long_rows = []

    for spectrum_id, current_feature_col in enumerate(feature_cols):
        matrix_col_id = spectrum_id + 1

        present_loc = aligned_neutral_losses_mat[:, matrix_col_id] > 0

        if np.sum(present_loc) == 0:
            continue

        current_df = pd.DataFrame({"neutral_loss_cluster_id": np.where(present_loc)[0],
                                   "feature_col": current_feature_col,
                                   "spectrum_id": int(spectrum_id),
                                   "aligned_neutral_loss_mz": aligned_neutral_losses_mat[present_loc, 0],
                                   "observed_neutral_loss_mz": aligned_neutral_losses_mz_mat[present_loc, matrix_col_id],
                                   "neutral_loss_intensity": aligned_neutral_losses_mat[present_loc, matrix_col_id]})

        long_rows.append(current_df)

    if len(long_rows) == 0:
        aligned_neutral_losses_long_df = pd.DataFrame()
    else:
        aligned_neutral_losses_long_df = pd.concat(long_rows,
                                                   ignore_index = True)

    return {"aligned_neutral_loss_intensity_df": aligned_neutral_loss_intensity_df,
            "aligned_neutral_loss_mz_df": aligned_neutral_loss_mz_df,
            "aligned_neutral_losses_long_df": aligned_neutral_losses_long_df}
