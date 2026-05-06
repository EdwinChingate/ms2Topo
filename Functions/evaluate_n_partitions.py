from __future__ import annotations
from cosine_to_training_space import *
import numpy as np
from silhouette_vector_calculator import *
from sklearn_spectral_modules_from_cosine_matrix import *

# TODO: unresolved names: aligned_query_mat, iteration, training_mat

def evaluate_n_partitions(silhouette_evaluation_matrix,
                          cosine_matrix,
                          max_n_clusters):
    modules_list = []
    silhouette_vector, closest_module_vector = silhouette_vector_calculator(CosineMat = cosine_matrix,
                                                                            modules = [set(range(len(cosine_matrix[:, 0])))])          
    silhouette_evaluation_matrix[iteration, 0] = np.mean(silhouette_vector)    

    for n_clusters in range(2, max_n_clusters):
        modules = sklearn_spectral_modules_from_cosine_matrix(cosine_matrix = cosine_matrix,
                                                              n_clusters = n_clusters,
                                                              min_nodes = 1,
                                                              assign_labels = 'discretize',
                                                              random_state = 0)
        modules_list.append(modules)


        ########

        cosine_to_training_space(aligned_query_mat,
                                 training_mat)

        ########



        silhouette_vector, closest_module_vector = silhouette_vector_calculator(CosineMat = cosine_matrix,
                                                                                modules = modules)          
        silhouette_evaluation_matrix[iteration, n_clusters - 1] = np.mean(silhouette_vector)    

    return [silhouette_evaluation_matrix, modules_list]