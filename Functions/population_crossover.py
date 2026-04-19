from __future__ import annotations
from binary_crossover import *
import numpy as np

def population_crossover(population_matrix,
                         population):
    
    n_individuals = len(population)
    n_nodes = len(population[0])
    nodes_ids_vector = np.arange(n_nodes)
    n_crossover_nodes = int(n_nodes/2)
    offspring = []
    
    for individual_1_id in range(n_individuals):
        individual_1 = population[individual_1_id]
        offspring.append(individual_1)
        
        for individual_2_id in range(n_individuals):
            if individual_1_id == individual_2_id:
                continue
            individual_2 = population[individual_2_id] 
            child, population_matrix, duplicated = binary_crossover(n_crossover_nodes = n_crossover_nodes,
                                                                    nodes_ids_vector = nodes_ids_vector,
                                                                    population_matrix = population_matrix,
                                                                    individual_1 = individual_1,
                                                                    individual_2 = individual_2)
            if not duplicated:
                offspring.append(child)
    
    return [offspring, population_matrix]