from __future__ import annotations

import numpy as np

def mate_square_gauss_par_pop(context,
                              params):
    """
    Create a crossed population of Gaussian parameter matrices.

    Expected context keys:
        seed_population

    Relevant params:
        params["random"]["rng"]
    """

    seed_population = context["seed_population"]
    rng = params["random"]["rng"]

    n_seed_individuals = len(seed_population)
    n_peaks = len(seed_population[0])
    population = []

    for individual_1 in np.arange(n_seed_individuals,
                                  dtype = int):
        parameters_mat_i1 = seed_population[individual_1]

        for individual_2 in np.arange(individual_1,
                                      n_seed_individuals,
                                      dtype = int):
            parameters_mat_i2 = seed_population[individual_2]
            random_cut_seed = rng.random()
            random_cut_location = int(random_cut_seed * (n_peaks - 2)) + 1

            parameters_mat = parameters_mat_i1.copy()
            parameters_mat[random_cut_location:, :] = parameters_mat_i2[random_cut_location:, :]
            population.append(parameters_mat)

    return population
