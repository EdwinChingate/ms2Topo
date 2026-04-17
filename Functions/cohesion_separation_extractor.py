from __future__ import annotations
from cohesion_vector_calculator import *
from nodes2centroids_cohesion_approximation import *
import numpy as np
from separation_vector_calculator import *

def cohesion_separation_extractor(n_nodes,
                                  modules,
                                  CosineMat = None,
                                  nodes_modules_cosine_matrix = None,
                                  aproximate_mean_with_centroid = False):

    if n_nodes == 1:
        cohesion_vector = np.array([1])
    elif aproximate_mean_with_centroid:
        cohesion_vector, nodes_modules_cosine_matrix = nodes2centroids_cohesion_approximation(nodes_modules_cosine_matrix = nodes_modules_cosine_matrix)
    else:    
        cohesion_vector = cohesion_vector_calculator(CosineMat = CosineMat,
                                                     modules = modules)

    if len(modules) > 1:
        separation_vector, closest_module_vector = separation_vector_calculator(CosineMat = CosineMat,
                                                                                modules = modules,
                                                                                aproximate_mean_with_centroid = aproximate_mean_with_centroid,
                                                                                nodes_modules_cosine_matrix = nodes_modules_cosine_matrix)
    else:
        separation_vector = np.zeros(n_nodes)
        closest_module_vector = np.zeros(n_nodes).astype(int)

    return [cohesion_vector, separation_vector, closest_module_vector]


# In[246]: