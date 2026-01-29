import numpy as np
def AdjacentOverlappingModules(IntramoduleSimilarity,
                               CompactCosineTen):
    N_modules = len(CompactCosineTen[:,:,0])
    AdjacencyMatrix = np.zeros((N_modules,N_modules))
    AdjacencyList = []
    module_ids = []
    for module_id in np.arange(N_modules):    
        LowIntramoduleSimmilarity = IntramoduleSimilarity[module_id,1]
        maxSimNeighborsVec = CompactCosineTen[module_id,:,2]
        Neighbours = np.where(maxSimNeighborsVec > LowIntramoduleSimmilarity)[0].tolist()
        AdjacencyList.append(Neighbours+[int(module_id)])
        AdjacencyMatrix[module_id,Neighbours] = 1            
        module_ids.append(int(module_id))
    module_ids = set(module_ids)        
    return [AdjacencyList,AdjacencyMatrix,module_ids]
