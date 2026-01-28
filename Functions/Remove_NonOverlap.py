import numpy as np
from LeastSimilarNeighbour import *
def Remove_NonOverlap(Neighbours,
                      AdjacencyMatrix,
                      CosineMat):
    Sub_AdjacencyMatrix = AdjacencyMatrix[np.ix_(Neighbours,Neighbours)].copy()
    Sub_CosineMat = CosineMat[np.ix_(Neighbours,Neighbours)].copy()
    ConflictiveNeighbors = []
    NeighborhoodSize = len(Neighbours)
    for neighbour_1 in np.arange(NeighborhoodSize-1):
        for neighbour_2 in np.arange(neighbour_1+1,NeighborhoodSize):
            ConflictiveNeighbors += LeastSimilarNeighbour(module_id = NeighborhoodSize - 1,
                                                          neighbour_1 = neighbour_1,
                                                          neighbour_2 = neighbour_2,
                                                          CosineMat = Sub_CosineMat,
                                                          AdjacencyMatrix = Sub_AdjacencyMatrix)  
    ConflictiveNeighbors = list(set(ConflictiveNeighbors))
    OldNeighbours = Neighbours.copy()
    for conflictiveNeighbor in ConflictiveNeighbors:
        Neighbours.remove(OldNeighbours[conflictiveNeighbor])
    return [Neighbours,ConflictiveNeighbors]
