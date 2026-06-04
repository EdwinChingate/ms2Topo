from __future__ import annotations

import numpy as np
def summarize_neutral_loss_index_window(neutral_losses_array,
                                        start_idx,
                                        stop_idx):
    """
    Summarize one contiguous index window using the standard mz table format.

    Output:
        row[0] = median mz
        row[1] = count
        row[2] = start_idx
        row[3] = stop_idx, exclusive
        row[4] = IQR mz, Da
        row[5] = IQR mz, ppm
    """

    mz_vec = neutral_losses_array[start_idx: stop_idx]

    mz_vec = np.asarray(mz_vec,
                        dtype = float)

    mz_vec = mz_vec[np.isfinite(mz_vec)]

    if len(mz_vec) == 0:
        return None

    median_mz = np.median(mz_vec)

    q1_mz = np.percentile(mz_vec,
                          25)

    q3_mz = np.percentile(mz_vec,
                          75)

    iqr_mz_da = q3_mz - q1_mz
    iqr_mz_ppm = iqr_mz_da / median_mz * 1e6

    row = [median_mz,
           len(mz_vec),
           start_idx,
           stop_idx,
           iqr_mz_da,
           iqr_mz_ppm]

    return row
