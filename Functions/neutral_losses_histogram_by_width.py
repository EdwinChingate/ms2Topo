from __future__ import annotations

import numpy as np
def neutral_losses_histogram_by_width(neutral_losses_array,
                                      low_id_mz,
                                      high_id_mz,
                                      bin_width):
    """
    Build the histogram representation of neutral-loss mz values using
    an explicit mz bin width and a slice from the original neutral-loss vector.

    Expected:
        neutral_losses_array is sorted by mz.
        low_id_mz is inclusive.
        high_id_mz is exclusive.

    Output:
        neutral_loss_peaks[:, 0] = median neutral-loss mz captured by the bin
        neutral_loss_peaks[:, 1] = count
        neutral_loss_peaks[:, 2] = original start index
        neutral_loss_peaks[:, 3] = original stop index, exclusive
        neutral_loss_peaks[:, 4] = number of original neutral losses
        neutral_loss_peaks[:, 5] = IQR mz, Da
        neutral_loss_peaks[:, 6] = IQR mz, ppm
    """

    mz_vec = neutral_losses_array[low_id_mz: high_id_mz]

    mz_vec = np.asarray(mz_vec,
                        dtype = float)

    mz_vec = mz_vec[np.isfinite(mz_vec)]

    if len(mz_vec) == 0:
        return np.zeros((0, 7))

    mz_min = np.min(mz_vec)
    mz_max = np.max(mz_vec)

    if mz_min == mz_max:
        edges = np.array([mz_min - bin_width / 2,
                          mz_max + bin_width / 2])
    else:
        edges = np.arange(mz_min,
                          mz_max + bin_width,
                          bin_width)

    counts, edges = np.histogram(mz_vec,
                                 bins = edges)

    local_start_idx = np.searchsorted(mz_vec,
                                      edges[: -1],
                                      side = "left")

    local_stop_idx = np.searchsorted(mz_vec,
                                     edges[1: ],
                                     side = "left")

    local_stop_idx[-1] = len(mz_vec)

    original_start_idx = low_id_mz + local_start_idx
    original_stop_idx = low_id_mz + local_stop_idx

    median_mz_vec = np.zeros(len(counts))
    iqr_mz_da_vec = np.zeros(len(counts))
    iqr_mz_ppm_vec = np.zeros(len(counts))

    for bin_id in np.arange(len(counts),
                            dtype = int):

        bin_mz_vec = mz_vec[local_start_idx[bin_id]: local_stop_idx[bin_id]]

        if len(bin_mz_vec) > 0:
            median_mz = np.median(bin_mz_vec)

            q1_mz = np.percentile(bin_mz_vec,
                                  25)

            q3_mz = np.percentile(bin_mz_vec,
                                  75)

            iqr_mz_da = q3_mz - q1_mz
            iqr_mz_ppm = iqr_mz_da / median_mz * 1e6

        else:
            median_mz = np.nan
            iqr_mz_da = np.nan
            iqr_mz_ppm = np.nan

        median_mz_vec[bin_id] = median_mz
        iqr_mz_da_vec[bin_id] = iqr_mz_da
        iqr_mz_ppm_vec[bin_id] = iqr_mz_ppm

    neutral_loss_peaks = np.zeros((len(counts), 6))

    neutral_loss_peaks[:, 0] = median_mz_vec
    neutral_loss_peaks[:, 1] = counts
    neutral_loss_peaks[:, 2] = original_start_idx
    neutral_loss_peaks[:, 3] = original_stop_idx
    neutral_loss_peaks[:, 4] = iqr_mz_da_vec
    neutral_loss_peaks[:, 5] = iqr_mz_ppm_vec

    neutral_loss_peaks = neutral_loss_peaks[neutral_loss_peaks[:, 0].argsort(), :]

    return neutral_loss_peaks
