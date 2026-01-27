import numpy as np
def DoubleCheckCurrentModuleSimilarity(CurrentModule,
                                       Module,
                                       CosineMat,
                                       cos_tol = 0.9):
    if (len(Module) == 0) or (len(CurrentModule) == 0):
        return set([])
    SimilarityMatrix = CosineMat[np.ix_(list(CurrentModule),list(Module))]
    CheckSimilarityMatrix = np.array(np.where(SimilarityMatrix < cos_tol))
    ConflictiveMembers = list(set(CheckSimilarityMatrix[0,:]))    
    ActualConflictiveMembers = set(list(np.array(list(CurrentModule))[ConflictiveMembers]))
    ActualConflictiveMembers = [int(conflict) for conflict in ActualConflictiveMembers]
    return ActualConflictiveMembers
