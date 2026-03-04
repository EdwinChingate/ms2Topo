from __future__ import annotations
import numpy as np
def FormattingSummary(feature_cluster_data,
                      Explained_fractionInt,
                      slice_id):

    Modules, Feature_Module, IntramoduleSimilarity, All_FeaturesTable, AlignedFragmentsMat, AlignedFragments_mz_Mat = feature_cluster_data  # ← FIXED: Feature_module → Feature_Module (consistent naming)

    BigExplained_fractionIntVec = np.zeros(len(All_FeaturesTable)).reshape(-1, 1)
    BigExplained_fractionIntVec[Feature_Module] = Explained_fractionInt

    This_Module_FeaturesTable = np.hstack((All_FeaturesTable.copy(),
                                           BigExplained_fractionIntVec))
    This_Module_FeaturesTable = np.hstack((This_Module_FeaturesTable,
                                           slice_id * np.ones(len(BigExplained_fractionIntVec)).reshape(-1, 1)))
    
    BigAlignedFragmentsMat = np.zeros((AlignedFragmentsMat.shape[0],
                                       len(All_FeaturesTable) + 1))
    BigAlignedFragments_mz_Mat = np.zeros((AlignedFragmentsMat.shape[0],
                                           len(All_FeaturesTable) + 1))

    BigAlignedFragmentsMat[:, 0] = AlignedFragmentsMat[:, 0]
    BigAlignedFragments_mz_Mat[:, 0] = AlignedFragments_mz_Mat[:, 0]

    column_count = 1
    for spectra_id in Feature_Module:
        BigAlignedFragmentsMat[:, spectra_id + 1] = AlignedFragmentsMat[:, column_count]
        BigAlignedFragments_mz_Mat[:, spectra_id + 1] = AlignedFragments_mz_Mat[:, column_count]
        column_count += 1

    feature_cluster_data = [Modules,
                            Feature_Module,
                            IntramoduleSimilarity,
                            This_Module_FeaturesTable,
                            BigAlignedFragmentsMat,
                            BigAlignedFragments_mz_Mat]
    return feature_cluster_data
