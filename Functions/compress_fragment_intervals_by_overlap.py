from __future__ import annotations

import numpy as np
import pandas as pd

def compress_fragment_intervals_by_overlap(all_fragment_mz_table,
                                           mz_col = 4,
                                           min_mz_col = 6,
                                           max_mz_col = 7,
                                           min_counts = 3,
                                           max_gap = 0,
                                           return_segment_map = True):
    """
    Compress fragment m/z intervals into overlapping m/z segments.

    Expected:
        all_fragment_mz_table contains one row per fragment observation.

    Required columns:
        mz_col      -> representative fragment m/z
        min_mz_col  -> lower m/z interval edge
        max_mz_col  -> upper m/z interval edge

    Output:
        compressed_table[:, 0] = median mz of collapsed segment
        compressed_table[:, 1] = count
        compressed_table[:, 2] = start index in sorted interval table
        compressed_table[:, 3] = stop index in sorted interval table, exclusive
        compressed_table[:, 4] = IQR mz, Da
        compressed_table[:, 5] = IQR mz, ppm
        compressed_table[:, 6] = segment min mz
        compressed_table[:, 7] = segment max mz

        segment_map_df:
            map between original rows and compressed segment ids.
    """

    if isinstance(all_fragment_mz_table, pd.DataFrame):

        table = all_fragment_mz_table.to_numpy()

    else:

        table = np.asarray(all_fragment_mz_table)

    if len(table) == 0:
        return {"compressed_table": np.zeros((0, 8)),
                "segment_map_df": pd.DataFrame()}

    mz_vec = table[:, mz_col].astype(float)
    interval_left_vec = table[:, min_mz_col].astype(float)
    interval_right_vec = table[:, max_mz_col].astype(float)

    interval_min_vec = np.minimum(interval_left_vec,
                                  interval_right_vec)

    interval_max_vec = np.maximum(interval_left_vec,
                                  interval_right_vec)

    good_rows = (np.isfinite(mz_vec) &
                 np.isfinite(interval_min_vec) &
                 np.isfinite(interval_max_vec) &
                 (interval_max_vec >= interval_min_vec))

    if np.sum(good_rows) == 0:
        return {"compressed_table": np.zeros((0, 8)),
                "segment_map_df": pd.DataFrame()}

    original_row_ids = np.where(good_rows)[0]

    mz_vec = mz_vec[good_rows]
    interval_min_vec = interval_min_vec[good_rows]
    interval_max_vec = interval_max_vec[good_rows]

    interval_order = np.argsort(interval_min_vec)

    mz_vec = mz_vec[interval_order]
    interval_min_vec = interval_min_vec[interval_order]
    interval_max_vec = interval_max_vec[interval_order]
    original_row_ids = original_row_ids[interval_order]

    compressed_rows = []
    segment_map_rows = []

    segment_id = 0
    row_id = 0
    n_rows = len(mz_vec)

    while row_id < n_rows:

        segment_start_row = row_id
        segment_min_mz = interval_min_vec[row_id]
        segment_max_mz = interval_max_vec[row_id]

        row_id += 1

        while row_id < n_rows and interval_min_vec[row_id] <= segment_max_mz + max_gap:

            if interval_max_vec[row_id] > segment_max_mz:
                segment_max_mz = interval_max_vec[row_id]

            row_id += 1

        segment_stop_row = row_id

        segment_mz_vec = mz_vec[segment_start_row: segment_stop_row]
        segment_original_rows = original_row_ids[segment_start_row: segment_stop_row]

        segment_mz_vec = segment_mz_vec[np.isfinite(segment_mz_vec)]

        if len(segment_mz_vec) < min_counts:
            continue

        median_mz = np.median(segment_mz_vec)

        q1_mz = np.percentile(segment_mz_vec,
                              25)

        q3_mz = np.percentile(segment_mz_vec,
                              75)

        iqr_mz_da = q3_mz - q1_mz

        if median_mz != 0:
            iqr_mz_ppm = iqr_mz_da / median_mz * 1e6

        else:
            iqr_mz_ppm = np.nan

        compressed_rows.append([median_mz,
                                len(segment_mz_vec),
                                segment_start_row,
                                segment_stop_row,
                                iqr_mz_da,
                                iqr_mz_ppm,
                                segment_min_mz,
                                segment_max_mz])

        if return_segment_map:

            for original_row_id in segment_original_rows:
                segment_map_rows.append({"original_row_id": int(original_row_id),
                                         "compressed_fragment_id": int(segment_id),
                                         "compressed_fragment_mz": float(median_mz),
                                         "segment_min_mz": float(segment_min_mz),
                                         "segment_max_mz": float(segment_max_mz)})

        segment_id += 1

    if len(compressed_rows) == 0:
        compressed_table = np.zeros((0, 8))

    else:
        compressed_table = np.array(compressed_rows,
                                    dtype = float)

        compressed_table = compressed_table[compressed_table[:, 0].argsort(), :]

    if return_segment_map:
        segment_map_df = pd.DataFrame(segment_map_rows)

    else:
        segment_map_df = pd.DataFrame()

    return {"compressed_table": compressed_table,
            "segment_map_df": segment_map_df}
