from __future__ import annotations
from SplitConflicts import *
import numpy as np

def AdjacencyList_from_matrix(N_ms2_spectra,
                              CosineMat,
                              cos_tol = 0):
    
    AdjacencyList = []
    ms2_ids = np.arange(N_ms2_spectra,dtype='int')
    
    for ms2_candidate_id in ms2_ids:
        Neigbours = np.where(CosineMat[ms2_candidate_id, :] > cos_tol)[0].tolist() + [int(ms2_candidate_id)]
        feature_module = SplitConflicts(CosineMat = CosineMat[np.ix_(Neigbours,
                                                                     Neigbours)],
                                        feature_module = np.arange(len(Neigbours)).tolist(),
                                        cos_tol = cos_tol)
        Neigbours = set(np.array(Neigbours).astype(int)[feature_module].tolist())
        AdjacencyList.append(Neigbours)
        
    ms2_ids = set(ms2_ids) 
    
    return [np.array(AdjacencyList), ms2_ids]
