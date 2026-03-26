from __future__ import annotations
import numpy as np
from ConsensusSpectra import *
from FeatureModuleStats import *
from Write_ms2ids_and_Consensus_ms2Spectra import *

def ClosingModule(module,
                  AlignedFragments_mz_Mat,
                  AlignedFragmentsMat,
                  Feature_module,
                  feature_id,
                  All_FeaturesTable,
                  AlignedSamplesList,
                  SamplesNames,
                  IntramoduleCosineStatsVec,
                  sampling_samples = 0,
                  sample_id_col = 6,
                  ms2_spec_id_col = 0,
                  percentile_mz = 5,
                  percentile_Int = 10,
                  minSpectra = 3,
                  alpha = 0.01,
                  min_spectra = 3):
    
    npFeature_module = np.array(Feature_module)
    
    if len(module) < min_spectra:
        return [feature_id, AlignedSamplesList]
    
    consensus_spectraDF = ConsensusSpectra(module = module,
                                           min_spectra = min_spectra,
                                           AlignedFragmentsMat = AlignedFragmentsMat,
                                           AlignedFragments_mz_Mat = AlignedFragments_mz_Mat,
                                           percentile_mz = percentile_mz,
                                           percentile_Int = percentile_Int)  
    
    if len(consensus_spectraDF) == 0:
        return [feature_id, AlignedSamplesList] 
    
    Write_ms2ids_and_Consensus_ms2Spectra(feature_id = feature_id,
                                          feature_module = module,
                                          consensus_spectraDF = consensus_spectraDF,
                                          All_FeaturesTable = All_FeaturesTable,
                                          sample_id_col = sample_id_col,
                                          ms2_spec_id_col = ms2_spec_id_col,
                                          explained_Int_col = All_FeaturesTable.shape[1] - 2,
                                          summ_ms2_table_id_col = All_FeaturesTable.shape[1] - 3,
                                          module_id_col = All_FeaturesTable.shape[1] - 1)  
    
    AlignedSamplesVec = FeatureModuleStats(All_FeaturesTable = All_FeaturesTable,
                                           module = module,
                                           SamplesNames = SamplesNames,
                                           IntramoduleCosineStatsVec = IntramoduleCosineStatsVec,
                                           feature_id = feature_id,
                                           sampling_samples = sampling_samples)   
    
    AlignedSamplesList.append(AlignedSamplesVec)    
    feature_id += 1
    
    return [feature_id, AlignedSamplesList]
