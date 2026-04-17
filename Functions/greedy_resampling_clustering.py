from __future__ import annotations
from greedy_centroids_resampling_clustering import *
from nearest_centroid_classification import *

# TODO: unresolved names: SamplesNames, all_features_table, ms2Folder, ms2_spec_id_col_g, sample_id_col_g, test_feature_module

def greedy_resampling_clustering():

    raw_feature_module = test_feature_module
    greedy_centroid_state = greedy_centroids_resampling_clustering(all_features_table = all_features_table,
                                                                     raw_feature_module = raw_feature_module,
                                                                     n_spectra2analyze = len(raw_feature_module),
                                                                     SamplesNames = SamplesNames,
                                                                     ms2Folder = ms2Folder,
                                                                     to_add = 'mzML',
                                                                     current_sampling_size = 20,
                                                                     sample_id_col = sample_id_col_g,
                                                                     ms2_spec_id_col = ms2_spec_id_col_g,
                                                                     intensity_to_explain = 0.9,
                                                                     min_spectra = 3,
                                                                     percentile_mz = 5,
                                                                     percentile_Int = 10,
                                                                     seed_cosine_tolerance = 0.9,
                                                                     min_nodes = 3)

    modules, assigned_spectra = nearest_centroid_classification(raw_feature_module = greedy_centroid_state['raw_feature_module'],
                                          all_features_table = all_features_table,
                                          SamplesNames = SamplesNames,
                                          greedy_centroid_state = greedy_centroid_state,
                                          min_assignment_cosine = 0.6,
                                          norm2one = True,
                                          ms2Folder = ms2Folder,
                                          to_add = 'mzML',
                                          sample_id_col = sample_id_col_g,
                                          ms2_spec_id_col = ms2_spec_id_col_g)




    return modules