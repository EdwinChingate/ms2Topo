from __future__ import annotations
from CosineOverlappingClustering import *
from CosineSamplingOverlappingClustering import *

def FeatureClusterData(Feature_module,
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
    
    if len(Feature_module) < max_Nspectra_cluster:
        feature_cluster_data = CosineOverlappingClustering(All_FeaturesTable = All_FeaturesTable,
                                                           Feature_module = Feature_module,
                                                           sample_id_col = sample_id_col,
                                                           SamplesNames = SamplesNames,
                                                           ms2_spec_id_col = ms2_spec_id_col,
                                                           min_spectra = min_spectra,
                                                           cos_tol = cos_tol,
                                                           percentile = percentile,
                                                           slice_id = slice_id,
                                                           ms2Folder = ms2Folder,
                                                           ToAdd = ToAdd,
                                                           Norm2One = Norm2One,
                                                           Intensity_to_explain = Intensity_to_explain)  
        
        return [feature_cluster_data, 0]
        
    feature_cluster_data = CosineSamplingOverlappingClustering(All_FeaturesTable = All_FeaturesTable,
                                                               Feature_module = Feature_module,
                                                               sample_id_col = sample_id_col,
                                                               SamplesNames = SamplesNames,
                                                               ms2_spec_id_col = ms2_spec_id_col,
                                                               min_spectra = min_spectra,
                                                               cos_tol = cos_tol,
                                                               percentile = percentile,
                                                               slice_id = slice_id,
                                                               ms2Folder = ms2Folder,
                                                               ToAdd = ToAdd,
                                                               Norm2One = Norm2One,
                                                               percentile_mz = percentile_mz,
                                                               percentile_Int = percentile_Int,
                                                               SamplingTimes = SamplingTimes,
                                                               Intensity_to_explain = Intensity_to_explain)
    
    
    return [feature_cluster_data, 1]