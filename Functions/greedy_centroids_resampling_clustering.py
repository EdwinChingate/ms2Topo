from __future__ import annotations
from centroid_modules_extraction import *
from greedy_formatting import *
import numpy as np

def greedy_centroids_resampling_clustering(all_features_table,
                                           raw_feature_module,
                                           n_spectra2analyze,
                                           SamplesNames,
                                           ms2Folder,
                                           modules = None,
                                           to_add = 'mzML',
                                           current_assigned_spectra = 0,
                                           current_modules = 0,
                                           current_sampling_size = 20,
                                           pseudo_all_ms2 = np.array(0),
                                           use_pseudo_all_ms2 = False,
                                           sample_id_col = 15,
                                           ms2_spec_id_col = 16,
                                           intensity_to_explain = 0.9,
                                           min_spectra = 3,
                                           percentile_mz = 5,
                                           percentile_Int = 10,
                                           seed_cosine_tolerance = 0.9,
                                           min_nodes = 3,
                                           n_nodes_append_times = 3,
                                           n_modules_times = 3):

    no_new_nodes_counter = 0
    stable_modules_counter = 0

    while True:
        if len(raw_feature_module) == 0:
            break

        current_sampling_size_iter = min(current_sampling_size,
                                         len(raw_feature_module))

        rng = np.random.default_rng()
        sample_feature_module = rng.choice(raw_feature_module,
                                           size = current_sampling_size_iter,
                                           replace = False).tolist()

        extraction_state = centroid_modules_extraction(sample_feature_module = np.array(sample_feature_module).astype(int),
                                                       all_features_table = all_features_table,
                                                       SamplesNames = SamplesNames,
                                                       pseudo_all_ms2 = pseudo_all_ms2.copy(),
                                                       use_pseudo_all_ms2 = use_pseudo_all_ms2,
                                                       first_spectra = True,
                                                       norm2one = True,
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

        modules, assigned_spectra, pseudo_all_ms2, aligned_centroids_mat = greedy_formatting(modules = modules,
                                                                                             extraction_state = extraction_state)

        n_assigned_spectra = len(assigned_spectra)
        n_current_modules = len(modules)

        if n_assigned_spectra == current_assigned_spectra:
            no_new_nodes_counter += 1
        else:
            no_new_nodes_counter = 0

        if n_current_modules == current_modules:
            stable_modules_counter += 1
        else:
            stable_modules_counter = 0

        raw_feature_module = list(set(raw_feature_module) - assigned_spectra)

        if no_new_nodes_counter >= n_nodes_append_times:
            break

        if stable_modules_counter >= n_modules_times:
            break

        current_modules = n_current_modules
        current_assigned_spectra = n_assigned_spectra
        use_pseudo_all_ms2 = True
        raw_feature_module = np.array(raw_feature_module)

    greedy_centroid_state = {'modules': modules,
                             'pseudo_all_ms2': pseudo_all_ms2,
                             'assigned_spectra': assigned_spectra,
                             'centroids_matrix': aligned_centroids_mat,
                             'raw_feature_module': np.array(raw_feature_module)}

    return greedy_centroid_state