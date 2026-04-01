from __future__ import annotations
from evaluate_modules_vector_population_silhouette import *
from modules_as_list_of_sets_from_modules_vector import *
from mutating_population import *
import numpy as np
from population_crossover import *
from random_population_modules_vectors_generator import *
from selecting_best_individuals_from_population import *

def genetic_silhouette_clustering(CosineMat,
                                  population,
                                  n_individuals2keep = 10,
                                  stable_iterations = 5):
                                  
    n_nodes = len(CosineMat)
    random_individuals_population = random_population_modules_vectors_generator(population_matrix = np.array(population),
                                                                                n_nodes = n_nodes,
                                                                                population_size = n_individuals2keep)
    population = population + random_individuals_population
    silhouette = 0
    convergence_count = 0
    while convergence_count < stable_iterations:
        offspring = population_crossover(population = population)
        population = mutating_population(population = offspring)
        population_silhouette_vector = evaluate_modules_vector_population_silhouette(population = population,
                                                                                     CosineMat = CosineMat)
        population = selecting_best_individuals_from_population(population = population,
                                                                n_individuals2keep = n_individuals2keep,
                                                                population_silhouette_vector = population_silhouette_vector)
        new_silhouette = np.max(population_silhouette_vector)
        print(new_silhouette)

        if (new_silhouette - silhouette) < 0.01:
            convergence_count += 1            
        else:
            convergence_count = 0
        silhouette = new_silhouette
                                  
    modules = modules_as_list_of_sets_from_modules_vector(modules_vector = population[0])
                                  
    return modules