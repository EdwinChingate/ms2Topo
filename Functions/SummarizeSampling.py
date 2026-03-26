from __future__ import annotations
from ClusteringSamplingModules import *
from EvaluateRemainingAnalyticalSamples import *
from FeaturesTableSamples2Check import *
from FormattingSummary import *
from ReOrganizeSamplingResults import *

def SummarizeSampling(feature_clusterList,
                      All_FeaturesTable,
                      SamplesNames,
                      Original_Feature_module,
                      min_spectra = 3,
                      Intensity_to_explain = 0.9,
                      cos_tol = 0.9,
                      percentile = 10,
                      slice_id = 0,
                      sample_id_col = 16,
                      ms2_spec_id_col = 15,
                      percentile_mz = 5,
                      percentile_Int = 10,
                      Nspectra_sampling = 3,     
                      ms2Folder = 'ms2_spectra',
                      ToAdd = 'mzML',
                      Norm2One = False):

    All_consensus_ms2, ModulesList, IntramoduleSimilarityList, BigFeature_Module, modules_silhouette_summary_tables_list = ReOrganizeSamplingResults(feature_clusterList = feature_clusterList,
                                                                                                                                                     min_spectra = min_spectra,
                                                                                                                                                     percentile_mz = percentile_mz,
                                                                                                                                                     percentile_Int = percentile_Int)

    if len(ModulesList) == 0:
        return []      
    
    feature_cluster_data, Explained_fractionInt = ClusteringSamplingModules(All_consensus_ms2 = All_consensus_ms2,
                                                                            ModulesList = ModulesList,
                                                                            IntramoduleSimilarityList = IntramoduleSimilarityList,
                                                                            BigFeature_Module = BigFeature_Module,
                                                                            modules_silhouette_summary_tables_list = modules_silhouette_summary_tables_list,
                                                                            All_FeaturesTable = All_FeaturesTable,
                                                                            SamplesNames = SamplesNames,
                                                                            min_spectra = min_spectra,
                                                                            Intensity_to_explain = Intensity_to_explain,
                                                                            cos_tol = cos_tol,
                                                                            percentile = percentile,
                                                                            slice_id = slice_id,
                                                                            sample_id_col = sample_id_col,
                                                                            ms2_spec_id_col = ms2_spec_id_col,
                                                                            ms2Folder = ms2Folder,
                                                                            ToAdd = ToAdd,
                                                                            Norm2One = Norm2One)
    
    feature_cluster_data = FormattingSummary(feature_cluster_data = feature_cluster_data,
                                             Explained_fractionInt = Explained_fractionInt,
                                             slice_id = slice_id)
    
    Modules, BigFeature_Module, IntramoduleSimilarityModulesMat, _, AlignedFragmentsMat, AlignedFragments_mz_Mat, modules_silhouette_summary_table = feature_cluster_data 
    N_modules = len(Modules) 

    Samples_FeaturesIdsList, Samples_ids2Check = FeaturesTableSamples2Check(Feature_Module = BigFeature_Module,
                                                                            Original_Feature_module = Original_Feature_module,
                                                                            All_FeaturesTable = All_FeaturesTable,
                                                                            sample_id_col = sample_id_col)

    if len(Samples_ids2Check) == 0:
        return feature_cluster_data  

    feature_cluster_data = EvaluateRemainingAnalyticalSamples(Samples_FeaturesIdsList = Samples_FeaturesIdsList,
                                                              Samples_ids2Check = Samples_ids2Check,
                                                              feature_cluster_data = feature_cluster_data,
                                                              All_FeaturesTable = All_FeaturesTable,
                                                              SamplesNames = SamplesNames,
                                                              BigFeature_Module = BigFeature_Module,
                                                              IntramoduleSimilarityModulesMat = IntramoduleSimilarityModulesMat,
                                                              modules_silhouette_summary_table = modules_silhouette_summary_table,
                                                              sample_id_col = sample_id_col,
                                                              ms2_spec_id_col = ms2_spec_id_col,
                                                              ms2Folder = ms2Folder,
                                                              ToAdd = ToAdd,
                                                              Norm2One = Norm2One,
                                                              Nspectra_sampling = Nspectra_sampling,
                                                              std_distance = 3,     
                                                              ppm_tol = 20)
                                                              
    return feature_cluster_data