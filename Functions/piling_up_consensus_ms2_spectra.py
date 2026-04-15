from __future__ import annotations
from ConsensusSpectra import *
from CosineMatrix import *
import numpy as np
import pandas as pd

def piling_up_consensus_ms2_spectra(feature_id,
                                    modules,
                                    aligned_fragments_mat,
                                    aligned_fragments_mz_mat,
                                    first_spectra = True,
                                    all_consensus_ms2 = None,
                                    min_spectra = 3,
                                    percentile_mz = 5,
                                    percentile_Int = 10,
                                    reduceIQR_factor = 6,
                                    return_individual_consensus_spectra = False):

    consensus_spectra_list = []
    centroid_vectors = []
    centroid_mz_vectors = []

    for module in modules:
        module_list = sorted(list(module))

        consensus_spectra_df = ConsensusSpectra(module = module_list,
                                                min_spectra = min_spectra,
                                                AlignedFragmentsMat = aligned_fragments_mat,
                                                AlignedFragments_mz_Mat = aligned_fragments_mz_mat,
                                                percentile_mz = percentile_mz,
                                                percentile_Int = percentile_Int,
                                                reduceIQR_factor = reduceIQR_factor,
                                                Columns_to_return = np.array([0, 2, 3, 9, 10, 11, 17]))

        if len(consensus_spectra_df) == 0:
            continue

        consensus_spectra_df = consensus_spectra_df.copy()
        consensus_spectra_df['feature_id'] = int(feature_id)

        if return_individual_consensus_spectra:
            consensus_spectra_list.append(consensus_spectra_df.copy())

        if first_spectra:
            all_consensus_ms2 = consensus_spectra_df.copy()
            first_spectra = False
        else:
            all_consensus_ms2 = pd.concat([all_consensus_ms2,
                                           consensus_spectra_df],
                                          ignore_index = True)

        centroid_vector = np.mean(aligned_fragments_mat[:, np.array(module_list) + 1],
                                  axis = 1)
        centroid_mz_vector = np.mean(aligned_fragments_mz_mat[:, np.array(module_list) + 1],
                                     axis = 1)

        centroid_vectors.append(centroid_vector)
        centroid_mz_vectors.append(centroid_mz_vector)

        feature_id += 1

    n_fragments = aligned_fragments_mat.shape[0]

    if len(centroid_vectors) == 0:
        centroids_fragments_mat = np.zeros((n_fragments,
                                            1))
        centroids_fragments_mat[:, 0] = aligned_fragments_mat[:, 0]

        centroids_fragments_mz_mat = np.zeros((n_fragments,
                                               1))
        centroids_fragments_mz_mat[:, 0] = aligned_fragments_mz_mat[:, 0]

        max_centroids_cosine_similarity = 0

    else:
        centroids_fragments_mat = np.column_stack([aligned_fragments_mat[:, 0]] + centroid_vectors)
        centroids_fragments_mz_mat = np.column_stack([aligned_fragments_mz_mat[:, 0]] + centroid_mz_vectors)

        n_centroids = centroids_fragments_mat.shape[1] - 1
        centroid_cosine_matrix = CosineMatrix(AlignedFragmentsMat = centroids_fragments_mat,
                                              N_features = n_centroids)
        np.fill_diagonal(centroid_cosine_matrix,
                         0)
        max_centroids_cosine_similarity = np.max(centroid_cosine_matrix)

    return {'all_consensus_ms2': all_consensus_ms2,
            'max_centroids_cosine_similarity': max_centroids_cosine_similarity,
            'first_spectra': first_spectra,
            'feature_id': feature_id,
            'centroids_fragments_mat': centroids_fragments_mat,
            'centroids_fragments_mz_mat': centroids_fragments_mz_mat,
            'consensus_spectra_list': consensus_spectra_list}


# In[30]: