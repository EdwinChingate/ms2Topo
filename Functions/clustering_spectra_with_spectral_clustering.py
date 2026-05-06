from __future__ import annotations
from CosineMatrix import *
from IntramoduleSimilarityCalc import *
from align_fragments_engine import *
from all_modules_silhouette_vector_summarizer import *
from estimate_k_by_resampled_spectral_clustering import *
import numpy as np
from sklearn_spectral_modules_from_cosine_matrix import *

# TODO: unresolved names: AlignedFragmentsMat, AlignedFragments_mz_Mat, Explained_fractionInt, Spectra_idVec, module, silhouette_evaluation_matrix

def clustering_spectra_with_spectral_clustering(Feature_module,
                                                All_FeaturesTable,
                                                SamplesNames,
                                                Intensity_to_explain = 0.9,
                                                min_spectra = 3,
                                                cos_tol = 0.9,
                                                percentile = 10,
                                                percentile_mz = 5,
                                                percentile_Int = 10,
                                                slice_id = 0,
                                                max_Nspectra_cluster = 170,
                                                Nspectra_sampling = 54,
                                                SamplingTimes = 20,
                                                sample_id_col = 16,
                                                ms2_spec_id_col = 15,
                                                ms2Folder = 'ms2_spectra',
                                                ToAdd = 'mzML',
                                                Norm2One = False):
    all_features_table = All_FeaturesTable
    raw_feature_module = Feature_module


    aligned_fragments_mat, aligned_fragments_mz_mat, explained_fraction_int, n_features = align_fragments_engine()
    n_fragments = len(aligned_fragments_mat[:, 0])
    raw_feature_module = np.array(raw_feature_module)[Spectra_idVec].tolist()
    n_spectra = len(Spectra_idVec)




    n_clusters = estimate_k_by_resampled_spectral_clustering(aligned_fragments_mat)



    cosine_matrix = CosineMatrix(AlignedFragmentsMat = aligned_fragments_mat,
                                 N_features = len(aligned_fragments_mat[0, :] - 1))
    modules = sklearn_spectral_modules_from_cosine_matrix(cosine_matrix = cosine_matrix,
                                                          n_clusters = n_clusters,
                                                          min_nodes = 1,
                                                          assign_labels = 'discretize',
                                                          random_state = 0)            


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

    return [feature_cluster_data, 1]