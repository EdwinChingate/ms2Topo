from __future__ import annotations

from AdjacencyClustering import *

def ms2_feat_modules(AdjacencyList,ms2_ids):
    Modules=[]
    while len(ms2_ids)>0:        
        ms2_candidate_id=list(ms2_ids)[0]
        module=AdjacencyClustering(ms2_id=ms2_candidate_id,AdjacencyList=AdjacencyList)
        ms2_ids=ms2_ids-set(module)
        Modules.append(module)
    return Modules