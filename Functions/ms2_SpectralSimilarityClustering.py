from __future__ import annotations
from AdjacencyListFeatures import *
from ms2_FeaturesDifferences import *
from ms2_feat_modules import *
import numpy as np

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
    
    for feature_module_id in np.arange(N_raw_modules):
        Feature_module = RawModules[feature_module_id]        
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


#from ms2_SamplesAligment import *

def ms2_SamplesAligment(ProjectName,
                        All_SummMS2Table,
                        EdgesMat,
                        SamplesNames,
                        RT_tol = 30,
                        mz_Tol = 2e-3,
                        feature_id = 0,
                        cos_tol = 0.8,
                        min_N_ms2_spectra = 3,
                        ToReplace = 'mzML-ms2Summary.xlsx',
                        ms2Folder = 'ms2_spectra',
                        ToAdd = 'mzML',
                        Norm2One = True):
                        
    for Low_id_mz, High_id_mz, slice_id in EdgesMat:
        SummMS2_raw = All_SummMS2Table[Low_id_mz: High_id_mz, :]
        AlignedSamplesDF, feature_id = ms2_SpectralSimilarityClustering(SummMS2_raw = SummMS2_raw,
                                                                        SamplesNames = SamplesNames,
                                                                        feature_id = feature_id,
                                                                        slice_id = slice_id,
                                                                        mz_col = 1,
                                                                        RT_col = 2,
                                                                        RT_tol = RT_tol,
                                                                        mz_Tol = mz_Tol,
                                                                        sample_id_col = 6,
                                                                        ms2_spec_id_col = 0,
                                                                        ms2Folder = ms2Folder,
                                                                        ToAdd = ToAdd,
                                                                        cos_tol = cos_tol,
                                                                        Norm2One = Norm2One)     
        TableLoc = ProjectName + '-' + str(slice_id) + '.csv'
        #AlignedSamplesDF.to_csv(TableLoc)
    return AlignedSamplesDF        
    
    
                                                            

                