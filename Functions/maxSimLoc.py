import numpy as np
def maxSimLoc(CosineVec):
    maxSim = np.max(CosineVec)
    loc = np.where(CosineVec == maxSim)[0][0]
    return int(loc)
