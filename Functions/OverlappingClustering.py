from CommunityBlocks import *
from IntramoduleSimilarityCalc import *
from CompressCosineMatrix import *
from AdjacentOverlappingModules import *
from CompactNeighbourhood import *
from UpdateModulesAfterClustering import *
def OverlappingClustering(Feature_Modules,
                          CosineMat,
                          percentile = 10):
    Modules = Feature_Modules.copy()
    modulesDif = 42
    while modulesDif > 0:
        IntramoduleSimilarity = IntramoduleSimilarityCalc(Modules = Modules,
                                                          CosineMat = CosineMat.copy(),
                                                          percentile = percentile)
        CompactCosineTen = CompressCosineMatrix(Modules = Modules,
                                                CosineMat = CosineMat.copy(),
                                                percentile = percentile)
        AdjacencyList,AdjacencyMatrix,module_ids = AdjacentOverlappingModules(Modules = Modules,
                                                                              IntramoduleSimilarity = IntramoduleSimilarity,
                                                                              CompactCosineTen = CompactCosineTen)
        NewAdjacencyList,ConflictiveNeighborsList = CompactNeighbourhood(AdjacencyList = AdjacencyList.copy(),
                                                                         AdjacencyMatrix = AdjacencyMatrix.copy(),
                                                                         CosineMat = CompactCosineTen[:,:,1])        
        New_Modules = CommunityBlocks(AdjacencyList_Features = NewAdjacencyList)
        modulesDif = len(Modules) - len(New_Modules)        
        Modules = UpdateModulesAfterClustering(New_Modules = New_Modules,
                                               Modules = Modules)   
    return [IntramoduleSimilarity,CompactCosineTen,Modules,ConflictiveNeighborsList]
