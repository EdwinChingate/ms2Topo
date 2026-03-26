from __future__ import annotations
from ClosingModule import *

def Update_ids_FeatureModules(AlignedSamplesList,
                              feature_cluster_data,
                              SamplesNames,
                              sampling_samples = 0,
                              sample_id_col = 6,
                              ms2_spec_id_col = 0,
                              percentile_mz = 5,
                              percentile_Int = 10,
                              feature_id = 0,
                              min_spectra = 3): 
    
    if len(feature_cluster_data) == 0:
        return [feature_id, AlignedSamplesList]
    
    Modules, Feature_module, IntramoduleSimilarity, All_FeaturesTable, AlignedFragmentsMat, AlignedFragments_mz_Mat, modules_silhouette_summary_table = feature_cluster_data
    module_id = 0
    for module in Modules:    
        IntramoduleCosineStatsVec = modules_silhouette_summary_table[module_id, 1: 6]
        feature_id, AlignedSamplesList = ClosingModule(module = module,
                                                       min_spectra = min_spectra,
                                                       sampling_samples = sampling_samples,
                                                       All_FeaturesTable = All_FeaturesTable,
                                                       sample_id_col = sample_id_col,
                                                       IntramoduleCosineStatsVec = IntramoduleCosineStatsVec,
                                                       ms2_spec_id_col = ms2_spec_id_col,
                                                       Feature_module = Feature_module,
                                                       AlignedSamplesList = AlignedSamplesList,
                                                       AlignedFragmentsMat = AlignedFragmentsMat,
                                                       AlignedFragments_mz_Mat = AlignedFragments_mz_Mat,
                                                       percentile_mz = percentile_mz,
                                                       percentile_Int = percentile_Int,
                                                       feature_id = feature_id,
                                                       SamplesNames = SamplesNames)  
        module_id += 1
        
    return [feature_id, AlignedSamplesList]