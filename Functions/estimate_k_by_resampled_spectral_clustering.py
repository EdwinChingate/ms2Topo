from __future__ import annotations
from evaluate_n_partitions import *
import numpy as np
from retrieve_random_aligned_fragments import *

def estimate_k_by_resampled_spectral_clustering(max_n_clusters,
                                                n_iterations):

    silhouette_evaluation_matrix = np.full((n_iterations, max_n_clusters - 1),
                                           np.nan)    
    all_modules_list = []
    for iteration in range(n_iterations):
        cosine_matrix = retrieve_random_aligned_fragments()        
        silhouette_evaluation_matrix, modules_list = evaluate_n_partitions()
        all_modules_list.append(modules_list)

    n_clusters = np.argmax(np.mean(silhouette_evaluation_matrix,
                                   axis = 0)) + 1  

    return n_clusters