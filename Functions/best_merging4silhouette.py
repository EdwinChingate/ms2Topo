from __future__ import annotations
import numpy as np
from silhouette_vector_calculator import *

def best_merging4silhouette(CosineMat,
                            modules_space):
    
    n_modules_spaces = len(modules_space)
    
    mean_silhouette_meta_vector = np.zeros(n_modules_spaces)
    silhouette_meta_vectors_list = []
    closest_module_vectors_list = []

    for modules_id in range(n_modules_spaces):
        modules = modules_space[modules_id]
        silhouette_vector, closest_module_vector = silhouette_vector_calculator(CosineMat = CosineMat,
                                                                                modules = modules)
        silhouette_meta_vectors_list.append(silhouette_vector)
        closest_module_vectors_list.append(closest_module_vector)
        mean_silhouette_meta_vector[modules_id] = np.mean(silhouette_vector)
        
    best_silhouette_loc = int(np.argmax(mean_silhouette_meta_vector))

    return [modules_space[best_silhouette_loc], silhouette_meta_vectors_list[best_silhouette_loc], closest_module_vectors_list[best_silhouette_loc]]