from __future__ import annotations

import numpy as np
from biggest_selector import *

def fitness_selector(context,
                     params):
    """
    Select the fittest Gaussian parameter matrices by R².

    Expected context keys:
        r2_vec, population, n_select
    """

    r2_vec = context["r2_vec"]
    population = context["population"]
    n_select = context["n_select"]

    fit_population = []
    r2_vec_unique = np.array(list(set(r2_vec.copy())))
    sort_r2_vec = (-r2_vec_unique).argsort()
    r2_vec_unique = r2_vec_unique[sort_r2_vec]
    r2_list_fit = []

    for r2 in r2_vec_unique:
        selector_context = {"r2": r2,
                            "r2_vec": r2_vec,
                            "population": population}

        fittest_individual_id = biggest_selector(context = selector_context,
                                                 params = params)

        if fittest_individual_id >= 0:
            fit_population.append(population[fittest_individual_id])
            r2_list_fit.append(r2_vec[fittest_individual_id])

        if len(fit_population) == n_select:
            break

    return [fit_population,
            r2_list_fit]
