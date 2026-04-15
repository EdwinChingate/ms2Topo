from __future__ import annotations
from centroid_modules_extraction import *
from greedy_formatting import *
import numpy as np

def greedy_resampling_clustering(all_features_table,
                                 raw_feature_module,
                                 SamplesNames,
                                 ms2Folder,
                                 modules = None,
                                 to_add = 'mzML',
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
                                 min_nodes = 3):


    rng = np.random.default_rng()
    sample_feature_module = rng.choice(raw_feature_module,
                                       size = current_sampling_size,
                                       replace = False)

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



    modules, assigned_spectra, pseudo_all_ms2 = greedy_formatting(modules = modules,
                                                                  extraction_state = extraction_state)

    print(modules)
    raw_feature_module = list(set(raw_feature_module) - assigned_spectra)

    if len(assigned_spectra) / len(raw_feature_module) > 0.3:
        return modules

    modules = greedy_resampling_clustering(all_features_table = all_features_table,
                                           raw_feature_module = np.array(raw_feature_module),
                                           SamplesNames = SamplesNames,
                                           ms2Folder = ms2Folder,
                                           modules = modules,
                                           current_sampling_size = current_sampling_size,
                                           pseudo_all_ms2 = pseudo_all_ms2,
                                           use_pseudo_all_ms2 = True,
                                           to_add = to_add,
                                           sample_id_col = sample_id_col,
                                           ms2_spec_id_col = ms2_spec_id_col,
                                           intensity_to_explain = intensity_to_explain,
                                           min_spectra = min_spectra,
                                           percentile_mz = percentile_mz,
                                           percentile_Int = percentile_Int,
                                           seed_cosine_tolerance = seed_cosine_tolerance,
                                           min_nodes = min_nodes)




    return modules