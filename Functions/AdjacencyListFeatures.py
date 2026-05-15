from __future__ import annotations

import numpy as np

def AdjacencyListFeatures(MS2_features,
                          mz_col = 3,
                          mz_CI_col = 8,
                          RT_col = 2,
                          minRT_col = 12,
                          maxRT_col = 13,
                          RT_tol = 0,
                          mz_Tol = 0):
    N_possible_feat = len(MS2_features[:,0])
    if mz_Tol == 0:
        mz_CI_Vec = MS2_features[:,mz_CI_col]
    else:
        mz_CI_Vec = np.ones(N_possible_feat)*mz_Tol
    mzVec = MS2_features[:,mz_col]
    mzMaxVec = mzVec+mz_CI_Vec
    mzMinVec = mzVec-mz_CI_Vec
    if RT_tol == 0:
        RTMaxVec = MS2_features[:,maxRT_col]
        RTMinVec = MS2_features[:,minRT_col]
    else:
        RTMaxVec = MS2_features[:,RT_col]+RT_tol
        RTMinVec = MS2_features[:,RT_col]-RT_tol
    AdjacencyList = []
    feat_ids = []
    for feat_id in np.arange(N_possible_feat):
        min_mz = mzMinVec[feat_id]
        max_mz = mzMaxVec[feat_id]
        min_RT = RTMinVec[feat_id]
        max_RT = RTMaxVec[feat_id]       
        NearFilter = (mzMaxVec >= min_mz) & (mzMinVec <= max_mz) & (RTMaxVec >= min_RT) & (RTMinVec <= max_RT)
        Neigbours = np.where(NearFilter)[0]    
        AdjacencyList.append(Neigbours)
        if len(Neigbours) > 0:
            feat_ids.append(feat_id)
    feat_ids = set(feat_ids)
    return [AdjacencyList,feat_ids]