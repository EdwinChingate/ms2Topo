from __future__ import annotations
from FeatureClusterData import *
from Update_ids_FeatureModules import *

def ms2_FeaturesDifferences(All_FeaturesTable,
                            Feature_module,
                            SamplesNames,
                            AlignedSamplesList,
                            slice_id = 0,
                            sample_id_col = 16,
                            ms2_spec_id_col = 15,
                            ms2Folder = 'ms2_spectra',
                            ToAdd = 'mzML',
                            Norm2One = False,
                            cos_tol = 0.9,
                            Intensity_to_explain = 0.9,
                            min_spectra = 3,
                            percentile = 10,
                            percentile_mz = 5,
                            percentile_Int = 10,
                            SamplingTimes = 20,
                            Nspectra_sampling = 54,
                            max_Nspectra_cluster = 250,
                            feature_id = 0):    
    
    feature_cluster_data, sampling_samples = FeatureClusterData(All_FeaturesTable = All_FeaturesTable,
                                                                Feature_module = Feature_module,
                                                                Intensity_to_explain = Intensity_to_explain,
                                                                min_spectra = min_spectra,
                                                                cos_tol = cos_tol,
                                                                percentile = percentile,
                                                                slice_id = slice_id,
                                                                max_Nspectra_cluster = max_Nspectra_cluster,
                                                                Nspectra_sampling = Nspectra_sampling,
                                                                SamplingTimes = SamplingTimes,
                                                                SamplesNames = SamplesNames,
                                                                sample_id_col = sample_id_col,
                                                                ms2_spec_id_col = ms2_spec_id_col,
                                                                ms2Folder = ms2Folder,
                                                                ToAdd = ToAdd,
                                                                Norm2One = Norm2One,
                                                                percentile_mz = percentile_mz,
                                                                percentile_Int = percentile_Int)
    
    feature_id, AlignedSamplesList = Update_ids_FeatureModules(feature_cluster_data = feature_cluster_data,
                                                               AlignedSamplesList = AlignedSamplesList,
                                                               sample_id_col = sample_id_col,
                                                               ms2_spec_id_col = ms2_spec_id_col,
                                                               percentile_mz = percentile_mz,
                                                               percentile_Int = percentile_Int,
                                                               feature_id = feature_id,
                                                               min_spectra = min_spectra,
                                                               sampling_samples = sampling_samples,
                                                               SamplesNames = SamplesNames)
                                                               
    return [feature_id, AlignedSamplesList]