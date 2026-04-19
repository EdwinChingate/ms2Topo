from __future__ import annotations
from CosineOverlappingClustering import *
from SummarizeSampling import *
import numpy as np

def CosineSamplingOverlappingClustering(Feature_module,
                                        All_FeaturesTable,
                                        SamplesNames,
                                        Intensity_to_explain = 0.9,
                                        percentile_mz = 5,
                                        percentile_Int = 10,
                                        Spectra_idVec = [],
                                        All_ms2 = [],
                                        sample_id_col = 16,
                                        ms2_spec_id_col = 15,
                                        min_spectra = 3,
                                        cos_tol = 0.9,
                                        percentile = 10,
                                        slice_id = 0,
                                        Nspectra_sampling = 54,
                                        SamplingTimes = 20,
                                        ms2Folder = 'ms2_spectra',
                                        ToAdd = 'mzML',
                                        Norm2One = False):
    feature_clusterList = []
    sampling = 0
    max_attempts = SamplingTimes * 5 
    attempts = 0

    while sampling < SamplingTimes and attempts < max_attempts:
        attempts += 1
        rng = np.random.default_rng()
        Sample_Feature_module = rng.choice(Feature_module,
                                           size = Nspectra_sampling,
                                           replace = False)
        feature_cluster_data = CosineOverlappingClustering(All_FeaturesTable = All_FeaturesTable,
                                                           Feature_module = Sample_Feature_module,
                                                           sample_id_col = sample_id_col,
                                                           ms2_spec_id_col = ms2_spec_id_col,
                                                           SamplesNames = SamplesNames,
                                                           Intensity_to_explain = Intensity_to_explain,
                                                           min_spectra = min_spectra,
                                                           cos_tol = cos_tol,
                                                           percentile = percentile,
                                                           slice_id = slice_id,
                                                           ms2Folder = ms2Folder,
                                                           ToAdd = ToAdd,
                                                           Norm2One = Norm2One)               
        if len(feature_cluster_data) > 0:         
            feature_clusterList.append(feature_cluster_data)   
            sampling += 1

    if len(feature_clusterList) == 0:
        return []

    feature_cluster_data = SummarizeSampling(feature_clusterList = feature_clusterList,
                                             All_FeaturesTable = All_FeaturesTable.copy(),
                                             Original_Feature_module = Feature_module,
                                             SamplesNames = SamplesNames,
                                             Intensity_to_explain = Intensity_to_explain,
                                             min_spectra = min_spectra,
                                             cos_tol = cos_tol,
                                             percentile = percentile,
                                             slice_id = slice_id,
                                             sample_id_col = sample_id_col,
                                             ms2_spec_id_col = ms2_spec_id_col,
                                             percentile_mz = percentile_mz,
                                             percentile_Int = percentile_Int,
                                             ms2Folder = ms2Folder,
                                             ToAdd = ToAdd,
                                             Norm2One = Norm2One)    

    return feature_cluster_data