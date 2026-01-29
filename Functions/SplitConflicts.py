import numpy as np
from ClusterInnerConflicts import *
from ConflictsHubs import *
def SplitConflicts(CosineMat,
                   feature_module,
                   cos_tol = 0.9):
    ConflictsMat = ClusterInnerConflicts(CosineMat = CosineMat,
                                         feature_module = feature_module,
                                         cos_tol = cos_tol)
    ConflictiveNodes = []
    ConflictVec,ConflictsMat = ConflictsHubs(ConflictsMat = ConflictsMat)
    while sum(ConflictVec) > 0:
        MostConflicts = np.max(ConflictVec)
        MostConflictive = int(np.where(ConflictVec == MostConflicts)[0][0])        
        ConflictiveNodes.append(MostConflictive)
        ConflictVec,ConflictsMat = ConflictsHubs(ConflictsMat = ConflictsMat,
                                                 conflict_spectra = MostConflictive)
    if len(ConflictiveNodes) > 0:
        feature_module = list(set(feature_module) - set(ConflictiveNodes))
    return feature_module
