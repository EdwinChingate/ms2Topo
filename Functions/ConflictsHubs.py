import numpy as np
def ConflictsHubs(ConflictsMat,
                  conflict_spectra = -1):
    if conflict_spectra >= 0:        
        ConflictsMat[:,conflict_spectra] = 0
        ConflictsMat[conflict_spectra,:] = 0
    ConflictVec = np.sum(ConflictsMat,axis=1)
    return [ConflictVec,ConflictsMat]
