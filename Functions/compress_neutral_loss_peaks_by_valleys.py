from __future__ import annotations

import numpy as np
def compress_neutral_loss_peaks_by_valleys(neutral_loss_peaks,
                                           neutral_losses_array,
                                           cols,
                                           min_counts = 3):
    """
    Compress adjacent histogram rows into mz segments using low-count rows
    as valleys.

    A row is considered part of a segment when:

        count >= valley_count_threshold

    Consecutive segment rows are collapsed.

    Output:
        compressed_table[:, 0] = median mz of collapsed segment
        compressed_table[:, 1] = count
        compressed_table[:, 2] = start index
        compressed_table[:, 3] = stop index, exclusive
        compressed_table[:, 4] = IQR mz, Da
        compressed_table[:, 5] = IQR mz, ppm
    """

    neutral_loss_peaks = np.asarray(neutral_loss_peaks,
                                    dtype = float)

    if len(neutral_loss_peaks) == 0:
        return np.zeros((0, 6))

    count_col = cols["count"]
    start_col = cols["start_idx"]
    stop_col = cols["stop_idx"]

    signal_row = neutral_loss_peaks[:, count_col] >= min_counts

    compressed_rows = []
    row_id = 0

    while row_id < len(neutral_loss_peaks):

        if not signal_row[row_id]:
            row_id += 1
            continue

        segment_start_row = row_id

        while row_id < len(neutral_loss_peaks) and signal_row[row_id]:
            row_id += 1

        segment_stop_row = row_id - 1

        start_idx = int(neutral_loss_peaks[segment_start_row, start_col])
        stop_idx = int(neutral_loss_peaks[segment_stop_row, stop_col])

        segment_mz_vec = neutral_losses_array[start_idx: stop_idx]

        segment_mz_vec = np.asarray(segment_mz_vec,
                                    dtype = float)

        segment_mz_vec = segment_mz_vec[np.isfinite(segment_mz_vec)]

        median_mz = np.median(segment_mz_vec)

        q1_mz = np.percentile(segment_mz_vec,
                              25)

        q3_mz = np.percentile(segment_mz_vec,
                              75)

        iqr_mz_da = q3_mz - q1_mz
        iqr_mz_ppm = iqr_mz_da / median_mz * 1e6

        compressed_rows.append([median_mz,
                                len(segment_mz_vec),
                                start_idx,
                                stop_idx,
                                iqr_mz_da,
                                iqr_mz_ppm])

    if len(compressed_rows) == 0:
        return np.zeros((0, 6))

    compressed_table = np.array(compressed_rows,
                                dtype = float)

    compressed_table = compressed_table[compressed_table[:, 0].argsort(), :]

    return compressed_table
