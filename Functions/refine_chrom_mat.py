from __future__ import annotations

import numpy as np

def refine_chrom_mat(context,
                     params):
    """
    Re-estimate each peak contribution after subtracting other fitted peaks.

    Expected context keys:
        chromatogram_matrix, chromatogram, parameters_mat

    Relevant params:
        params["columns"]["int_col"]
        params["columns"]["rt_col"]
        params["gaussian"]["std_distance"]
        params["gaussian"]["constrain_peaks"]
    """

    chromatogram_matrix = context["chromatogram_matrix"]
    chromatogram = context["chromatogram"]
    parameters_mat = context["parameters_mat"]

    int_col = params["columns"]["int_col"]
    rt_col = params["columns"]["rt_col"]
    std_distance = params["gaussian"]["std_distance"]
    constrain_peaks = params["gaussian"]["constrain_peaks"]

    int_vec = chromatogram[:, int_col]
    rt_vec = chromatogram[:, rt_col]

    chromatogram_matrix_adjusted = chromatogram_matrix.copy()
    n_contributions = len(chromatogram_matrix[0, :])
    sum_subtract_vec = np.ones(n_contributions)
    rt_location = np.arange(len(rt_vec))
    contributions_order = parameters_mat[:, 2].argsort()

    for peak_id in contributions_order:
        if constrain_peaks:
            rt, rt_std = parameters_mat[peak_id, :2]
            min_rt = rt - std_distance * rt_std
            max_rt = rt + std_distance * rt_std
            rt_location = (rt_vec > min_rt) & (rt_vec < max_rt)

        sum_subtract_vec[peak_id] = 0
        other_intensity_contribution = np.matmul(chromatogram_matrix_adjusted[rt_location, :],
                                                 sum_subtract_vec)

        sum_subtract_vec[peak_id] = 1
        refined_intensity_contribution = int_vec[rt_location] - other_intensity_contribution
        chromatogram_matrix_adjusted[rt_location, peak_id] = refined_intensity_contribution

    return chromatogram_matrix_adjusted
