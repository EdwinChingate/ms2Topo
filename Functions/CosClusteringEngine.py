from __future__ import annotations
from AdjacencyList_from_matrix import *
from AlignFragmentsEngine import *
from CosineMatrix import *
from IntramoduleSimilarityCalc import *
from all_modules_silhouette_vector_summarizer import *
from find_and_reassign_negative_silhouette_nodes import *
from k_nn_cosine_with_silhouette import *
from leiden_silhouette_clustering import *
from modules_vector2modules_list import *
import numpy as np
from silhouette_merging_neighbor_clusters import *
from silhouette_overlapping import *
from silhouette_vector_calculator import *
import time

# TODO: unresolved names: module, silhouetteList

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

    global silhouetteList

    AlignedFragmentsMat, AlignedFragments_mz_Mat, Explained_fractionInt, N_features = AlignFragmentsEngine(All_ms2 = All_ms2,
                                                                                                           Feature_module = Feature_module,
                                                                                                           Intensity_to_explain = Intensity_to_explain,
                                                                                                           min_spectra = min_spectra)
    CosineMat = CosineMatrix(AlignedFragmentsMat = AlignedFragmentsMat,
                             N_features = N_features)

    global cosine_matrix
    cosine_matrix = CosineMat.copy()

    global test_feature_module
    global all_features_table
    global SamplesNames_g
    global Norm2One_g
    global ms2Folder_g
    global sample_id_col_g
    global ms2_spec_id_col_g

    SamplesNames_g = SamplesNames
    Norm2One_g = Norm2One
    ms2Folder_g = ms2Folder
    sample_id_col_g = sample_id_col
    ms2_spec_id_col_g = ms2_spec_id_col




    test_feature_module = Feature_module
    all_features_table = All_FeaturesTable

    #ShowDF(CosineMat)


    #########3
    t_k_start = time.time()
    modules, centroid_state = k_nn_cosine_with_silhouette(raw_feature_module = Feature_module,
                                                          all_features_table = All_FeaturesTable,
                                                          SamplesNames = SamplesNames,
                                                          sample_size = 30,
                                                          n_spectra_sampling = 20,
                                                          k = 3,
                                                          min_assignment_cosine = 0,
                                                          norm2one = Norm2One,
                                                          ms2Folder = ms2Folder,
                                                          to_add = 'mzML',
                                                          sample_id_col = sample_id_col,
                                                          ms2_spec_id_col = ms2_spec_id_col,
                                                          intensity_to_explain = 0.9,
                                                          min_spectra = 3,
                                                          percentile_mz = 5,
                                                          percentile_Int = 10,
                                                          seed_cosine_tolerance = 0.9,
                                                          min_nodes = 1)
    print('k-nn')
    print(len(modules))

    silhouette_vector_k, closest_module_vector = silhouette_vector_calculator(CosineMat = CosineMat,
                                                                            modules = modules) 
    t_k_end = time.time()
    dt_k = t_k_end - t_k_start

    ##########333

    t_leiden_start = time.time()
    modules, silhouette_vector_leiden = leiden_silhouette_clustering(CosineMat = CosineMat)

    print(len(modules))
    t_leiden_end = time.time()
    dt_leiden = t_leiden_end - t_leiden_start

    t_overlap_start = time.time()
    AdjacencyList_Features, features_ids = AdjacencyList_from_matrix(CosineMat = CosineMat,
                                                                     N_ms2_spectra = N_features,
                                                                     cos_tol = cos_tol)
    modules, silhouette_vector_overlapping, closest_module_vector = silhouette_overlapping(AdjacencyList_Features = AdjacencyList_Features,
                                                                                           CosineMat = CosineMat)
    print(len(modules))
    modules_vector = modules_vector2modules_list(modules = modules,
                                                 silhouette_vector = silhouette_vector_overlapping)

    modules, silhouette_vector_overlapping, closest_module_vector = find_and_reassign_negative_silhouette_nodes(modules_vector = modules_vector,
                                                                                                                CosineMat = CosineMat)
    silhouette_vector_fix, closest_module_vector = silhouette_vector_calculator(CosineMat = CosineMat,
                                                                                modules = modules)

    modules, silhouette_vector_merging, closest_module_vector = silhouette_merging_neighbor_clusters(modules = modules,
                                                                                                     CosineMat = CosineMat,
                                                                                                     silhouette_vector = silhouette_vector_fix,
                                                                                                     closest_module_vector = closest_module_vector)
    t_overlap_end = time.time()
    print(len(modules))
    dt_overlap = t_overlap_end - t_overlap_start

    silhouette_list = [np.min(All_FeaturesTable[Feature_module, 1]),
                       np.max(All_FeaturesTable[Feature_module, 1]),
                       np.mean(silhouette_vector_leiden),
                       np.mean(silhouette_vector_overlapping),
                       np.mean(silhouette_vector_fix),
                       np.mean(silhouette_vector_merging),
                       np.mean(silhouette_vector_k),
                       dt_leiden,
                       dt_overlap,
                       dt_k,
                       len(silhouette_vector_leiden),
                       len(silhouette_vector_leiden),
                       len(silhouette_vector_leiden),
                       len(CosineMat)]
    silhouetteList.append(silhouette_list)

    IntramoduleSimilarity = IntramoduleSimilarityCalc(Modules = modules,
                                                      CosineMat = CosineMat.copy(),
                                                      percentile = percentile)

    modules_silhouette_summary_table = all_modules_silhouette_vector_summarizer(CosineMat = CosineMat,
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


# In[ ]:





# In[ ]:





# In[24]: