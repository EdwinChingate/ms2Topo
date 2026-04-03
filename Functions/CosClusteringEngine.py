from __future__ import annotations
from AdjacencyList_from_matrix import *
from AlignFragmentsEngine import *
from CosineMatrix import *
from IntramoduleSimilarityCalc import *
from all_modules_silhouette_vector_summarizer import *
from find_and_reassign_negative_silhouette_nodes import *
from leiden_silhouette_clustering import *
from modules_vector2modules_list import *
import numpy as np
from silhouette_merging_neighbor_clusters import *
from silhouette_overlapping import *
from silhouette_vector_calculator import *

# TODO: unresolved names: module

def CosClusteringEngine(All_FeaturesTable,
                        All_ms2,
                        Feature_module,
                        slice_id,
                        Intensity_to_explain = 0.9,
                        min_spectra = 3,
                        cos_tol = 0.9,
                        percentile = 10):
    
    AlignedFragmentsMat, AlignedFragments_mz_Mat, Explained_fractionInt, N_features = AlignFragmentsEngine(All_ms2 = All_ms2,
                                                                                                           Feature_module = Feature_module,
                                                                                                           Intensity_to_explain = Intensity_to_explain,
                                                                                                           min_spectra = min_spectra)
    CosineMat = CosineMatrix(AlignedFragmentsMat = AlignedFragmentsMat,
                             N_features = N_features)

    modules, silhouette_vector = leiden_silhouette_clustering(CosineMat = CosineMat)

    AdjacencyList_Features, features_ids = AdjacencyList_from_matrix(CosineMat = CosineMat,
                                                                     N_ms2_spectra = N_features,
                                                                     cos_tol = cos_tol)
    modules, silhouette_vector, closest_module_vector = silhouette_overlapping(AdjacencyList_Features = AdjacencyList_Features,
                                                                               CosineMat = CosineMat)

    modules_vector = modules_vector2modules_list(modules = modules,
                                                 silhouette_vector = silhouette_vector)

    modules = find_and_reassign_negative_silhouette_nodes(modules_vector = modules_vector,
                                                          CosineMat = CosineMat)
    silhouette_vector, closest_module_vector = silhouette_vector_calculator(CosineMat = CosineMat,
                                                                            modules = modules)

    modules, silhouette_vector, closest_module_vector = silhouette_merging_neighbor_clusters(modules = modules,
                                                                                             CosineMat = CosineMat,
                                                                                             silhouette_vector = silhouette_vector,
                                                                                             closest_module_vector = closest_module_vector)

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