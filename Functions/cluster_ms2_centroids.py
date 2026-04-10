from __future__ import annotations
from AlignFragmentsEngine import *
from CosineMatrix import *
from consensus_df_to_pseudo_all_ms2 import *
import numpy as np
from scipy_seeds_finder import *

def cluster_ms2_centroids(all_consensus_ms2,
                          centroids_cosine_tolerance,
                          intensity_to_explain = 1,
                          min_spectra = 1,
                          min_nodes = 1):

    if all_consensus_ms2 is None or len(all_consensus_ms2) == 0:
        return {}

    pseudo_all_ms2 = consensus_df_to_pseudo_all_ms2(consensus_spectra_df = all_consensus_ms2)

    n_consensus_features = int(np.max(pseudo_all_ms2[:, 10])) + 1
    consensus_feature_module = list(range(n_consensus_features))

    aligned_fragments_mat, aligned_fragments_mz_mat, explained_fraction_int, n_features = AlignFragmentsEngine(All_ms2 = pseudo_all_ms2,
                                                                                                                Feature_module = consensus_feature_module,
                                                                                                                Intensity_to_explain = intensity_to_explain,
                                                                                                                min_spectra = min_spectra)

    cosine_matrix = CosineMatrix(AlignedFragmentsMat = aligned_fragments_mat,
                                 N_features = n_features)

    centroid_modules = scipy_seeds_finder(cosine_matrix = cosine_matrix,
                                          seed_cosine_tolerance = centroids_cosine_tolerance,
                                          min_nodes = min_nodes)

    n_fragments = aligned_fragments_mat.shape[0]
    centroid_vectors = []
    centroid_mz_vectors = []

    consensus_labels = -np.ones(n_features,
                                dtype = int)

    for module_id, module in enumerate(centroid_modules):
        module_list = sorted(list(module))

        centroid_vector = np.mean(aligned_fragments_mat[:, np.array(module_list) + 1],
                                  axis = 1)
        centroid_mz_vector = np.mean(aligned_fragments_mz_mat[:, np.array(module_list) + 1],
                                     axis = 1)

        centroid_vectors.append(centroid_vector)
        centroid_mz_vectors.append(centroid_mz_vector)
        consensus_labels[module_list] = module_id

    if len(centroid_vectors) == 0:
        centroids_matrix = np.zeros((n_fragments,
                                     1))
        centroids_matrix[:, 0] = aligned_fragments_mat[:, 0]

        centroids_mz_matrix = np.zeros((n_fragments,
                                        1))
        centroids_mz_matrix[:, 0] = aligned_fragments_mz_mat[:, 0]

    else:
        centroids_matrix = np.column_stack([aligned_fragments_mat[:, 0]] + centroid_vectors)
        centroids_mz_matrix = np.column_stack([aligned_fragments_mz_mat[:, 0]] + centroid_mz_vectors)

    return {'all_consensus_ms2': all_consensus_ms2,
            'pseudo_all_ms2': pseudo_all_ms2,
            'consensus_aligned_fragments_mat': aligned_fragments_mat,
            'consensus_aligned_fragments_mz_mat': aligned_fragments_mz_mat,
            'consensus_cosine_matrix': cosine_matrix,
            'centroid_modules': centroid_modules,
            'consensus_labels': consensus_labels,
            'centroids_matrix': centroids_matrix,
            'centroids_mz_matrix': centroids_mz_matrix,
            'centroids_cosine_tolerance': centroids_cosine_tolerance}