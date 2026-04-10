from __future__ import annotations
from best_merging4silhouette import *
from find_and_reassign_negative_silhouette_nodes import *
from merging_combinations_mudules_space import *
import numpy as np
from igraph import Graph
import leidenalg as la

def leiden_silhouette_clustering(CosineMat):
    
    cosine_matrix = CosineMat.copy()
    np.fill_diagonal(cosine_matrix, 0) 

    similarity_cosine_network = Graph.Weighted_Adjacency(cosine_matrix,
                                                         mode="undirected",
                                                         attr="weight",
                                                         loops=False)
    partition = la.find_partition(similarity_cosine_network,
                                  la.ModularityVertexPartition,
                                  weights = "weight")

    modules = find_and_reassign_negative_silhouette_nodes(modules_vector = np.array(partition.membership),
                                                          CosineMat = CosineMat)
    
    modules_space = merging_combinations_mudules_space(modules = modules,
                                                       modules_space = [modules])
    
    
    modules, silhouette_vector, closest_module_vector = best_merging4silhouette(CosineMat = CosineMat,
                                                                                modules_space = modules_space)

    return [modules, silhouette_vector]
