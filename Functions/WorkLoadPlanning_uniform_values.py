from __future__ import annotations

import numpy as np
import pandas as pd

def WorkLoadPlanning_uniform_values(mz_vec,
                                    slices = 50,
                                    mz_Tol = 2e-3,
                                    snap_to_valleys = True,
                                    max_shift_fraction = 0.15,
                                    max_shift_values = None,
                                    min_batch_size = 1,
                                    overlap_mz = None,
                                    return_df = True):

    mz_vec = np.asarray(mz_vec, dtype = float)
    n_values = len(mz_vec)

    if n_values == 0:
        if return_df:
            return pd.DataFrame(columns = ["start_idx",
                                           "stop_idx",
                                           "read_start_idx",
                                           "read_stop_idx",
                                           "batch_id",
                                           "n_values",
                                           "read_n_values",
                                           "mz_min",
                                           "mz_max",
                                           "read_mz_min",
                                           "read_mz_max",
                                           "start_cut_type",
                                           "stop_cut_type",
                                           "start_cut_forced",
                                           "stop_cut_forced",
                                           "has_forced_cut"])

        return np.empty((0, 5), dtype = int)

    if slices < 1:
        raise ValueError("slices must be >= 1")

    slices = min(slices, n_values)

    target_edges = np.linspace(0,
                               n_values,
                               slices + 1)

    target_edges = np.round(target_edges).astype(int)

    target_cuts = target_edges[1: -1]

    target_batch_size = n_values / slices

    if max_shift_values is None:
        max_shift_values = int(np.ceil(target_batch_size * max_shift_fraction))

    if snap_to_valleys:
        dif_vec = mz_vec[1: ] - mz_vec[: -1]

        valley_cuts = np.where(dif_vec > mz_Tol)[0] + 1

        selected_cuts = []
        selected_cut_types = []
        selected_cut_forced = []
        selected_cut_shift_values = []
        selected_target_cuts = []

        previous_cut = 0

        for cut_id, target_cut in enumerate(target_cuts):
            remaining_batches = slices - cut_id - 1

            lowest_allowed = previous_cut + min_batch_size
            highest_allowed = n_values - remaining_batches * min_batch_size

            low_search = max(lowest_allowed,
                             target_cut - max_shift_values)

            high_search = min(highest_allowed,
                              target_cut + max_shift_values)

            candidate_cuts = valley_cuts[(valley_cuts >= low_search) &
                                         (valley_cuts <= high_search)]

            if len(candidate_cuts) > 0:
                best_cut = candidate_cuts[np.argmin(np.abs(candidate_cuts - target_cut))]
                cut_type = "valley"
                cut_forced = False

            else:
                best_cut = int(np.clip(target_cut,
                                       lowest_allowed,
                                       highest_allowed))

                cut_type = "forced"
                cut_forced = True

            selected_cuts.append(best_cut)
            selected_cut_types.append(cut_type)
            selected_cut_forced.append(cut_forced)
            selected_cut_shift_values.append(int(best_cut - target_cut))
            selected_target_cuts.append(int(target_cut))

            previous_cut = best_cut

        edges = np.array([0] + selected_cuts + [n_values],
                         dtype = int)

        cut_types = np.array(["origin"] + selected_cut_types + ["final"],
                             dtype = object)

        cut_forced = np.array([False] + selected_cut_forced + [False],
                              dtype = bool)

        cut_shift_values = np.array([0] + selected_cut_shift_values + [0],
                                    dtype = int)

        cut_target_idx = np.array([0] + selected_target_cuts + [n_values],
                                  dtype = int)

    else:
        edges = target_edges

        cut_types = np.array(["origin"] +
                             ["target"] * (len(edges) - 2) +
                             ["final"],
                             dtype = object)

        cut_forced = np.zeros(len(edges),
                              dtype = bool)

        cut_shift_values = np.zeros(len(edges),
                                    dtype = int)

        cut_target_idx = edges.copy()

    starts = edges[: -1]
    stops = edges[1: ]

    batch_ids = np.arange(len(starts),
                          dtype = int)

    if overlap_mz is None:
        read_starts = starts.copy()
        read_stops = stops.copy()

    else:
        read_starts = []
        read_stops = []

        for start, stop in zip(starts, stops):
            if start == 0:
                read_start = 0
            else:
                read_start = np.searchsorted(mz_vec,
                                             mz_vec[start] - overlap_mz,
                                             side = "left")

            if stop >= n_values:
                read_stop = n_values
            else:
                read_stop = np.searchsorted(mz_vec,
                                            mz_vec[stop - 1] + overlap_mz,
                                            side = "right")

            read_starts.append(read_start)
            read_stops.append(read_stop)

        read_starts = np.asarray(read_starts,
                                 dtype = int)

        read_stops = np.asarray(read_stops,
                                dtype = int)

    edges_matrix = np.column_stack((starts,
                                    stops,
                                    read_starts,
                                    read_stops,
                                    batch_ids))

    if not return_df:
        return edges_matrix

    rows = []

    for batch_id in batch_ids:
        start = starts[batch_id]
        stop = stops[batch_id]
        read_start = read_starts[batch_id]
        read_stop = read_stops[batch_id]

        core_mz_vec = mz_vec[start: stop]
        read_mz_vec = mz_vec[read_start: read_stop]

        start_cut_type = cut_types[batch_id]
        stop_cut_type = cut_types[batch_id + 1]

        start_cut_forced = bool(cut_forced[batch_id])
        stop_cut_forced = bool(cut_forced[batch_id + 1])

        rows.append({"start_idx": int(start),
                     "stop_idx": int(stop),
                     "read_start_idx": int(read_start),
                     "read_stop_idx": int(read_stop),
                     "batch_id": int(batch_id),
                     "n_values": int(stop - start),
                     "read_n_values": int(read_stop - read_start),
                     "mz_min": float(core_mz_vec[0]),
                     "mz_max": float(core_mz_vec[-1]),
                     "read_mz_min": float(read_mz_vec[0]),
                     "read_mz_max": float(read_mz_vec[-1]),
                     "start_cut_type": start_cut_type,
                     "stop_cut_type": stop_cut_type,
                     "start_cut_forced": start_cut_forced,
                     "stop_cut_forced": stop_cut_forced,
                     "has_forced_cut": start_cut_forced or stop_cut_forced,
                     "start_cut_shift_values": int(cut_shift_values[batch_id]),
                     "stop_cut_shift_values": int(cut_shift_values[batch_id + 1]),
                     "start_target_idx": int(cut_target_idx[batch_id]),
                     "stop_target_idx": int(cut_target_idx[batch_id + 1])})

    return pd.DataFrame(rows)
