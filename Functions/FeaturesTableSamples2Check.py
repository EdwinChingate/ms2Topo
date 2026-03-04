from __future__ import annotations
import numpy as np

def FeaturesTableSamples2Check(Feature_Module,
                               Original_Feature_module,
                               All_FeaturesTable,
                               sample_id_col = 6):  # ← ADDED: was hardcoded as [:, 6]
    
    # Samples already covered by sampling
    SampledFeatureTable = All_FeaturesTable[Feature_Module, :]
    Samples_ids_inFeatureCluster = set(np.array(SampledFeatureTable[:, sample_id_col],
                                                dtype='int').tolist())
    
    # All samples present in the ORIGINAL module (not all of All_FeaturesTable)
    OriginalFeatureTable = All_FeaturesTable[Original_Feature_module, :]
    All_samples_in_original = set(np.array(OriginalFeatureTable[:, sample_id_col],
                                           dtype='int').tolist())
    
    # Samples in original cluster but NOT covered by sampling
    Samples_ids2Check = list(All_samples_in_original - Samples_ids_inFeatureCluster)
    Samples_ids2Check.sort()
    Samples_ids2Check = [int(s) for s in Samples_ids2Check]
    
    N_samples = int(np.max(All_FeaturesTable[:, sample_id_col])) + 1  # ← FIXED: missing closing parenthesis + 1
    Samples_FeaturesIdsList = [[]] * N_samples
    
    # Search within ORIGINAL Feature_module, return row indices into All_FeaturesTable
    OriginalSamples_ids = np.array(OriginalFeatureTable[:, sample_id_col], dtype='int')
    Original_Feature_module_arr = np.array(Original_Feature_module)
    
    for sample_id in Samples_ids2Check:
        SampleFilter = np.where(OriginalSamples_ids == sample_id)[0]
        Samples_FeaturesIdsList[sample_id] = Original_Feature_module_arr[SampleFilter].tolist()
    
    return [Samples_FeaturesIdsList, Samples_ids2Check]
