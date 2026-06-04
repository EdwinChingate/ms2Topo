import numpy as np
from raw_gauss_seed import *
from redistribute_sampling import *
from smooth_data_and_find_peaks import *
from gauss_boundaries import *

def tools_gaussian_chrom(Chromatogram,
                       RT_col = 2,
                       int_col = 1,
                       MaxSignals = 100,
                       distance = 2):
    
    smooth_peaks,peaksMax = smooth_data_and_find_peaks(Chromatogram = Chromatogram,
                                                     MaxSignals = MaxSignals,
                                                     distance = distance)
    
    if len(peaksMax)==0:
        return [[],[],[]]
    
    L=len(smooth_peaks[:,1])
    
    SChrom = redistribute_sampling(PeakChr = Chromatogram,
                                  N_new = L,
                                  RT_col = RT_col,
                                  int_col = int_col)
    
    boundsMat = gauss_boundaries(smooth_peaks = smooth_peaks)
    ParametersMat = raw_gauss_seed(smooth_peaks = smooth_peaks,
                                 peaksMax = peaksMax,
                                 boundsMat = boundsMat)
    
    NPeaks = len(ParametersMat[:, 0])
    minVec = np.array([boundsMat[:, 0]] * NPeaks)
    maxVec = np.array([boundsMat[:, 1]] * NPeaks)
    minList = minVec.flatten()
    maxList = maxVec.flatten()
    bounds = (minList, maxList)
    
    ParametersList = ParametersMat.flatten()  
    
    return [SChrom,
            ParametersList,
            bounds]
