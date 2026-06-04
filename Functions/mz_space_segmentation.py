from __future__ import annotations

import numpy as np
from neutral_losses_histogram_by_width import *
def mz_space_segmentation(workload_mat,
                          neutral_losses_array,
                          iqr_da_tol = 1e-3,
                          iqr_ppm_tol = 3,
                          bin_width_list = (1e-2, 1e-3),
                          filter_count = 0):
    """
    Recursively segment mz-space until each row is narrow enough.

    Expected table structure:
        table[:, 0] = median mz
        table[:, 1] = count
        table[:, 2] = start index
        table[:, 3] = stop index, exclusive
        table[:, 4] = IQR mz, Da
        table[:, 5] = IQR mz, ppm
    """

    segmented_tables = []

    for row in workload_mat:

        low_id_mz = int(row[2])
        high_id_mz = int(row[3])
        iqr_da = row[4]
        iqr_ppm = row[5]

        resolved_mz_space = ((iqr_da < iqr_da_tol) |
                             (iqr_ppm < iqr_ppm_tol))

        if resolved_mz_space:
            segmented_tables.append(row.reshape(1, -1))
            continue

        neutral_loss_peaks = neutral_losses_histogram_by_width(neutral_losses_array = neutral_losses_array,
                                                               low_id_mz = low_id_mz,
                                                               high_id_mz = high_id_mz,
                                                               bin_width = bin_width_list[filter_count])

        if len(neutral_loss_peaks) == 0:
            segmented_tables.append(row.reshape(1, -1))
            continue

        neutral_loss_peaks = mz_space_segmentation(workload_mat = neutral_loss_peaks,
                                                   neutral_losses_array = neutral_losses_array,
                                                   iqr_da_tol = iqr_da_tol,
                                                   iqr_ppm_tol = iqr_ppm_tol,
                                                   bin_width_list = bin_width_list,
                                                   filter_count = filter_count + 1)

        segmented_tables.append(neutral_loss_peaks)

    neutral_loss_table = np.vstack(segmented_tables)

    neutral_loss_filter = ((neutral_loss_table[:, 4] < iqr_da_tol) |
                           (neutral_loss_table[:, 5] < iqr_ppm_tol))

    return neutral_loss_table[neutral_loss_filter, :]
