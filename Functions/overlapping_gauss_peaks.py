import numpy as np
from ChromGaussPeak import *
def OverlappingGaussPeaks(RT_vec,ParametersMat,stdDistance=3):
    NPeaks=int(len(ParametersMat[:,0]))
    NPoints=len(RT_vec)
    ChromatogramMatrix=np.zeros((NPoints,NPeaks))
    for peak_id in np.arange(NPeaks):      
        RT,RT_std,Integral=ParametersMat[peak_id,:]
        ChromatogramMatrix[:,peak_id]=ChromGaussPeak(RT_vec=RT_vec,RT=RT,RT_std=RT_std,Integral=Integral,stdDistance=stdDistance)
    return ChromatogramMatrix
