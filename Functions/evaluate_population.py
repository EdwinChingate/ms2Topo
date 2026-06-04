from __future__ import annotations

import numpy as np
from overlapping_gauss_peaks import *
from r2_model import *

def evaluate_population(context,
                        params):
    """
    Evaluate every Gaussian parameter matrix against a smoothed chromatogram.

    Expected context keys:
        population, smooth_peaks
    """

    population = context["population"]
    smooth_peaks = context["smooth_peaks"]

    n_individuals = len(population)
    rt_vec = smooth_peaks[:, 0]
    int_vec = smooth_peaks[:, 1]
    r2_list = []

    for individual in np.arange(n_individuals,
                                dtype = int):
        overlap_context = {"rt_vec": rt_vec,
                           "parameters_mat": population[individual]}

        chromatogram_matrix = overlapping_gauss_peaks(context = overlap_context,
                                                      params = params)

        intensity_model = np.sum(chromatogram_matrix.T,
                                 axis = 0)

        r2_context = {"raw_signal": int_vec,
                      "model_signal": intensity_model}

        r2 = r2_model(context = r2_context,
                      params = params)

        r2_list.append(r2)

    r2_vec = np.array(r2_list,
                      dtype = np.float32)

    return r2_vec
