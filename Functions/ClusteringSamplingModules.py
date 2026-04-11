from __future__ import annotations
from AlignFragmentsEngine import *
from CosineOverlappingClustering import *
from Retrieve_and_Join_ms2_for_feature import *
from UpdateIntramoduleSimilarityAfterClustering import *
from UpdateUniqueModulesAfterClustering import *
import numpy as np
from update_silhouette_summary_table_after_clustering import *

def ClusteringSamplingModules(All_consensus_ms2,      
                              ModulesList,            
                              IntramoduleSimilarityList,
                              BigFeature_Module,      
                              All_FeaturesTable,
                              SamplesNames,
                              modules_silhouette_summary_tables_list,
                              min_spectra = 3,
                              Intensity_to_explain = 0.9,
                              cos_tol = 0.9,
                              percentile = 10,
                              slice_id = 0,
                              sample_id_col = 16,
                              ms2_spec_id_col = 15,
                              ms2Folder = 'ms2_spectra',
                              ToAdd = 'mzML',
                              Norm2One = False):

    feature_cluster_data = CosineOverlappingClustering(All_ms2 = np.array(All_consensus_ms2),
                                                       SamplesNames = SamplesNames,
                                                       All_FeaturesTable = All_FeaturesTable,
                                                       Feature_module = np.arange(len(ModulesList)),
                                                       Spectra_idVec = np.arange(len(ModulesList)),
                                                       Intensity_to_explain = 1,
                                                       min_spectra = min_spectra,
                                                       cos_tol = cos_tol,
                                                       percentile = percentile,
                                                       slice_id = slice_id)   

    Modules, Feature_Module, IntramoduleSimilarity, This_Module_FeaturesTable, AlignedFragmentsMat, AlignedFragments_mz_Mat, modules_silhouette_summary_table = feature_cluster_data

    IntramoduleSimilarityModulesMat = UpdateIntramoduleSimilarityAfterClustering(Modules = Modules,
                                                                                 IntramoduleSimilarityList = IntramoduleSimilarityList)

    sampling_modules_silhouette_summary_table = update_silhouette_summary_table_after_clustering(modules = Modules,
                                                                                                 modules_silhouette_summary_tables_list = modules_silhouette_summary_tables_list)

    Modules = UpdateUniqueModulesAfterClustering(New_Modules = Modules,
                                                 Modules = ModulesList)

    All_ms2, Spectra_idVec = Retrieve_and_Join_ms2_for_feature(All_FeaturesTable = All_FeaturesTable,
                                                               Feature_module = BigFeature_Module,
                                                               SamplesNames = SamplesNames,
                                                               sample_id_col = sample_id_col,
                                                               ms2_spec_id_col = ms2_spec_id_col,
                                                               ms2Folder = ms2Folder,
                                                               ToAdd = ToAdd,
                                                               Norm2One = Norm2One)

    AlignedFragmentsMat, AlignedFragments_mz_Mat, Explained_fractionInt, N_features = AlignFragmentsEngine(All_ms2 = All_ms2,
                                                                                                           Feature_module = BigFeature_Module,
                                                                                                           Intensity_to_explain = Intensity_to_explain,
                                                                                                           min_spectra = min_spectra)

    feature_cluster_data = [Modules,
                            BigFeature_Module,
                            IntramoduleSimilarityModulesMat,
                            All_FeaturesTable,
                            AlignedFragmentsMat,
                            AlignedFragments_mz_Mat,
                            sampling_modules_silhouette_summary_table]

    return [feature_cluster_data, Explained_fractionInt]