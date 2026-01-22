import numpy as np
from maxSimLoc import *
def MostPopularSpectrum(CosineMat):
    CosineList = list(CosineMat)
    maxSimLocVec = np.array(list(map(maxSimLoc,CosineList)))
    unique_values, counts = np.unique(maxSimLocVec, return_counts=True)
    maxCount = np.max(counts)
    loc = np.where(counts == maxCount)[0][0]
    HubId = int(unique_values[loc])
    return HubId
