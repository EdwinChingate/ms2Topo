import numpy as np
def ClusterInnerConflicts(CosineMat,
                          feature_module,
                          cos_tol = 0.9):    
    ConflictsMat = np.zeros((len(CosineMat[0,:]),len(CosineMat[0,:])))
    for spectra_id in feature_module:
        CosineVec = CosineMat[spectra_id,:]
        Conflict = np.where((CosineVec<cos_tol) & (CosineVec>0))[0]
        ConflictsMat[spectra_id,Conflict] = 1       
        ConflictsMat[Conflict,spectra_id] = 1   
    return ConflictsMat
