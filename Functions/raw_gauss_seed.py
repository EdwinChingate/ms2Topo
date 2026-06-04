from __future__ import annotations

import numpy as np
from fitness_selector import *
from refine_pop_one_peak import *
from umbrellas_stats import *

def raw_gauss_seed(context,
                   params):
    """
    Build and refine a seeded Gaussian population from detected peak maxima.

    Expected context keys:
        smooth_peaks, peaks_max, bounds_mat

    Relevant params:
        params["gaussian"]["n_select_seed"]
        params["gaussian"]["seed_generations"]
        params["gaussian"]["min_contribution_percent"]
        params["random"]["rng"]
    """

    smooth_peaks = context["smooth_peaks"]
    peaks_max = context["peaks_max"]
    bounds_mat = context["bounds_mat"]

    n_select_seed = params["gaussian"]["n_select_seed"]
    seed_generations = params["gaussian"]["seed_generations"]
    min_contribution_percent = params["gaussian"]["min_contribution_percent"]
    rng = params["random"]["rng"]

    n_peaks = len(peaks_max)
    n_signals = int(len(smooth_peaks[:, 0]))

    peaks_umbrella_mat = np.zeros((n_peaks,
                                   6))

    peaks_umbrella_mat[:, 0] = peaks_max

    peak_valley = np.array((peaks_max[1:] + peaks_max[:-1]) / 2,
                           dtype = int)

    peaks_umbrella_mat[1:, 1] = peak_valley
    peaks_umbrella_mat[:-1, 2] = peak_valley
    peaks_umbrella_mat[-1, 2] = n_signals

    umbrella_context = {"smooth_peaks": smooth_peaks,
                        "peaks_umbrella_mat": peaks_umbrella_mat,
                        "n_peaks": n_peaks}

    peaks_umbrella_mat = umbrellas_stats(context = umbrella_context,
                                         params = params)

    parameters_mat = peaks_umbrella_mat[:, 3:]

    extra_peak = np.mean(parameters_mat,
                         axis = 0).reshape(1, -1) + rng.random()

    parameters_mat = np.append(parameters_mat,
                               extra_peak,
                               axis = 0)

    extra_peak = np.median(parameters_mat,
                           axis = 0).reshape(1, -1)

    parameters_mat = np.append(parameters_mat,
                               extra_peak,
                               axis = 0)

    parameters_mat = parameters_mat[parameters_mat[:, 0].argsort(), :]

    refine_context = {"population": [parameters_mat],
                      "smooth_peaks": smooth_peaks,
                      "bounds_mat": bounds_mat,
                      "n_select": n_select_seed,
                      "generations": seed_generations}

    population, r2_list_fit = refine_pop_one_peak(context = refine_context,
                                                  params = params)

    selector_context = {"r2_vec": r2_list_fit,
                        "population": population,
                        "n_select": 1}

    population, r2_list_fit = fitness_selector(context = selector_context,
                                               params = params)

    parameters_mat = population[0]
    integral = bounds_mat[2, 1]
    min_integral_contribution = integral * min_contribution_percent / 100

    contribution_filter = parameters_mat[:, 2] > min_integral_contribution
    parameters_mat = parameters_mat[contribution_filter, :]

    return parameters_mat
