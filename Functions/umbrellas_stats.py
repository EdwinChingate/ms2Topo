from __future__ import annotations

import numpy as np
from weight_gauss import *

def umbrellas_stats(context,
                    params):
    """
    Estimate initial Gaussian parameters for peak umbrellas.

    Expected context keys:
        smooth_peaks, peaks_umbrella_mat, n_peaks

    Relevant params:
        params["columns"]["rt_col"]
        params["columns"]["int_col"]
    """

    smooth_peaks = context["smooth_peaks"]
    peaks_umbrella_mat = context["peaks_umbrella_mat"]
    n_peaks = context["n_peaks"]

    rt_col = params["columns"]["rt_col"]
    int_col = params["columns"]["int_col"]

    for pseudo_peak_id in np.arange(n_peaks,
                                    dtype = int):
        early_location = int(peaks_umbrella_mat[pseudo_peak_id, 1])
        late_location = int(peaks_umbrella_mat[pseudo_peak_id, 2])
        max_rt_location = int(peaks_umbrella_mat[pseudo_peak_id, 0])

        rt = smooth_peaks[max_rt_location, rt_col]
        rt_vec = smooth_peaks[early_location: late_location, rt_col]
        int_vec = smooth_peaks[early_location: late_location, int_col]

        weight_context = {"rt_vec": rt_vec,
                          "int_vec": int_vec,
                          "rt": rt}

        stats = weight_gauss(context = weight_context,
                             params = params)

        peaks_umbrella_mat[pseudo_peak_id, 3:] = stats

    return peaks_umbrella_mat
