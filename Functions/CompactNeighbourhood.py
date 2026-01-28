from Remove_NonOverlap import *
def CompactNeighbourhood(AdjacencyList,
                         AdjacencyMatrix,
                         CosineMat):
    NewAdjacencyList = []
    ConflictiveNeighborsList = []
    for Neighbours in AdjacencyList:
        NewNeighbours,ConflictiveNeighbors = Remove_NonOverlap(Neighbours = Neighbours,
                                                               AdjacencyMatrix = AdjacencyMatrix,
                                                               CosineMat = CosineMat)
        NewAdjacencyList.append(NewNeighbours)
        ConflictiveNeighborsList.append(ConflictiveNeighbors)
    return [NewAdjacencyList,ConflictiveNeighborsList]
