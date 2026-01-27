import numpy as np
from DoubleCheckCurrentModuleSimilarity import *
def AdjacencyClustering(ms2_id,
                        AdjacencyList,
                        CosineMat,
                        AssignedNodes,
                        cos_tol = 0.9,
                        Module=[]):
    CurrentModule = set(AdjacencyList[ms2_id])
    CurrentModule = CurrentModule-set(Module)-set(AssignedNodes)   
    ActualConflictiveMembers = DoubleCheckCurrentModuleSimilarity(CurrentModule = CurrentModule,
                                                                  Module = Module,
                                                                  CosineMat = CosineMat,
                                                                  cos_tol = cos_tol)
    CurrentModule = CurrentModule-set(ActualConflictiveMembers) 
    Module = Module+list(CurrentModule)
    for ms2_id in CurrentModule: 
        Module = AdjacencyClustering(ms2_id = ms2_id,
                                     AdjacencyList = AdjacencyList,
                                     Module = Module,
                                     AssignedNodes = AssignedNodes,
                                     CosineMat = CosineMat)
    return Module
