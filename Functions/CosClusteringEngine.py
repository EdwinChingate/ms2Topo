# Combined export from canvas: Playground.canvas
# Functions folder: /home/edwin/0-GitHubProjects/Codding/ms2Gauss/Functions
# Functions included (detected in canvas): 7





# --- CosClusteringEngine.py ---
from __future__ import annotations
from AdjacencyList_from_matrix import *
from AlignFragmentsEngine import *
from CosineMatrix import *
from IntramoduleSimilarityCalc import *
from all_modules_silhouette_vector_summarizer import *
import numpy as np
from sklearn_spectral_modules_from_cosine_matrix import *
from silhouette_vector_calculator import *

def CosClusteringEngine(All_FeaturesTable,
                        All_ms2,
                        Feature_module,
                        slice_id,
                        SamplesNames,
                        sample_id_col,
                        ms2_spec_id_col,
                        Norm2One,
                        ms2Folder,
                        Intensity_to_explain = 0.9,
                        min_spectra = 3,
                        cos_tol = 0.9,
                        percentile = 10):
    

    max_n_clusters = 6
    n_iterations = 5
    current_sampling_size = 30

    all_ms2, Spectra_idVec = Retrieve_and_Join_ms2_for_feature(All_FeaturesTable = all_features_table,
                                                               Feature_module = raw_feature_module,
                                                               SamplesNames = SamplesNames,
                                                               sample_id_col = sample_id_col_g,
                                                               ms2_spec_id_col = ms2_spec_id_col_g,
                                                               ms2Folder = ms2Folder,
                                                               ToAdd = 'mzML',
                                                               Norm2One = True)
    aligned_fragments_mat, aligned_fragments_mz_mat, explained_fraction_int, n_features = AlignFragmentsEngine(all_ms2 = all_ms2,
                                                                                                                Feature_module = raw_feature_module,
                                                                                                                Intensity_to_explain = 0.9,
                                                                                                                min_spectra = 5)

    n_fragments = len(aligned_fragments_mat[:, 0])
    #if len(all_ms2) == 0:
    #    continue

    raw_feature_module = np.array(raw_feature_module)[Spectra_idVec].tolist()
    n_spectra = len(Spectra_idVec)
    #def spectral_centroid_inference():

    silhouette_evaluation_matrix = np.full((n_iterations, max_n_clusters - 1),
                                           np.nan)

    for iteration in range(n_iterations):
        rng = np.random.default_rng()
        sample_feature_module = rng.choice(np.arange(n_spectra),
                                           size = current_sampling_size,
                                           replace = False).tolist()
        #current_sampling_size
        current_sample_aligned_fragments_mat = np.full((n_fragments, current_sampling_size + 1),
                                                        np.nan)
        current_sample_aligned_fragments_mat[:, 0] = aligned_fragments_mat[:, 0]
        current_sample_aligned_fragments_mat[:, 1:] = aligned_fragments_mat[:, np.array(sample_feature_module) + 1].copy()

        cosine_matrix = CosineMatrix(AlignedFragmentsMat = current_sample_aligned_fragments_mat,
                                     N_features = current_sampling_size)
        silhouette_vector, closest_module_vector = silhouette_vector_calculator(CosineMat = cosine_matrix,
                                                                                modules = [set(range(len(cosine_matrix[:, 0])))])          
        silhouette_evaluation_matrix[iteration, 0] = np.mean(silhouette_vector)

        for n_clusters in range(2, max_n_clusters):
            modules = sklearn_spectral_modules_from_cosine_matrix(cosine_matrix = cosine_matrix,
                                                                  n_clusters = n_clusters,
                                                                  min_nodes = 1,
                                                                  assign_labels = 'discretize',
                                                                  random_state = 0)
            #cosine_to_training

            silhouette_vector, closest_module_vector = silhouette_vector_calculator(CosineMat = cosine_matrix,
                                                                                    modules = modules)          
            silhouette_evaluation_matrix[iteration, n_clusters - 1] = np.mean(silhouette_vector)
            
    
    n_clusters = np.argmax(np.mean(silhouette_evaluation_matrix, axis = 0))
    cosine_matrix = CosineMatrix(AlignedFragmentsMat = aligned_fragments_mat,
                                 N_features = len(aligned_fragments_mat[0, :] - 1))
    modules = sklearn_spectral_modules_from_cosine_matrix(cosine_matrix = cosine_matrix,
                                                          n_clusters = n_clusters,
                                                          min_nodes = 1,
                                                          assign_labels = 'discretize',
                                                          random_state = 0)                
    
    

    IntramoduleSimilarity = IntramoduleSimilarityCalc(Modules = modules,
                                                      CosineMat = cosine_matrix.copy(),
                                                      percentile = percentile)

    modules_silhouette_summary_table = all_modules_silhouette_vector_summarizer(CosineMat = cosine_matrix,
                                                                                modules = modules,
                                                                                percentile = percentile)

    Modules = [list(module) for module in modules]
    This_Module_FeaturesTable = np.hstack((All_FeaturesTable[Feature_module, :].copy(),
                                           Explained_fractionInt))
    This_Module_FeaturesTable = np.hstack((This_Module_FeaturesTable,
                                           slice_id * np.ones(len(Explained_fractionInt)).reshape(-1, 1)))
    feature_cluster_data = [Modules,
                            Feature_module,
                            IntramoduleSimilarity,
                            This_Module_FeaturesTable,
                            AlignedFragmentsMat,
                            AlignedFragments_mz_Mat,
                            modules_silhouette_summary_table]

    return feature_cluster_data
