from __future__ import annotations
from CompressCosineMatrix import *
from IntramoduleSimilarityCalc import *
from ShowDF import *
from explore_similarity_overlapping import *

def silhouette_overlap_merging(CosineMat,
                               modules,
                               current_silhouette,
                               percentile,
                               cos_tol):
    
    n_modules = len(modules)
    
    IntramoduleSimilarity = IntramoduleSimilarityCalc(Modules = modules,
                                                      CosineMat = CosineMat.copy(),
                                                      percentile = percentile)
    
    CompactCosineTen = CompressCosineMatrix(Modules = modules,
                                            CosineMat = CosineMat.copy(),
                                            percentile = percentile)
    
    modules, current_silhouette, modules_explored_count = explore_similarity_overlapping(modules = modules,
                                                                                         current_silhouette = current_silhouette,
                                                                                         IntramoduleSimilarity = IntramoduleSimilarity,
                                                                                         CompactCosineTen = CompactCosineTen,
                                                                                         CosineMat = CosineMat,
                                                                                         cos_tol = cos_tol)
    
    if modules_explored_count == n_modules:
        return [modules, IntramoduleSimilarity, CompactCosineTen]
        
    modules, IntramoduleSimilarity, CompactCosineTen = silhouette_overlap_merging(CosineMat = CosineMat,
                                                                                  current_silhouette = current_silhouette,
                                                                                  modules = modules,
                                                                                  percentile = percentile,
                                                                                  cos_tol = cos_tol) 
    
    return [modules, IntramoduleSimilarity, CompactCosineTen]
