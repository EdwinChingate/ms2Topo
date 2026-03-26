from __future__ import annotations
from CompressCosineMatrix import *
from IntramoduleSimilarityCalc import *
from explore_similarity_overlapping import *

def silhouette_overlap_merging(CosineMat,
                               modules,
                               silhouette_vector,
                               percentile,
                               cos_tol):
    
    n_modules = len(modules)
    
    IntramoduleSimilarity = IntramoduleSimilarityCalc(Modules = modules,
                                                      CosineMat = CosineMat.copy(),
                                                      percentile = percentile)
    
    CompactCosineTen = CompressCosineMatrix(Modules = modules,
                                            CosineMat = CosineMat.copy(),
                                            percentile = percentile)
    
    modules, silhouette_vector, modules_explored_count = explore_similarity_overlapping(modules = modules,
                                                                                        silhouette_vector = silhouette_vector,
                                                                                        IntramoduleSimilarity = IntramoduleSimilarity,
                                                                                        CompactCosineTen = CompactCosineTen,
                                                                                        CosineMat = CosineMat,
                                                                                        cos_tol = cos_tol)
    
    if modules_explored_count == n_modules:
        return [modules, silhouette_vector, CompactCosineTen, IntramoduleSimilarity]
        
    modules, silhouette_vector, CompactCosineTen, IntramoduleSimilarity = silhouette_overlap_merging(CosineMat = CosineMat,
                                                                                                     silhouette_vector = silhouette_vector,
                                                                                                     modules = modules,
                                                                                                     percentile = percentile,
                                                                                                     cos_tol = cos_tol) 
    
    return [modules, silhouette_vector, CompactCosineTen, IntramoduleSimilarity]