from AdjacencyClustering import *
def ms2_CosModules(AdjacencyList,
                   ms2_ids,
                   CosineMat):
    Modules=[]
    AssignedNodes = []
    while len(ms2_ids) > 0:        
        ms2_candidate_id=list(ms2_ids)[0]
        module = AdjacencyClustering(ms2_id = ms2_candidate_id,
                                     AdjacencyList = AdjacencyList,
                                     CosineMat = CosineMat,
                                     AssignedNodes = AssignedNodes)
        ms2_ids = ms2_ids-set(module)
        Modules.append(module)
        AssignedNodes += module
    return Modules
