from __future__ import annotations
from leiden_clustering_space_engine import *
import numpy as np

# TODO: unresolved names: Graph

def leiden_silhouette_clustering(CosineMat,
                                 extract_mst = True,
                                 resolution_parameter = 0.4,
                                 n_iterations = 3):

    cosine_matrix = CosineMat.copy()
    np.fill_diagonal(cosine_matrix, 0) 

    similarity_cosine_network = Graph.Weighted_Adjacency(cosine_matrix,
                                                         mode = "undirected",
                                                         attr = "weight",
                                                         loops = False)
    if extract_mst:
        i_network = similarity_cosine_network.spanning_tree(weights = - np.array(similarity_cosine_network.es["weight"]),
                                                            return_tree = True)

    else:
        i_network = similarity_cosine_network

    #fig, ax = plt.subplots()
    #ig.plot(
    #i_network,
    #target=ax,
    #vertex_size = 7,
    #edge_width = 1,
    #vertex_color="lightblue",
    #edge_background="white",
    #)
    #plt.show()
    modules, silhouette_vector = leiden_clustering_space_engine(CosineMat = CosineMat,
                                                                i_network = i_network,
                                                                resolution_parameter = resolution_parameter,
                                                                n_iterations = n_iterations)

    return [modules, silhouette_vector]


# In[107]: