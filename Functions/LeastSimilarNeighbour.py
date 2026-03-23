from __future__ import annotations
def LeastSimilarNeighbour(module_id,
                          neighbour_1,
                          neighbour_2,
                          CosineMat,
                          AdjacencyMatrix):
                          
    checkSum = AdjacencyMatrix[neighbour_1, neighbour_2] + AdjacencyMatrix[neighbour_2, neighbour_1]
    
    if checkSum > 1:
        return []
        
    if module_id == neighbour_1:
        return [int(neighbour_2)]
    elif module_id == neighbour_2:
        return [int(neighbour_1)]
        
    sim_1 = CosineMat[module_id, neighbour_1]
    sim_2 = CosineMat[module_id, neighbour_2]
    
    if sim_1 > sim_2:
        return [int(neighbour_2)]
    else:
        return [int(neighbour_1)]
