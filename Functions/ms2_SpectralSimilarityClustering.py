from __future__ import annotations
from AdjacencyListFeatures import *
from ms2_FeaturesDifferences import *
from ms2_feat_modules import *
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
    Columns = ['median_mz(Da)',
               'min_mz',
               'max_mz',
               'IQR_mz(ppm)',
               'SamplingSamples',
               'N_samples',
               'N_ms2-spectra',
               'min_CosSim',
               'Q1_CosSim',
               'median_CosSim',
               'Q3_CosSim',
               'max_CosSim',
               'median_RT(s)',
               'Q1_RT(s)',
               'Q3_RT(s)',
               'min_RT(s)',
               'max_RT(s)',
               'feat_id']
    Columns = Columns + SamplesNames 
    AlignedSamplesDF = pd.DataFrame(AlignedSamplesList,columns = Columns)
    return [AlignedSamplesDF, feature_id]
