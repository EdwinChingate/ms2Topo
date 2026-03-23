from __future__ import annotations
from merge_full_overlapping import *
from silhouette_merging import *

def silhouette_overlapping(AdjacencyList_Features,
                           CosineMat):
    
    merged_modules = merge_full_overlapping(modules = AdjacencyList_Features)
    modules = silhouette_merging(CosineMat = CosineMat,
                                 modules = merged_modules)
    
    return modules