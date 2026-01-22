def UpdateCosineMat(CosineMat,
                    ZeroRow,
                    ClusterRow,
                    MaxSimAdjacencyList):
    N_membersZeroRow = len(MaxSimAdjacencyList[ZeroRow][0])
    N_membersClusterRow = len(MaxSimAdjacencyList[ClusterRow][0])
    N_members = N_membersZeroRow+N_membersClusterRow
    ZeroVec = CosineMat[ZeroRow,:]
    ClusterVec = CosineMat[ClusterRow,:]
    Centroid = (N_membersZeroRow*ZeroVec+N_membersClusterRow*ClusterVec)/N_members
    Centroid[ClusterRow] = 0
    CosineMat[ClusterRow,:] = Centroid
    CosineMat[:,ClusterRow] = Centroid
    CosineMat[ZeroRow,:] = 0
    CosineMat[:,ZeroRow] = 0
    return CosineMat
