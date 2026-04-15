from __future__ import annotations
from centroid_modules_extraction import *
from consensus_df_to_pseudo_all_ms2 import *
import numpy as np

# TODO: unresolved names: SamplesNames, all_features_table_g, intensity_to_explain, min_nodes, min_spectra, module, ms2Folder, ms2_spec_id_col, percentile_Int, percentile_mz, raw_feature_module_g, sample_id_col, seed_cosine_tolerance, to_add

raw_feature_module = raw_feature_module_g
all_features_table = all_features_table_g

current_sampling_size = 20

def centroid_seeds_extraction():

    rng = np.random.default_rng()
    sample_feature_module = rng.choice(raw_feature_module,
                                       size = current_sampling_size,
                                       replace = False)

    extraction_state = centroid_modules_extraction(sample_feature_module = np.array(sample_feature_module).astype(int),
                                                   all_features_table = all_features_table,
                                                   SamplesNames = SamplesNames,
                                                   feature_id = 0,
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

    all_consensus_ms2 = extraction_state['all_consensus_ms2']
    first_spectra = extraction_state['first_spectra']
    feature_id = extraction_state['feature_id']
    modules_seeds = extraction_state['modules']

    modules_seeds = np.array([set(sample_feature_module[np.array(list(module)).astype(int).tolist()])
                              for module in modules_seeds])

    pseudo_all_ms2 = consensus_df_to_pseudo_all_ms2(consensus_spectra_df = all_consensus_ms2)

    return [modules_seeds, pseudo_all_ms2]


# In[29]: