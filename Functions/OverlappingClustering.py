from RefineCoherence import *
from ms2_feat_modules import *
from IntramoduleSimilarityCalc import *
from CompressCosineMatrix import *
from AdjacentOverlappingModules import *
#from UpdateModulesAfterClustering import *
def OverlappingClustering(Feature_Modules,
                          CosineMat,
                          percentile = 10,
                          cos_tol = 0.9):
    Modules = RefineCoherence(Feature_Modules = Feature_Modules,
                              CosineMat = CosineMat.copy(),
                              cos_tol = cos_tol)
    modulesDif = 7
    while modulesDif > 0:
        IntramoduleSimilarity = IntramoduleSimilarityCalc(Modules = Modules,
                                                          CosineMat = CosineMat.copy(),
                                                          percentile = percentile)
        CompactCosineTen = CompressCosineMatrix(Modules = Modules,
                                                CosineMat = CosineMat.copy(),
                                                percentile = percentile)
        AdjacencyList,module_ids = AdjacentOverlappingModules(Modules = Modules,
                                                              IntramoduleSimilarity = IntramoduleSimilarity,
                                                              CompactCosineTen = CompactCosineTen)
        #I need to add a sanity check to prevent merging of two quite different clusters because of a node in the middle
        New_Modules = ms2_feat_modules(AdjacencyList = AdjacencyList,
                                       ms2_ids=module_ids)
        modulesDif = len(Modules) - len(New_Modules)
        Modules = UpdateModulesAfterClustering(New_Modules = New_Modules,
                                               Modules = Modules)   
    return [IntramoduleSimilarity,CompactCosineTen,Modules]
