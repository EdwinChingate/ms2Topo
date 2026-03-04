from __future__ import annotations
import numpy as np
def FeatureClusterCentroids(feature_cluster_data):

    Modules, Feature_Module, IntramoduleSimilarity, This_Module_FeaturesTable, AlignedFragmentsMat, AlignedFragments_mz_Mat = feature_cluster_data

    N_Fragments = AlignedFragmentsMat.shape[0]  # ← ADDED: was undefined
    N_modules = len(Modules)

    CentroidsAlignedFragmentsMat = np.zeros((N_Fragments, N_modules + 1))
    CentroidsAlignedFragmentsMat[:, 0] = AlignedFragmentsMat[:, 0]
    
    for module_id in np.arange(N_modules):       
        module = Modules[module_id]
        MeanVec = np.mean(AlignedFragmentsMat[:, 1:][:, module], axis = 1)
        CentroidsAlignedFragmentsMat[:, module_id + 1] = MeanVec

    return CentroidsAlignedFragmentsMat
