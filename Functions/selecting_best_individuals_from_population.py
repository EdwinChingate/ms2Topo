from __future__ import annotations
import numpy as np

def selecting_best_individuals_from_population(population,
                                               n_individuals2keep,
                                               population_silhouette_vector):
    
    best_population = []    
    individual_ranking = np.argsort(-population_silhouette_vector).astype(int)[: n_individuals2keep]
    
    for individual_id in individual_ranking:
        modules_vector = population[int(individual_id)]
        best_population.append(modules_vector)
    
    return best_population