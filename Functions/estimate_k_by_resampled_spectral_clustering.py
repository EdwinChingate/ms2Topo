from __future__ import annotations
from evaluate_n_partitions import *
import numpy as np
from retrieve_random_aligned_fragments import *

def estimate_k_by_resampled_spectral_clustering(aligned_fragments_mat,
                                                max_n_clusters,
                                                n_iterations,
                                                current_sampling_size,
                                                min_nodes = 1,
                                                assign_labels = 'discretize',
                                                random_state = 0):
    """
    Estimate the number of spectral partitions using repeated random subsampling.

    Returns:
        n_clusters
        silhouette_evaluation_matrix
        all_modules_by_iteration
        sampled_spectra_by_iteration
    """

    n_spectra = aligned_fragments_mat.shape[1] - 1

    if n_spectra < 1:
        raise ValueError("aligned_fragments_mat must contain at least one spectrum column after the m/z column.")

    current_sampling_size = min(int(current_sampling_size),
                                n_spectra)

    current_sampling_size = max(current_sampling_size,
                                1)

    max_n_clusters = min(int(max_n_clusters),
                         current_sampling_size)

    max_n_clusters = max(max_n_clusters,
                         1)

    n_iterations = max(int(n_iterations),
                       1)

    rng = np.random.default_rng(random_state)

    silhouette_evaluation_matrix = np.full((n_iterations, max_n_clusters),
                                           np.nan)

    all_modules_by_iteration = []
    sampled_spectra_by_iteration = []

    for iteration in range(n_iterations):
        cosine_matrix, current_sample_aligned_fragments_mat, sampled_spectrum_ids = retrieve_random_aligned_fragments(aligned_fragments_mat = aligned_fragments_mat,
                                                                                                                      current_sampling_size = current_sampling_size,
                                                                                                                      rng = rng)

        silhouette_evaluation_matrix, modules_by_k = evaluate_n_partitions(silhouette_evaluation_matrix = silhouette_evaluation_matrix,
                                                                           cosine_matrix = cosine_matrix,
                                                                           max_n_clusters = max_n_clusters,
                                                                           iteration = iteration,
                                                                           min_nodes = min_nodes,
                                                                           assign_labels = assign_labels,
                                                                           random_state = random_state)

        all_modules_by_iteration.append(modules_by_k)
        sampled_spectra_by_iteration.append(sampled_spectrum_ids)

    mean_silhouette_by_k = np.nanmean(silhouette_evaluation_matrix,
                                      axis = 0)

    n_clusters = int(np.nanargmax(mean_silhouette_by_k) + 1)

    return [n_clusters,
            silhouette_evaluation_matrix,
            all_modules_by_iteration,
            sampled_spectra_by_iteration]