from __future__ import annotations
from AdjacencyList_from_matrix import *
from AlignFragmentsEngine import *
from CosineMatrix import *
from ShowDF import *
from silhouette_overlap_merging import *
from silhouette_overlapping import *
from ShowDF import *

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
    AdjacencyList_Features, features_ids = AdjacencyList_from_matrix(CosineMat = CosineMat,
                                                                     N_ms2_spectra = N_features,
                                                                     cos_tol = 0.95)
    modules, current_silhouette = silhouette_overlapping(AdjacencyList_Features = AdjacencyList_Features,
                                                         CosineMat = CosineMat)
    modules, IntramoduleSimilarity, CompactCosineTen = silhouette_overlap_merging(modules = modules,
                                                                                  current_silhouette = current_silhouette,
                                                                                  CosineMat = CosineMat.copy(),
                                                                                  percentile = percentile,
                                                                                  cos_tol = cos_tol)  

    Modules = [list(module) for module in modules]
    ShowDF(CompactCosineTen[:, :, 2])
    ShowDF(IntramoduleSimilarity)
    This_Module_FeaturesTable = np.hstack((All_FeaturesTable[Feature_module, :].copy(),
                                           Explained_fractionInt))
    This_Module_FeaturesTable = np.hstack((This_Module_FeaturesTable,
                                           slice_id * np.ones(len(Explained_fractionInt)).reshape(-1, 1)))      
    feature_cluster_data = [Modules,
                            Feature_module,
                            IntramoduleSimilarity,
                            This_Module_FeaturesTable,
                            AlignedFragmentsMat,
                            AlignedFragments_mz_Mat]  
                            
    return feature_cluster_data
