from __future__ import annotations

import numpy as np
from overlapping_gauss_peaks import *

def gaussian_chromatogram(context,
                          params):
    """
    Sum all Gaussian peak contributions into one chromatographic model.

    Expected context keys:
        rt_vec, parameters_list
    """

    rt_vec = context["rt_vec"]
    parameters_list = context["parameters_list"]

    n_peaks = int(len(parameters_list) / 3)
    parameters_mat = np.array(parameters_list).reshape(n_peaks,
                                                       3)

    overlap_context = {"rt_vec": rt_vec,
                       "parameters_mat": parameters_mat}

    chromatogram_matrix = overlapping_gauss_peaks(context = overlap_context,
                                                  params = params)

    intensity_model = np.sum(chromatogram_matrix.T,
                             axis = 0)

    return intensity_model
