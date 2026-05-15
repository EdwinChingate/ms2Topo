from __future__ import annotations

import numpy as np
from evaluate_n_partitions import *
from retrieve_random_aligned_fragments import *

def estimate_k_by_resampled_spectral_clustering(context,
                                                params):
    """
    Estimate the number of spectral partitions using repeated random subsampling.

    Expected context keys:
        aligned_fragments_mat, max_n_clusters, current_sampling_size

    Returns:
        n_clusters
        all_modules_by_iteration
        sampled_spectra_by_iteration
    """

    aligned_fragments_mat = context["aligned_fragments_mat"]
    max_n_clusters = context["max_n_clusters"]
    current_sampling_size = context["current_sampling_size"]

    n_iterations = params["clustering"]["SamplingTimes"]
    std_times = params["clustering"].get("std_times", 1)
    random_state = params["clustering"].get("random_state", 0)

    n_spectra = aligned_fragments_mat.shape[1] - 1

    if n_spectra < current_sampling_size:
        current_sampling_size = n_spectra
        n_iterations = 1

    max_n_clusters = min(current_sampling_size // 3,
                         max_n_clusters) #3
    max_n_clusters = max(max_n_clusters,
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

        evaluation_context = {
            "silhouette_evaluation_matrix": silhouette_evaluation_matrix,
            "cosine_matrix": cosine_matrix,
            "max_n_clusters": max_n_clusters,
            "iteration": iteration,
        }

        silhouette_evaluation_matrix, modules_by_k = evaluate_n_partitions(context = evaluation_context,
                                                                           params = params)

        all_modules_by_iteration.append(modules_by_k)
        sampled_spectra_by_iteration.append(sampled_spectrum_ids)

    mean_silhouette_by_k = np.nanmean(silhouette_evaluation_matrix,
                                      axis = 0)
    std_silhouette_by_k = np.nanstd(silhouette_evaluation_matrix,
                                     axis = 0)
    top_mean_silhouette_by_k = mean_silhouette_by_k + std_times * std_silhouette_by_k

    best_silhouette_k = int(np.nanargmax(mean_silhouette_by_k))
    best_silhouette = mean_silhouette_by_k[best_silhouette_k]
    best_silhouette_std = std_silhouette_by_k[best_silhouette_k]
    low_best_silhouette = best_silhouette - best_silhouette_std * std_times
    plausible_k = np.where(top_mean_silhouette_by_k >= low_best_silhouette)[0]
    n_clusters = np.min(plausible_k) + 1

    return [n_clusters,
            all_modules_by_iteration,
            sampled_spectra_by_iteration]