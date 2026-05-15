from __future__ import annotations

import numpy as np
from CosineMatrix import *
from IntramoduleSimilarityCalc import *
from align_fragments_engine import *
from all_modules_silhouette_vector_summarizer import *
from estimate_k_by_resampled_spectral_clustering import *
from sklearn_spectral_modules_from_cosine_matrix import *

# TODO: unresolved names: module

def clustering_spectra_with_spectral_clustering(context,
                                                params):
    """
    Orchestrate MS2 spectral clustering for one raw feature module.

    Expected context keys:
        Feature_module, All_FeaturesTable, SamplesNames, slice_id
    """

    Feature_module = context["Feature_module"]
    All_FeaturesTable = context["All_FeaturesTable"]
    SamplesNames = context["SamplesNames"]
    slice_id = context.get("slice_id", 0)

    n_spectra = len(Feature_module)
    min_spectra = int(np.ceil(params["alignment"]["min_spectra_fraction"] * n_spectra))

    alignment_context = {
        "All_FeaturesTable": All_FeaturesTable,
        "Feature_module": Feature_module,
        "SamplesNames": SamplesNames,
        "min_spectra": min_spectra,
    }

    aligned_fragments_mat, aligned_fragments_mz_mat, explained_fraction_int, n_features, Spectra_idVec = align_fragments_engine(context = alignment_context,
                                                                                                                                params = params)

    filtered_feature_module = np.array(Feature_module)[Spectra_idVec].tolist()

    n_spectra = aligned_fragments_mat.shape[1] - 1

    current_sampling_size = min(params["clustering"]["Nspectra_sampling"],
                                n_spectra)

    max_n_clusters = min(params["clustering"]["max_Nspectra_cluster"],
                         current_sampling_size)

    k_context = {
        "aligned_fragments_mat": aligned_fragments_mat,
        "max_n_clusters": max_n_clusters,
        "current_sampling_size": current_sampling_size,
    }

    n_clusters, all_modules_by_iteration, sampled_spectra_by_iteration = estimate_k_by_resampled_spectral_clustering(context = k_context,
                                                                                                                     params = params)

    cosine_matrix = CosineMatrix(AlignedFragmentsMat = aligned_fragments_mat,
                                 N_features = n_spectra)

    if n_clusters == 1:
        modules = np.array([set(range(n_spectra))],
                           dtype = object)
    else:
        modules = sklearn_spectral_modules_from_cosine_matrix(cosine_matrix = cosine_matrix,
                                                              n_clusters = n_clusters,
                                                              min_nodes = params["clustering"].get("min_nodes", 1),
                                                              assign_labels = params["clustering"].get("assign_labels", "discretize"),
                                                              random_state = params["clustering"].get("random_state", 0))

    IntramoduleSimilarity = IntramoduleSimilarityCalc(Modules = modules,
                                                      CosineMat = cosine_matrix.copy(),
                                                      percentile = params["summary"]["percentile"])

    modules_silhouette_summary_table = all_modules_silhouette_vector_summarizer(CosineMat = cosine_matrix,
                                                                                modules = modules,
                                                                                percentile = params["summary"]["percentile"])

    Modules = [list(module) for module in modules]

    This_Module_FeaturesTable = np.hstack((All_FeaturesTable[filtered_feature_module, :].copy(),
                                           explained_fraction_int.reshape(-1, 1)))

    This_Module_FeaturesTable = np.hstack((This_Module_FeaturesTable,
                                           slice_id * np.ones(len(explained_fraction_int)).reshape(-1, 1)))

    feature_cluster_data = {
        "Modules": Modules,
        "Feature_module": filtered_feature_module,
        "IntramoduleSimilarity": IntramoduleSimilarity,
        "All_FeaturesTable": This_Module_FeaturesTable,
        "AlignedFragmentsMat": aligned_fragments_mat,
        "AlignedFragments_mz_Mat": aligned_fragments_mz_mat,
        "modules_silhouette_summary_table": modules_silhouette_summary_table,
        "k_evidence": {
            "n_clusters": n_clusters,
            "all_modules_by_iteration": all_modules_by_iteration,
            "sampled_spectra_by_iteration": sampled_spectra_by_iteration,
        },
    }

    sampling_samples = current_sampling_size

    return [feature_cluster_data,
            sampling_samples]