from __future__ import annotations

import numpy as np
from evaluate_population import *
from fitness_selector import *
from mate_square_gauss_par_pop import *

def mate_generations(context,
                     params):
    """
    Evolve a Gaussian-parameter population through mating and fitness selection.

    Expected context keys:
        population, smooth_peaks, generations, n_select
    """

    population = context["population"]
    smooth_peaks = context["smooth_peaks"]
    generations = context["generations"]
    n_select = context["n_select"]

    for generation in np.arange(generations):
        mate_context = {"seed_population": population}
        population = mate_square_gauss_par_pop(context = mate_context,
                                               params = params)

        mate_context = {"seed_population": population}
        population = mate_square_gauss_par_pop(context = mate_context,
                                               params = params)

        evaluation_context = {"population": population,
                              "smooth_peaks": smooth_peaks}

        r2_vec = evaluate_population(context = evaluation_context,
                                     params = params)

        selector_context = {"r2_vec": r2_vec,
                            "population": population,
                            "n_select": n_select}

        population, r2_list_fit = fitness_selector(context = selector_context,
                                                   params = params)

    return [population,
            r2_list_fit]
