from __future__ import annotations
from AdjacencyList_from_matrix import *
from AlignFragmentsEngine import *
from CosineMatrix import *
from IntramoduleSimilarityCalc import *
from all_modules_silhouette_vector_summarizer import *
import numpy as np
from silhouette_merging_neighbor_clusters import *
from silhouette_overlapping import *

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
    #print('CosineMat')
    #ShowDF(CosineMat)
    #print("CosClusteringEngine")
    #ShowDF(All_FeaturesTable)
    AdjacencyList_Features, features_ids = AdjacencyList_from_matrix(CosineMat = CosineMat,
                                                                     N_ms2_spectra = N_features,
                                                                     cos_tol = cos_tol)
    modules, silhouette_vector, closest_module_vector = silhouette_overlapping(AdjacencyList_Features = AdjacencyList_Features,
                                                                               CosineMat = CosineMat)
    #print("silhouette_vector")
    #print(silhouette_vector)
    #print('just spectral overlapping')
    #print(modules)
    print("before merging")
    print(np.mean(silhouette_vector))
    #for module in modules:
    #    print(module)
    #    print(np.min(All_FeaturesTable[list(module),1]),np.mean(All_FeaturesTable[list(module),1]),np.max(All_FeaturesTable[list(module),1]))
    #    ShowDF(All_FeaturesTable[list(module), :])
    #    print(silhouette_vector[list(module)])
    #    print(np.mean(silhouette_vector[list(module)]))
    
    
    #modules, silhouette_vector, CompactCosineTen, IntramoduleSimilarity = silhouette_overlap_merging(modules = modules,    
    #                                                                                                 silhouette_vector = silhouette_vector,
    #                                                                                                 CosineMat = CosineMat.copy(),
    #                                                                                                 percentile = percentile,
    #                                                                                                 cos_tol = 0.6)  

    
    modules, silhouette_vector, closest_module_vector = silhouette_merging_neighbor_clusters(modules = modules,
                                                                                             CosineMat = CosineMat,
                                                                                             silhouette_vector = silhouette_vector,
                                                                                             closest_module_vector = closest_module_vector)
    
    
    #print("silhouette_vector")
    print("after merging")    
    print(np.mean(silhouette_vector))
    #print('more overlapping')
    #for module in modules:
    #    print(module)
    #    print(np.min(All_FeaturesTable[list(module),1]),np.mean(All_FeaturesTable[list(module),1]),np.max(All_FeaturesTable[list(module),1]))
    #    ShowDF(All_FeaturesTable[list(module), :])
    #    print(silhouette_vector[list(module)])
    #    print(np.mean(silhouette_vector[list(module)]))
    
    IntramoduleSimilarity = IntramoduleSimilarityCalc(Modules = modules,
                                                      CosineMat = CosineMat.copy(),
                                                      percentile = percentile)
    
    
    modules_silhouette_summary_table = all_modules_silhouette_vector_summarizer(CosineMat = CosineMat,
                                                                                modules = modules,
                                                                                percentile = percentile)

    #print("modules_silhouette_summary_table")
    #ShowDF(modules_silhouette_summary_table)
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
