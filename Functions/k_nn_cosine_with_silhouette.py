from __future__ import annotations
from infer_modules_centroids import *
from k_nn_cosine_similarity_space import *

def k_nn_cosine_with_silhouette(raw_feature_module,
                                all_features_table,
                                SamplesNames,
                                sample_size,
                                n_spectra_sampling,
                                k = 3,
                                min_assignment_cosine = 0,
                                norm2one = False,
                                ms2Folder = 'ms2_spectra',
                                to_add = 'mzML',
                                sample_id_col = 16,
                                ms2_spec_id_col = 15,
                                intensity_to_explain = 0.9,
                                min_spectra = 3,
                                percentile_mz = 5,
                                percentile_Int = 10,
                                seed_cosine_tolerance = 0.9,
                                min_nodes = 3):

    centroid_state = infer_modules_centroids(all_features_table = all_features_table,
                                             raw_feature_module = raw_feature_module,
                                             SamplesNames = SamplesNames,
                                             sample_size = sample_size,
                                             n_spectra_sampling = n_spectra_sampling,
                                             norm2one = norm2one,
                                             ms2Folder = ms2Folder,
                                             to_add = to_add,
                                             sample_id_col = sample_id_col,
                                             ms2_spec_id_col = ms2_spec_id_col,
                                             intensity_to_explain = intensity_to_explain,
                                             min_spectra = min_spectra,
                                             percentile_mz = percentile_mz,
                                             percentile_Int = percentile_Int,
                                             seed_cosine_tolerance = seed_cosine_tolerance,
                                             min_nodes = min_nodes)

    modules = k_nn_cosine_similarity_space(raw_feature_module = raw_feature_module,
                                           all_features_table = all_features_table,
                                           SamplesNames = SamplesNames,
                                           centroid_state = centroid_state,
                                           k = k,
                                           min_assignment_cosine = min_assignment_cosine,
                                           norm2one = norm2one,
                                           ms2Folder = ms2Folder,
                                           to_add = to_add,
                                           sample_id_col = sample_id_col,
                                           ms2_spec_id_col = ms2_spec_id_col)

    return [modules,
            centroid_state]