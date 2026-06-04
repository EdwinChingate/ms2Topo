from __future__ import annotations

import numpy as np
def WorkLoadPlanning_uniform_mz(mz_vec,
                                mz_interval = 2,
                                mz_Tol = 2e-3,
                                snap_to_valleys = True,
                                max_shift_fraction = 0.15,
                                min_batch_size = 1):
    """
    Plan workload batches using approximately uniform mz intervals.

    Expected:
        mz_vec is sorted by mz.

    Output:
        workload_mat[:, 0] = median mz captured by the workload batch
        workload_mat[:, 1] = count
        workload_mat[:, 2] = start index
        workload_mat[:, 3] = stop index, exclusive
        workload_mat[:, 4] = IQR mz, Da
        workload_mat[:, 5] = IQR mz, ppm
    """

    mz_vec = np.asarray(mz_vec,
                        dtype = float)

    mz_vec = mz_vec[np.isfinite(mz_vec)]

    n_values = len(mz_vec)

    if n_values == 0:
        return np.zeros((0, 6))

    if mz_interval <= 0:
        raise ValueError("mz_interval must be > 0")

    mz_min = np.min(mz_vec)
    mz_max = np.max(mz_vec)

    target_mz_edges = np.arange(mz_min,
                                mz_max + mz_interval,
                                mz_interval)

    if target_mz_edges[-1] < mz_max:
        target_mz_edges = np.append(target_mz_edges,
                                    mz_max)

    target_mz_edges[-1] = mz_max

    target_edges = np.searchsorted(mz_vec,
                                   target_mz_edges,
                                   side = "left")

    target_edges[0] = 0
    target_edges[-1] = n_values

    target_edges = np.unique(target_edges)

    target_cuts = target_edges[1: -1]
    n_batches = len(target_edges) - 1

    max_shift_mz = mz_interval * max_shift_fraction

    if snap_to_valleys:
        dif_vec = mz_vec[1: ] - mz_vec[: -1]
        valley_cuts = np.where(dif_vec > mz_Tol)[0] + 1

        selected_cuts = []
        previous_cut = 0

        for cut_id, target_cut in enumerate(target_cuts):

            target_mz = mz_vec[target_cut]
            remaining_batches = n_batches - cut_id - 1

            lowest_allowed = previous_cut + min_batch_size
            highest_allowed = n_values - remaining_batches * min_batch_size

            candidate_cuts = valley_cuts[(valley_cuts >= lowest_allowed) &
                                         (valley_cuts <= highest_allowed)]

            if len(candidate_cuts) > 0:
                candidate_mz = mz_vec[candidate_cuts]
                candidate_filter = np.abs(candidate_mz - target_mz) <= max_shift_mz
                candidate_cuts = candidate_cuts[candidate_filter]

            if len(candidate_cuts) > 0:
                candidate_mz = mz_vec[candidate_cuts]
                best_cut = candidate_cuts[np.argmin(np.abs(candidate_mz - target_mz))]

            else:
                best_cut = int(np.clip(target_cut,
                                       lowest_allowed,
                                       highest_allowed))

            selected_cuts.append(best_cut)
            previous_cut = best_cut

        edges = np.array([0] + selected_cuts + [n_values],
                         dtype = int)

    else:
        edges = target_edges

    starts = edges[: -1]
    stops = edges[1: ]

    workload_mat = np.zeros((len(starts), 6))

    for batch_id in np.arange(len(starts),
                              dtype = int):

        start = starts[batch_id]
        stop = stops[batch_id]

        batch_mz_vec = mz_vec[start: stop]

        median_mz = np.median(batch_mz_vec)

        q1_mz = np.percentile(batch_mz_vec,
                              25)

        q3_mz = np.percentile(batch_mz_vec,
                              75)

        iqr_mz_da = q3_mz - q1_mz
        iqr_mz_ppm = iqr_mz_da / median_mz * 1e6

        workload_mat[batch_id, 0] = median_mz
        workload_mat[batch_id, 1] = stop - start
        workload_mat[batch_id, 2] = start
        workload_mat[batch_id, 3] = stop
        workload_mat[batch_id, 4] = iqr_mz_da
        workload_mat[batch_id, 5] = iqr_mz_ppm

    workload_mat = workload_mat[workload_mat[:, 0].argsort(), :]

    return workload_mat
