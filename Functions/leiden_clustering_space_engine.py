from __future__ import annotations
from modules_as_list_of_sets_from_modules_vector import *
import numpy as np
from silhouette_vector_calculator import *
import time

# TODO: unresolved names: la

def leiden_clustering_space_engine(CosineMat,
                                   i_network,
                                   resolution_parameter = 0.5,
                                   n_iterations = 3):
    t0 = time.time()
    partition = la.find_partition(i_network,
                                  la.CPMVertexPartition,
                                  weights = "weight",
                                  resolution_parameter = resolution_parameter,
                                  n_iterations = n_iterations)
    #print(time.time() - t0)
    #modules, silhouette_vector, closest_module_vector = find_and_reassign_negative_silhouette_nodes(modules_vector = np.array(partition.membership),
    #                                                                                                CosineMat = CosineMat)
    #print(np.array(partition.membership))
    modules = modules_as_list_of_sets_from_modules_vector(modules_vector = np.array(partition.membership))
    #print(modules)
    silhouette_vector, closest_module_vector = silhouette_vector_calculator(CosineMat = CosineMat,
                                                                            modules = modules)    

    #print(silhouette_vector)
    #modules, silhouette_vector, closest_module_vector = silhouette_merging_neighbor_clusters(modules = modules,
    #                                                                                         CosineMat = CosineMat,
    #                                                                                         silhouette_vector = silhouette_vector,
    #                                                                                         closest_module_vector = closest_module_vector)    
    #modules, silhouette_vector, silhouette, closest_module_vector = merging_combinations_mudules_space(modules = modules,
    #                                                                                                   silhouette_vector = silhouette_vector,
    #                                                                                                   CosineMat = CosineMat,
    #                                                                                                   silhouette = np.mean(silhouette_vector))
    #    

    return [modules, silhouette_vector]


# In[7]: