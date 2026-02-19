import numpy as np
import pandas as pd
from ConsensusSpectra import *
#from Write_ms2ids_and_Consensus_ms2Spectra import *
#from FeatureModuleStats import *
def ClosingModule(module,
                  Modules,
                  AlignedFragments_mz_Mat,
                  AlignedFragmentsMat,
                  Feature_module,
                  feature_id,
                  All_FeaturesTable,
                  AlignedSamplesList,
                  SamplesNames,
                  sample_id_col = 6,
                  ms2_spec_id_col = 0,
                  percentile_mz = 5,
                  percentile_Int = 10,
                  minSpectra = 3,
                  alpha = 0.01,
                  min_spectra = 3):
    npFeature_module = np.array(Feature_module)
    if len(module) < min_spectra:
        return [Modules, feature_id, AlignedSamplesList]
    consensus_spectraDF = ConsensusSpectra(module = module,
                                           min_spectra = min_spectra,
                                           AlignedFragmentsMat = AlignedFragmentsMat,
                                           AlignedFragments_mz_Mat = AlignedFragments_mz_Mat,
                                           percentile_mz = percentile_mz,
                                           percentile_Int = percentile_Int)  
    if len(consensus_spectraDF) == 0:
        return [Modules, feature_id, AlignedSamplesList]   
    feature_module = npFeature_module[module].tolist()    
    Modules.append(feature_module)
    Write_ms2ids_and_Consensus_ms2Spectra(feature_id = feature_id,
                                          feature_module = module,
                                          consensus_spectraDF = consensus_spectraDF,
                                          All_FeaturesTable = All_FeaturesTable,
                                          sample_id_col = sample_id_col,
                                          ms2_spec_id_col = ms2_spec_id_col,
                                          explained_Int_col = All_FeaturesTable.shape[1] - 1)    
    AlignedSamplesVec = FeatureModuleStats(All_FeaturesTable = All_FeaturesTable,
                                           module = module,
                                           SamplesNames = SamplesNames,
                                           feature_id = feature_id)   
    AlignedSamplesList.append(AlignedSamplesVec)    
    feature_id += 1
    return [Modules, feature_id, AlignedSamplesList]
