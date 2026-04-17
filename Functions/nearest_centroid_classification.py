from __future__ import annotations
from Retrieve_and_Join_ms2_for_feature import *
from align_ms2_spectra_with_centroids import *
from cosine_to_training_space import *
import numpy as np

def nearest_centroid_classification(raw_feature_module,
                                    all_features_table,
                                    SamplesNames,
                                    greedy_centroid_state,
                                    min_assignment_cosine = 0,
                                    norm2one = False,
                                    ms2Folder = 'ms2_spectra',
                                    to_add = 'mzML',
                                    sample_id_col = 16,
                                    ms2_spec_id_col = 15):

    all_ms2, spectra_id_vec = Retrieve_and_Join_ms2_for_feature(All_FeaturesTable = all_features_table,
                                                                Feature_module = raw_feature_module,
                                                                SamplesNames = SamplesNames,
                                                                sample_id_col = sample_id_col,
                                                                ms2_spec_id_col = ms2_spec_id_col,
                                                                ms2Folder = ms2Folder,
                                                                ToAdd = to_add,
                                                                Norm2One = norm2one)

    if len(all_ms2) == 0:
        return [greedy_centroid_state['modules'], set()]

    candidate_feature_module = raw_feature_module[spectra_id_vec].tolist()

    aligned_query_mat, aligned_query_mz_mat = align_ms2_spectra_with_centroids(all_ms2 = all_ms2,
                                                                               reference_fragments_mz_matrix = greedy_centroid_state['centroids_matrix'])

    cosine_to_training = cosine_to_training_space(aligned_query_mat = aligned_query_mat,
                                                  training_mat = greedy_centroid_state['centroids_matrix'])

    modules = greedy_centroid_state['modules']
    assigned_spectra = set()

    for spectrum_local_id in range(cosine_to_training.shape[0]):
        best_module_id = int(np.argmax(cosine_to_training[spectrum_local_id, :]))
        best_score = cosine_to_training[spectrum_local_id,
                                        best_module_id]

        if best_score > min_assignment_cosine:
            true_feature_id = int(candidate_feature_module[spectrum_local_id])
            modules[best_module_id].add(true_feature_id)
            assigned_spectra.add(true_feature_id)

    return [modules, assigned_spectra]