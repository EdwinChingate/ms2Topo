from __future__ import annotations
from CosClusteringEngine import *
from Retrieve_and_Join_ms2_for_feature import *
import numpy as np

def CosineOverlappingClustering(Feature_module,
                                All_FeaturesTable,
                                SamplesNames,
                                Intensity_to_explain = 0.9,
                                Spectra_idVec = [],
                                All_ms2 = [],
                                sample_id_col = 16,
                                ms2_spec_id_col = 15,
                                min_spectra = 3,
                                cos_tol = 0.9,
                                percentile = 10,
                                slice_id = 0,
                                ms2Folder = 'ms2_spectra',
                                ToAdd = 'mzML',
                                Norm2One = False):   
    if len(Spectra_idVec) == 0:
        All_ms2, Spectra_idVec = Retrieve_and_Join_ms2_for_feature(All_FeaturesTable = All_FeaturesTable,
                                                                   Feature_module = Feature_module,
                                                                   SamplesNames = SamplesNames,
                                                                   sample_id_col = sample_id_col,
                                                                   ms2_spec_id_col = ms2_spec_id_col,
                                                                   ms2Folder = ms2Folder,
                                                                   ToAdd = ToAdd,
                                                                   Norm2One = Norm2One)
    if len(All_ms2) == 0:
        return []
    Feature_module = np.array(Feature_module)[Spectra_idVec].tolist()
    feature_cluster_data = CosClusteringEngine(All_FeaturesTable = All_FeaturesTable,
                                               All_ms2 = All_ms2,
                                               Feature_module = Feature_module,
                                               slice_id = slice_id,
                                               Intensity_to_explain = Intensity_to_explain,
                                               min_spectra = min_spectra,
                                               cos_tol = cos_tol,
                                               percentile = percentile)
    
    return feature_cluster_data