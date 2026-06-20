from __future__ import annotations

import numpy as np
import pandas as pd

def align_all_ms2_to_consensus_intervals(consensus_spectrum_df,
                                         all_ms2,
                                         consensus_mz_col = 'median_mz(Da)',
                                         consensus_min_mz_col = 'min_mz',
                                         consensus_max_mz_col = 'max_mz',
                                         raw_mz_col = 0,
                                         raw_intensity_col = 9,
                                         raw_sample_id_col = -1,
                                         aggregation = 'closest'):
    """
    Align raw MS2 fragments to consensus-fragment intervals.

    The consensus spectrum defines the rows.
    The raw sample/spectrum ids define the columns.

    Output:
        aligned_mz_df:
            rows    = consensus fragments
            columns = samples/spectra
            values  = observed raw fragment m/z

        aligned_intensity_df:
            same shape, but values are raw fragment intensities.

        assignment_df:
            one row per accepted raw-fragment assignment.

    aggregation options:
        "closest"       -> keep raw fragment closest to consensus m/z
        "max_intensity" -> keep raw fragment with highest intensity
    """

    if isinstance(all_ms2, pd.DataFrame):
        raw_mz = all_ms2[str(raw_mz_col)].to_numpy(dtype = float) if str(raw_mz_col) in all_ms2.columns else all_ms2.iloc[:, raw_mz_col].to_numpy(dtype = float)
        raw_intensity = all_ms2[str(raw_intensity_col)].to_numpy(dtype = float) if str(raw_intensity_col) in all_ms2.columns else all_ms2.iloc[:, raw_intensity_col].to_numpy(dtype = float)
        raw_sample_id = all_ms2[str(raw_sample_id_col)].to_numpy(dtype = int) if str(raw_sample_id_col) in all_ms2.columns else all_ms2.iloc[:, raw_sample_id_col].to_numpy(dtype = int)

    else:
        all_ms2 = np.asarray(all_ms2)
        raw_mz = all_ms2[:, raw_mz_col].astype(float)
        raw_intensity = all_ms2[:, raw_intensity_col].astype(float)
        raw_sample_id = all_ms2[:, raw_sample_id_col].astype(int)

    consensus_mz = consensus_spectrum_df[consensus_mz_col].to_numpy(dtype = float)
    consensus_min_mz = consensus_spectrum_df[consensus_min_mz_col].to_numpy(dtype = float)
    consensus_max_mz = consensus_spectrum_df[consensus_max_mz_col].to_numpy(dtype = float)

    good_raw = (np.isfinite(raw_mz) &
                np.isfinite(raw_intensity) &
                np.isfinite(raw_sample_id))

    raw_mz = raw_mz[good_raw]
    raw_intensity = raw_intensity[good_raw]
    raw_sample_id = raw_sample_id[good_raw]

    raw_order = np.argsort(raw_mz)

    raw_mz_sorted = raw_mz[raw_order]
    raw_intensity_sorted = raw_intensity[raw_order]
    raw_sample_id_sorted = raw_sample_id[raw_order]

    sample_ids = np.unique(raw_sample_id_sorted)
    sample_ids.sort()

    sample_id_to_col = {sample_id: col_id
                        for col_id, sample_id in enumerate(sample_ids)}

    n_consensus_fragments = len(consensus_mz)
    n_samples = len(sample_ids)

    aligned_mz_mat = np.zeros((n_consensus_fragments,
                               n_samples),
                              dtype = float)

    aligned_intensity_mat = np.zeros((n_consensus_fragments,
                                      n_samples),
                                     dtype = float)

    aligned_score_mat = np.full((n_consensus_fragments,
                                 n_samples),
                                np.inf,
                                dtype = float)

    assignment_rows = []

    for consensus_fragment_id in range(n_consensus_fragments):

        min_mz = consensus_min_mz[consensus_fragment_id]
        max_mz = consensus_max_mz[consensus_fragment_id]
        center_mz = consensus_mz[consensus_fragment_id]

        if not np.isfinite(min_mz) or not np.isfinite(max_mz):
            continue

        start_id = np.searchsorted(raw_mz_sorted,
                                   min_mz,
                                   side = "left")

        stop_id = np.searchsorted(raw_mz_sorted,
                                  max_mz,
                                  side = "right")

        if start_id >= stop_id:
            continue

        candidate_mz = raw_mz_sorted[start_id:stop_id]
        candidate_intensity = raw_intensity_sorted[start_id:stop_id]
        candidate_sample_id = raw_sample_id_sorted[start_id:stop_id]

        mz_error = candidate_mz - center_mz
        abs_error = np.abs(mz_error)

        for candidate_id in range(len(candidate_mz)):

            sample_id = int(candidate_sample_id[candidate_id])
            sample_col = sample_id_to_col[sample_id]

            mz_value = float(candidate_mz[candidate_id])
            intensity_value = float(candidate_intensity[candidate_id])
            distance_value = float(abs_error[candidate_id])

            if aggregation == "closest":

                replace_value = distance_value < aligned_score_mat[consensus_fragment_id,
                                                                   sample_col]

            elif aggregation == "max_intensity":

                replace_value = intensity_value > aligned_intensity_mat[consensus_fragment_id,
                                                                        sample_col]

            else:
                raise ValueError("aggregation must be 'closest' or 'max_intensity'.")

            if replace_value:
                aligned_mz_mat[consensus_fragment_id,
                               sample_col] = mz_value

                aligned_intensity_mat[consensus_fragment_id,
                                      sample_col] = intensity_value

                aligned_score_mat[consensus_fragment_id,
                                  sample_col] = distance_value

            assignment_rows.append({"consensus_fragment_id": consensus_fragment_id,
                                    "sample_id": sample_id,
                                    "consensus_mz": center_mz,
                                    "consensus_min_mz": min_mz,
                                    "consensus_max_mz": max_mz,
                                    "raw_fragment_mz": mz_value,
                                    "raw_fragment_intensity": intensity_value,
                                    "mz_error_da": mz_value - center_mz,
                                    "mz_error_ppm": (mz_value - center_mz) / center_mz * 1e6})

    aligned_mz_df = pd.DataFrame(aligned_mz_mat,
                                 columns = [str(sample_id) for sample_id in sample_ids])

    aligned_intensity_df = pd.DataFrame(aligned_intensity_mat,
                                        columns = [str(sample_id) for sample_id in sample_ids])

    aligned_mz_df.insert(0,
                         "consensus_mz",
                         consensus_mz)

    aligned_mz_df.insert(0,
                         "consensus_fragment_id",
                         np.arange(n_consensus_fragments,
                                   dtype = int))

    aligned_intensity_df.insert(0,
                                "consensus_mz",
                                consensus_mz)

    aligned_intensity_df.insert(0,
                                "consensus_fragment_id",
                                np.arange(n_consensus_fragments,
                                          dtype = int))

    assignment_df = pd.DataFrame(assignment_rows)

    return {"aligned_mz_df": aligned_mz_df,
            "aligned_intensity_df": aligned_intensity_df,
            "assignment_df": assignment_df}
