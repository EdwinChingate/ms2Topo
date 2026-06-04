from __future__ import annotations

import numpy as np
from weight_gauss import *

def parameters_fit_gauss_parallel_peaks(context,
                                        params):
    """
    Refit one Gaussian peak at a time from a contribution matrix.

    Expected context keys:
        rt_vec, chromatogram_matrix, bounds_mat, parameters_mat
    """

    rt_vec = context["rt_vec"]
    chromatogram_matrix = context["chromatogram_matrix"]
    bounds_mat = context["bounds_mat"]
    parameters_mat = context["parameters_mat"]

    n_peaks = int(len(parameters_mat[:, 0]))
    integral = bounds_mat[2, 1]
    gaussian_population = []

    for peak_id in np.arange(n_peaks):
        parameters_mat_peak = parameters_mat.copy()
        int_vec = chromatogram_matrix[:, peak_id]
        rt = parameters_mat[peak_id, 0]

        weight_context = {"rt_vec": rt_vec,
                          "int_vec": int_vec,
                          "rt": rt}

        gaussian_parameters = weight_gauss(context = weight_context,
                                           params = params)

        parameters_mat_peak[peak_id, :] = np.array(gaussian_parameters)
        parameters_mat_peak = parameters_mat_peak[parameters_mat_peak[:, 0].argsort(), :]

        gaussian_integral = np.sum(parameters_mat_peak[:, 2])
        parameters_mat_peak[:, 2] = parameters_mat_peak[:, 2] * integral / gaussian_integral

        gaussian_population.append(parameters_mat_peak)

    return gaussian_population
