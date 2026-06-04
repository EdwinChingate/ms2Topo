import numpy as np
from RawGaussSeed import *
from RedistributeSampling import *
from SmoothData_and_FindPeaks import *
from GaussBoundaries import *
def ToolsGaussianChrom(Chromatogram,RT_col=2,int_col=1,MaxSignals=100,distance=2):
    smooth_peaks,peaksMax=SmoothData_and_FindPeaks(Chromatogram=Chromatogram,MaxSignals=100,distance=2)
    if len(peaksMax)==0:
        return [[],[],[]]
    L=len(smooth_peaks[:,1])
    SChrom=RedistributeSampling(PeakChr=Chromatogram,N_new=L,RT_col=RT_col,int_col=int_col)
    boundsMat=GaussBoundaries(smooth_peaks=smooth_peaks)
    ParametersMat=RawGaussSeed(smooth_peaks=smooth_peaks,peaksMax=peaksMax,boundsMat=boundsMat)
    NPeaks=len(ParametersMat[:,0])
    minVec=np.array([boundsMat[:,0]]*NPeaks)
    maxVec=np.array([boundsMat[:,1]]*NPeaks)
    minList=minVec.flatten()
    maxList=maxVec.flatten()
    bounds=(minList, maxList)
    ParametersList=ParametersMat.flatten()    
    return [SChrom,ParametersList,bounds]
