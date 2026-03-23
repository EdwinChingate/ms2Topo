from __future__ import annotations
import numpy as np
from silhouette_vector_calculator import *

def best_merging4silhouette(CosineMat,
                            modules_space):
    
    n_modules_spaces = len(modules_space)
    
    mean_silhouette_meta_vector = np.zeros(n_modules_spaces)

    for modules_id in range(n_modules_spaces):
        modules = modules_space[modules_id]
        silhouette_vector = silhouette_vector_calculator(CosineMat = CosineMat,
                                                         modules = modules)
        mean_silhouette_meta_vector[modules_id] = np.mean(silhouette_vector)
        
    best_silhouette_loc = int(np.argmax(mean_silhouette_meta_vector))

    return modules_space[best_silhouette_loc]