import numpy as np
def JaccardFragmentsSimilarity(OverlappingSpectraVec):
    intersectionSpectraLoc = np.where(OverlappingSpectraVec > 1)[0]
    intersectionSpectra = sum(OverlappingSpectraVec[intersectionSpectraLoc])/2
    unionSpectra = sum(OverlappingSpectraVec) - intersectionSpectra
    JaccardSim = float(intersectionSpectra/unionSpectra)
    return JaccardSim
