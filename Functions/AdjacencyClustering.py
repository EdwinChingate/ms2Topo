from __future__ import annotations

def AdjacencyClustering(ms2_id,AdjacencyList,Module=[]):
    CurrentModule=set(AdjacencyList[ms2_id])
    CurrentModule=CurrentModule-set(Module)   
    Module=Module+list(CurrentModule)
    for ms2_id in CurrentModule: 
        Module=AdjacencyClustering(ms2_id=ms2_id,AdjacencyList=AdjacencyList,Module=Module)
    return Module