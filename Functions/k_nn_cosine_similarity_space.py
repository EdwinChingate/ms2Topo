from __future__ import annotations
from Retrieve_and_Join_ms2_for_feature import *
from align_ms2_spectra_with_centroids import *
from cosine_to_training_space import *
import numpy as np

def k_nn_cosine_similarity_space(raw_feature_module,
                                 all_features_table,
                                 SamplesNames,
                                 centroid_state,
                                 k = 3,
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
        return []

    raw_feature_module = np.array(raw_feature_module)[spectra_id_vec].tolist()

    aligned_query_mat, aligned_query_mz_mat = align_ms2_spectra_with_centroids(all_ms2 = all_ms2,
                                                                                reference_fragments_mz_matrix = centroid_state['consensus_aligned_fragments_mz_mat'])

    cosine_to_training = cosine_to_training_space(aligned_query_mat = aligned_query_mat,
                                                  training_mat = centroid_state['consensus_aligned_fragments_mat'])

    training_labels = centroid_state['consensus_labels']
    n_modules = len(centroid_state['centroid_modules'])
    modules = [set() for _ in range(n_modules)]

    for spectrum_local_id in range(cosine_to_training.shape[0]):
        neighbours = np.argsort(-cosine_to_training[spectrum_local_id, :])[:k]

        label_scores = np.zeros(n_modules)

        for neighbour_id in neighbours:
            module_id = training_labels[neighbour_id]
            if module_id < 0:
                continue

            label_scores[module_id] += cosine_to_training[spectrum_local_id,
                                                          neighbour_id]

        best_module_id = int(np.argmax(label_scores))
        best_score = label_scores[best_module_id]

        if best_score > min_assignment_cosine:
            true_feature_id = raw_feature_module[spectrum_local_id]
            modules[best_module_id].add(int(true_feature_id))

    return modules