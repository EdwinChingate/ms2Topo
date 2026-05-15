from __future__ import annotations

import numpy as np
from FlatMatrix_woDiag import *

def IntramoduleCosineStats(moduleCosineMat,
                           percentile = 10):
    n = moduleCosineMat.shape[0]
    if n == 1:
        return [1, 1, 1, 1, 1, 1]
    CosineArray = FlatMatrix_woDiag(matrix = moduleCosineMat,
                                    n = n)
    median_CosSim = np.median(CosineArray)
    if len(CosineArray) > 1:        
        min_CosSim = np.percentile(CosineArray,
                                   percentile)
        max_CosSim = np.percentile(CosineArray,
                                   100 - percentile)
        Q1_CosSim = np.percentile(CosineArray,
                               25)
        Q3_CosSim = np.percentile(CosineArray,
                               75)           
    else:
        min_CosSim = median_CosSim
        max_CosSim = median_CosSim
        Q1_CosSim = median_CosSim
        Q3_CosSim = median_CosSim
 
    IntramoduleCosineStatsList = [n,
                                  min_CosSim,
                                  Q1_CosSim,
                                  median_CosSim,
                                  Q3_CosSim,
                                  max_CosSim]
    return IntramoduleCosineStatsList