import numpy as np
from weight_gauss import *
def ParametersFitGaussPeaks(RT_vec,ChromatogramMatrix,boundsMat,ParametersMat,keepRTCentroid=True,stdDistance=3):
    NPeaks=int(len(ParametersMat[:,0]))
    Integral=boundsMat[2,1]
    ParametersMat_peak=ParametersMat.copy()
    RT=0
    for peak_id in np.arange(NPeaks):            
        Int_vec=ChromatogramMatrix[:,peak_id] 
        if keepRTCentroid:
            RT=ParametersMat[peak_id,0]
        GaussianParameters=weight_gauss(RT_vec=RT_vec,Int_vec=Int_vec,RT=RT)
        ParametersMat_peak[peak_id,:]=np.array(GaussianParameters)
    ParametersMat_peak=ParametersMat_peak[ParametersMat_peak[:,0].argsort(),:]
    GaussianIntegral=np.sum(ParametersMat_peak[:,2])
    ParametersMat_peak[:,2]=ParametersMat_peak[:,2]*Integral/GaussianIntegral
    return ParametersMat_peak
