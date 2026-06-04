from __future__ import annotations

import numpy as np

def biggest_selector(context,
                     params):
    """
    Resolve tied fitness scores by selecting the individual with the strongest peak.

    Expected context keys:
        r2, r2_vec, population

    Relevant params:
        params["selection"]["lower_std"]
    """

    r2 = context["r2"]
    r2_vec = context["r2_vec"]
    population = context["population"]

    lower_std = params["selection"]["lower_std"]

    biggest_peak_list = []
    level_line_vec = np.where(r2_vec == r2)[0]

    if len(level_line_vec) == 1:
        fittest_individual_id = level_line_vec[0]
        return fittest_individual_id

    for individual_id in level_line_vec:
        individual = population[individual_id]
        most_intense_peak_intensity = np.max(individual[:, 2] / (individual[:, 1] + lower_std))
        biggest_peak_list.append(most_intense_peak_intensity)

    if len(biggest_peak_list) == 0:
        return -1

    biggest_peak_vec = np.array(biggest_peak_list)
    biggest_peak = np.max(biggest_peak_vec)
    biggest_peak_location = np.where(biggest_peak_vec == biggest_peak)[0][0]
    fittest_individual_id = level_line_vec[biggest_peak_location]

    return fittest_individual_id
