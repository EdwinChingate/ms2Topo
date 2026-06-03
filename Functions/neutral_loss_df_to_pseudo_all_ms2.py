from __future__ import annotations

import numpy as np

def neutral_loss_df_to_pseudo_all_ms2(neutral_losses_df,
                                      loss_mz_col = "neutral_loss_mz",
                                      loss_std_col = None,
                                      intensity_col = "neutral_loss_intensity",
                                      spectrum_id_col = "spectrum_id",
                                      default_loss_std = 1.0):

    if neutral_losses_df is None or len(neutral_losses_df) == 0:
        return np.array([])

    n_rows = len(neutral_losses_df)

    pseudo_all_ms2 = np.zeros((n_rows,
                               11))

    pseudo_all_ms2[:, 0] = neutral_losses_df[loss_mz_col].to_numpy(float)

    if loss_std_col is None:
        pseudo_all_ms2[:, 1] = default_loss_std
    else:
        pseudo_all_ms2[:, 1] = neutral_losses_df[loss_std_col].to_numpy(float)

    pseudo_all_ms2[:, 9] = neutral_losses_df[intensity_col].to_numpy(float)
    pseudo_all_ms2[:, 10] = neutral_losses_df[spectrum_id_col].astype(int).to_numpy()

    return pseudo_all_ms2
