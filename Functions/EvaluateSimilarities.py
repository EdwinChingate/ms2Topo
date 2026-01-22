import numpy as np
def EvaluateSimilarities(CosineMat,MaxSimAdjacencyList,ClusterRow,ZeroRow):    
    ClusterMembers = MaxSimAdjacencyList[ClusterRow][0]
    ClusterCoherence = MaxSimAdjacencyList[ClusterRow][1]
    ClusterExternalAffinity = MaxSimAdjacencyList[ClusterRow][2]
    NewMemberCosineVec = CosineMat[ZeroRow,:]    
    NodesSet = set(np.arange(len(NewMemberCosineVec),dtype='int').tolist())
    NewClusterCoherence = min(list(NewMemberCosineVec[ClusterMembers]).append(ClusterCoherence))
    NoNeighborsSet = NodesSet - set(list(NewMemberCosineVec[ClusterMembers]))
    NewClusterExternalAffinity = max(list(NewMemberCosineVec[NoNeighborsSet]).append(ClusterExternalAffinity))    
    Contrast = NewClusterCoherence-NewClusterExternalAffinity
    merge = Constrast>0
    if merge:
        MaxSimAdjacencyList[ClusterRow][0].append(ZeroRow)
        MaxSimAdjacencyList[ClusterRow][1] = NewClusterCoherence
        MaxSimAdjacencyList[ClusterRow][2] = NewClusterExternalAffinity
    else:
        CosineMat[ClusterRow,ZeroRow] = 0
        CosineMat[ZeroRow,ClusterRow] = 0
    return [merge,CosineMat,MaxSimAdjacencyList]
    
