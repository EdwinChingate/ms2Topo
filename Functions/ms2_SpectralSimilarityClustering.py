from __future__ import annotations
from AdjacencyListFeatures import *
from ms2_FeaturesDifferences import *
from ms2_feat_modules import *
import numpy as np
import pandas as pd

def ms2_SpectralSimilarityClustering(SummMS2_raw,
                                     SampleName = '',
                                     SamplesNames = [],
                                     slice_id = 0,
                                     feature_id = 0,
                                     mz_col = 1,
                                     RT_col = 2,
                                     RT_tol = 20,
                                     mz_Tol = 1e-2,
                                     sample_id_col = -1,
                                     ms2_spec_id_col = 0,
                                     ms2Folder = 'ms2_spectra',
                                     ToAdd = 'mzML',
                                     cos_tol = 0.9,
                                     Norm2One = False,
                                     max_Nspectra_cluster = 250,
                                     Nspectra_sampling = 100):
    
    if len(SamplesNames) == 0:
        SamplesNames = [SampleName]
        
    AdjacencyList, feat_ids = AdjacencyListFeatures(MS2_features = SummMS2_raw,
                                                    mz_col = mz_col,
                                                    RT_col = RT_col,
                                                    RT_tol = RT_tol,
                                                    mz_Tol = mz_Tol)
    
    RawModules = ms2_feat_modules(AdjacencyList = AdjacencyList,
                                  ms2_ids = feat_ids)
    AlignedSamplesList = []
    N_raw_modules = len(RawModules)
    print(N_raw_modules)
    for feature_module_id in np.arange(N_raw_modules):
        Feature_module = RawModules[feature_module_id]   
       # print(len(Feature_module))
       # print(np.min(SummMS2_raw[Feature_module, 1]), np.max(SummMS2_raw[Feature_module, 1]))
        feature_id, AlignedSamplesList = ms2_FeaturesDifferences(All_FeaturesTable = SummMS2_raw,
                                                                 Feature_module = Feature_module,
                                                                 AlignedSamplesList = AlignedSamplesList,
                                                                 SamplesNames = SamplesNames,
                                                                 sample_id_col = sample_id_col,
                                                                 ms2_spec_id_col = ms2_spec_id_col,
                                                                 ms2Folder = ms2Folder,
                                                                 ToAdd = ToAdd,
                                                                 cos_tol = cos_tol,
                                                                 Norm2One = Norm2One,
                                                                 feature_id = feature_id,
                                                                 slice_id = slice_id)
       # ShowDF(AlignedSamplesList)
        
    feature_descriptor_columns = ['median_mz(Da)',
                                  'min_mz',
                                  'max_mz',
                                  'IQR_mz(ppm)',
                                  'SamplingSamples',
                                  'N_samples',
                                  'N_ms2-spectra',
                                  'min_silhouette',
                                  'Q1_silhouette',
                                  'median_silhouette',
                                  'Q3_silhouette',
                                  'max_silhouette',
                                  'median_RT(s)',
                                  'Q1_RT(s)',
                                  'Q3_RT(s)',
                                  'min_RT(s)',
                                  'max_RT(s)',
                                  'feat_id']
    
    all_columns = feature_descriptor_columns + SamplesNames 
    AlignedSamplesDF = pd.DataFrame(AlignedSamplesList,
                                    columns = all_columns)
    return_columns = np.array(feature_descriptor_columns)[[0, 3, 13, 12, 14, 5, 6, 4, 8, 9, 10, 7, 11, 1, 2, 15, 16, 17]].tolist() + SamplesNames 
    
    return [AlignedSamplesDF[np.array(return_columns)], feature_id]