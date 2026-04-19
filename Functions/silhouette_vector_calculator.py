from __future__ import annotations
from cohesion_separation_extractor import *
import numpy as np

def silhouette_vector_calculator(modules,
                                 CosineMat = None,
                                 nodes_modules_cosine_matrix = None,
                                 aproximate_mean_with_centroid = True):

    n_nodes = len(CosineMat)
    cohesion_vector, separation_vector, closest_module_vector = cohesion_separation_extractor(n_nodes = n_nodes,
                                                                                              CosineMat = CosineMat,
                                                                                              modules = modules,
                                                                                              nodes_modules_cosine_matrix = nodes_modules_cosine_matrix,
                                                                                              aproximate_mean_with_centroid = aproximate_mean_with_centroid)

    silhouette_vector = np.zeros(n_nodes)

    for node_id in range(n_nodes):
        if cohesion_vector[node_id] > 0:
            silhouette_vector[node_id] = (cohesion_vector[node_id] - separation_vector[node_id]) / (1 - min([cohesion_vector[node_id], separation_vector[node_id]]))
        else:
            silhouette_vector[node_id] = 0

    return [silhouette_vector, closest_module_vector]


# In[272]: