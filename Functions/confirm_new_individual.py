from __future__ import annotations
import numpy as np

def confirm_new_individual(population_matrix,
                           new_individual):
    individual = new_individual.reshape(1, -1) 
    contrast_matrix = np.abs(population_matrix - individual)
    contrast_vector = np.sum(contrast_matrix, axis = 1)
    contrast_vector_eval = np.where(contrast_vector == 0)[0]
    
    if len(contrast_vector_eval) > 0:
        return [population_matrix, False]
    
    population_matrix = np.vstack((population_matrix, individual))
    
    return [population_matrix, True]