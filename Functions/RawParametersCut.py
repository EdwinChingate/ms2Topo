import numpy as np
from umbrellas_stats import *
from RefineParameters import *
from NPeaksRestrict import *
def RawParametersCut(smooth_peaks,peaksMax,boundsMat,minContribution=2):
    NPeaks=len(peaksMax)
    NSignals=int(len(smooth_peaks[:,0]))
    PeaksUmbrellaMat=np.zeros((NPeaks,6))
    ExtraPeaksMat=np.zeros((1,3))
    PeaksUmbrellaMat[:,0]=peaksMax
    PeakValley=np.array((peaksMax[1:]+peaksMax[:-1])/2,dtype='int')
    PeaksUmbrellaMat[1:,1]=PeakValley
    PeaksUmbrellaMat[:-1,2]=PeakValley
    PeaksUmbrellaMat[-1,2]=NSignals
    PeaksUmbrellaMat=umbrellas_stats(smooth_peaks=smooth_peaks,PeaksUmbrellaMat=PeaksUmbrellaMat,NPeaks=NPeaks)
    ParametersMat=PeaksUmbrellaMat[:,3:]       
    GaussianParMat=RefineParameters(ParametersMat=ParametersMat,smooth_peaks=smooth_peaks,boundsMat=boundsMat)
    NPeaks_std_cut=NPeaksRestrict(GaussianParMat=GaussianParMat,boundsMat=boundsMat,stdDistance=4)  
    return [ParametersMat,NPeaks_std_cut]
