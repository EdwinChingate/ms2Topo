from __future__ import annotations
from centroid_modules_extraction import *
from cluster_ms2_centroids import *
import numpy as np

def infer_modules_centroids(all_features_table,
                            raw_feature_module,
                            SamplesNames,
                            sample_size,
                            n_spectra_sampling,
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

    ###############3




    global raw_feature_module_g
    global all_features_table_g    

    raw_feature_module_g = raw_feature_module
    all_features_table_g = all_features_table








    ##############



    all_consensus_ms2 = None
    first_spectra = True
    feature_id = 0
    centroids_cosine_tolerance = 0

    current_sampling_size = min(n_spectra_sampling,
                                len(raw_feature_module))

    for _ in range(sample_size):
        rng = np.random.default_rng()
        sample_feature_module = rng.choice(raw_feature_module,
                                           size = current_sampling_size,
                                           replace = False)

        extraction_state = centroid_modules_extraction(sample_feature_module = np.array(sample_feature_module).astype(int),
                                                       all_features_table = all_features_table,
                                                       SamplesNames = SamplesNames,
                                                       feature_id = feature_id,
                                                       all_consensus_ms2 = all_consensus_ms2,
                                                       first_spectra = first_spectra,
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

        all_consensus_ms2 = extraction_state['all_consensus_ms2']
        first_spectra = extraction_state['first_spectra']
        feature_id = extraction_state['feature_id']

        centroids_cosine_tolerance = max(centroids_cosine_tolerance,
                                         extraction_state['max_centroids_cosine_similarity'])
    centroids_cosine_tolerance = (centroids_cosine_tolerance + seed_cosine_tolerance) / 2

    centroid_state = cluster_ms2_centroids(all_consensus_ms2 = all_consensus_ms2,
                                           centroids_cosine_tolerance = centroids_cosine_tolerance,
                                           intensity_to_explain = 1,
                                           min_spectra = min_spectra,
                                           min_nodes = min_nodes)

    return centroid_state


# In[ ]:





# In[9]: