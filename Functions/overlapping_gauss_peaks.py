from __future__ import annotations

import numpy as np
from chrom_gauss_peak import *

def overlapping_gauss_peaks(context,
                            params):
    """
    Build a matrix with one Gaussian peak per column.

    Expected context keys:
        rt_vec, parameters_mat
    """

    rt_vec = context["rt_vec"]
    parameters_mat = context["parameters_mat"]

    n_peaks = int(len(parameters_mat[:, 0]))
    n_points = len(rt_vec)
    chromatogram_matrix = np.zeros((n_points,
                                    n_peaks))

    for peak_id in np.arange(n_peaks):
        rt, rt_std, integral = parameters_mat[peak_id, :]

        peak_context = {"rt_vec": rt_vec,
                        "rt": rt,
                        "rt_std": rt_std,
                        "integral": integral}

        chromatogram_matrix[:, peak_id] = chrom_gauss_peak(context = peak_context,
                                                           params = params)

    return chromatogram_matrix
