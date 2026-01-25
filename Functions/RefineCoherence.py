import numpy as np
from SplitConflicts import *
from SplitModules import *
def RefineCoherence(Feature_Modules,
                    CosineMat,
                    cos_tol = 0.9):
    Modules = []
    for Feature_module in Feature_Modules:
        feature_module,ConflictiveNodes = SplitConflicts(CosineMat = CosineMat[np.ix_(Feature_module,Feature_module)],
                                                         feature_module = np.arange(len(Feature_module)).tolist(),
                                                         cos_tol = cos_tol)
        Modules += SplitModules(Feature_module = Feature_module,
                                feature_module = feature_module,
                                ConflictiveNodes = ConflictiveNodes)
    return Modules
