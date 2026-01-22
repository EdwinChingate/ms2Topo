import numpy as np
from UpdateMaxSimAdjacencyList import *
def FillMaxSimAdjacencyList(MaxSimAdjacencyList,
                            ZeroRow,
                            ClusterRow,
                            CosineMat):
    ZeroRowNeighbors = MaxSimAdjacencyList[ZeroRow][0]+[ClusterRow]
    ClusterRowNeighbors = MaxSimAdjacencyList[ClusterRow][0]+[ZeroRow]    
    AllNeighbors = list(set(ZeroRowNeighbors+ClusterRowNeighbors))
    CleanCentroid = np.delete(CosineMat[ClusterRow,:].copy(),AllNeighbors)        
    # this is the average inter-cluster similarity
    MaxSimAdjacencyList[ClusterRow][2] = float(np.mean(CleanCentroid))
    
    MaxSimAdjacencyList = UpdateMaxSimAdjacencyList(MaxSimAdjacencyList = MaxSimAdjacencyList,
                                                    AllNeighbors = AllNeighbors)
    return MaxSimAdjacencyList
