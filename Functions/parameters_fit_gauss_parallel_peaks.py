import numpy as np
from WeightGauss import *
def ParametersFitGaussParallelPeaks(RT_vec,ChromatogramMatrix,boundsMat,ParametersMat,stdDistance=3):
    NPeaks=int(len(ParametersMat[:,0]))
    Integral=boundsMat[2,1]
    GaussianPopulation=[]
    for peak_id in np.arange(NPeaks):    
        ParametersMat_peak=ParametersMat.copy()
        Int_vec=ChromatogramMatrix[:,peak_id] 
        RT=ParametersMat[peak_id,0]        
        GaussianParameters=WeightGauss(RT_vec=RT_vec,Int_vec=Int_vec,RT=RT)        
        ParametersMat_peak[peak_id,:]=np.array(GaussianParameters)
        ParametersMat_peak=ParametersMat_peak[ParametersMat_peak[:,0].argsort(),:]
        GaussianIntegral=np.sum(ParametersMat_peak[:,2])
        ParametersMat_peak[:,2]=ParametersMat_peak[:,2]*Integral/GaussianIntegral
        GaussianPopulation.append(ParametersMat_peak)
    return GaussianPopulation
