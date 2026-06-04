from __future__ import annotations

from evaluate_population import *
from fitness_selector import *
from mate_generations import *
from refine_chrom_peak import *

def refine_pop_one_peak(context,
                        params):
    """
    Refine a population by locally refitting one peak at a time.

    Expected context keys:
        population, smooth_peaks, bounds_mat, n_select, generations
    """

    population = context["population"]
    smooth_peaks = context["smooth_peaks"]
    bounds_mat = context["bounds_mat"]
    n_select = context["n_select"]
    generations = context["generations"]

    population_0 = population.copy()

    for parameters_mat in population_0:
        refine_context = {"parameters_mat": parameters_mat,
                          "smooth_peaks": smooth_peaks,
                          "bounds_mat": bounds_mat}

        new_population = refine_chrom_peak(context = refine_context,
                                           params = params)

        mate_context = {"population": new_population,
                        "smooth_peaks": smooth_peaks,
                        "generations": generations,
                        "n_select": n_select}

        new_population, r2_list_fit = mate_generations(context = mate_context,
                                                       params = params)

        population = population + new_population

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
