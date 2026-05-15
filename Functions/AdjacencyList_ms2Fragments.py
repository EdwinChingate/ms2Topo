from __future__ import annotations

import numpy as np

def AdjacencyList_ms2Fragments(All_ms2,
                               std_distance = 3,
                               ppm_tol = 20):
    mzVec = All_ms2[:, 0]
    mz_stdVec = All_ms2[:, 1]
    mz_std_edgeVec = np.minimum(mz_stdVec * std_distance,
                                ppm_tol / 1e6 * mzVec)
    N_fragments = len(All_ms2[:, 0])
    mzMaxVec = mzVec + mz_std_edgeVec
    mzMinVec = mzVec - mz_std_edgeVec
    AdjacencyList = []
    frag_ids = []
    for feat_id in np.arange(N_fragments):
        mz = mzVec[feat_id]
        mz_std_edge = mz_std_edgeVec[feat_id] 
        min_mz = mz - mz_std_edge
        max_mz = mz + mz_std_edge        
        NearFilter = (mzMaxVec > min_mz) & (mzMinVec < max_mz)
        Neigbours = np.where(NearFilter)[0]    
        AdjacencyList.append(Neigbours)
        if len(Neigbours) > 0:
            frag_ids.append(feat_id)
    frag_ids = set(frag_ids)
    return [AdjacencyList, frag_ids]