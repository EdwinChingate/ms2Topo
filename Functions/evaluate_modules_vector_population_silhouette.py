from __future__ import annotations
import numpy as np
from silhouette_from_modules_vector import *

# TODO: unresolved names: modules_vector

def evaluate_modules_vector_population_silhouette(population,
                                                  CosineMat):
    
    lambda_silhouette = lambda modules_vector: silhouette_from_modules_vector(CosineMat = CosineMat,
                                                                              modules_vector = modules_vector)
    population_silhouette_vector = [lambda_silhouette(modules_vector) for modules_vector in population]
    
    return np.array(population_silhouette_vector)