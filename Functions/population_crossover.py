from __future__ import annotations
from binary_crossover import *
import numpy as np

def population_crossover(population):
    
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
            child = binary_crossover(individual_1 = individual_1,
                                     individual_2 = individual_2)
            offspring.append(child)
    
    return offspring