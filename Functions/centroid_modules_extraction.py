from __future__ import annotations
from AlignFragmentsEngine import *
from CosineMatrix import *
from Retrieve_and_Join_ms2_for_feature import *
import numpy as np
from piling_up_consensus_ms2_spectra import *
from scipy_seeds_finder import *

def centroid_modules_extraction(sample_feature_module,
                                all_features_table,
                                SamplesNames,
                                feature_id = 0,
                                all_consensus_ms2 = None,
                                first_spectra = True,
                                norm2one = True,
                                pseudo_all_ms2 = 0,
                                use_pseudo_all_ms2 = False,
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

    all_ms2, spectra_id_vec = Retrieve_and_Join_ms2_for_feature(All_FeaturesTable = all_features_table,
                                                                Feature_module = sample_feature_module,
                                                                SamplesNames = SamplesNames,
                                                                sample_id_col = sample_id_col,
                                                                ms2_spec_id_col = ms2_spec_id_col,
                                                                ms2Folder = ms2Folder,
                                                                ToAdd = to_add,
                                                                Norm2One = norm2one)


    if len(all_ms2) == 0:
        return {'all_consensus_ms2': all_consensus_ms2,
                'max_centroids_cosine_similarity': 0,
                'first_spectra': first_spectra,
                'feature_id': feature_id}

    sample_feature_module = np.array(sample_feature_module)[spectra_id_vec].astype(int)
    n_spectra = len(sample_feature_module)

    if use_pseudo_all_ms2:
        pseudo_all_ms2[:, -1] = pseudo_all_ms2[:, -1] + n_spectra
        all_ms2 = np.vstack((all_ms2,
                             pseudo_all_ms2))


    aligned_fragments_mat, aligned_fragments_mz_mat, explained_fraction_int, n_features = AlignFragmentsEngine(all_ms2 = all_ms2,
                                                                                                                Feature_module = sample_feature_module.tolist(),
                                                                                                                Intensity_to_explain = intensity_to_explain,
                                                                                                                min_spectra = min_spectra)

    cosine_matrix = CosineMatrix(AlignedFragmentsMat = aligned_fragments_mat,
                                 N_features = n_features)
    #ShowDF(cosine_matrix)
    modules = scipy_seeds_finder(cosine_matrix = cosine_matrix,
                                 seed_cosine_tolerance = seed_cosine_tolerance,
                                 min_nodes = min_spectra)

    #modules, silhouette_vector_leiden = leiden_silhouette_clustering(CosineMat = cosine_matrix,
    #                                                                 extract_mst = False)
    #print(modules)

    #AdjacencyList_Features, features_ids = AdjacencyList_from_matrix(CosineMat = cosine_matrix,
    #                                                                 N_ms2_spectra = n_features,
    #                                                                 cos_tol = 0.95)
    #modules, silhouette_vector_overlapping, closest_module_vector = silhouette_overlapping(AdjacencyList_Features = AdjacencyList_Features,
    #                                                                                       CosineMat = cosine_matrix)


    piling_state = piling_up_consensus_ms2_spectra(feature_id = feature_id,
                                                   modules = modules,
                                                   aligned_fragments_mat = aligned_fragments_mat,
                                                   aligned_fragments_mz_mat = aligned_fragments_mz_mat,
                                                   first_spectra = first_spectra,
                                                   all_consensus_ms2 = all_consensus_ms2,
                                                   min_spectra = min_spectra,
                                                   percentile_mz = percentile_mz,
                                                   percentile_Int = percentile_Int)    

    piling_state['modules'] = modules
    piling_state['all_ms2'] = all_ms2
    piling_state['sample_feature_module'] = sample_feature_module
    piling_state['aligned_fragments_mat'] = aligned_fragments_mat
    piling_state['aligned_fragments_mz_mat'] = aligned_fragments_mz_mat
    piling_state['cosine_matrix'] = cosine_matrix

    return piling_state


# In[9]: