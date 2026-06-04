import numpy as np
from umbrellas_stats import *
from RefineParameters import *
def RawGaussCouple(smooth_peaks,peaksMax,boundsMat,minContribution=2):
    NPeaks=len(peaksMax)
    NSignals=int(len(smooth_peaks[:,0]))
    PeaksUmbrellaMat=np.zeros((NPeaks,6))
    ExtraPeaksMat=np.zeros((2,3))
    PeaksUmbrellaMat[:,0]=peaksMax
    PeakValley=np.array((peaksMax[1:]+peaksMax[:-1])/2,dtype='int')
    PeaksUmbrellaMat[1:,1]=PeakValley
    PeaksUmbrellaMat[:-1,2]=PeakValley
    PeaksUmbrellaMat[-1,2]=NSignals
    PeaksUmbrellaMat=umbrellas_stats(smooth_peaks=smooth_peaks,PeaksUmbrellaMat=PeaksUmbrellaMat,NPeaks=NPeaks)
    ParametersMat=PeaksUmbrellaMat[:,3:]    
    GaussianParMatCons,ContributionFilter=RefineParameters(ParametersMat=ParametersMat,smooth_peaks=smooth_peaks,boundsMat=boundsMat,minContribution=minContribution,ReturnFilter=True)
    ParametersMat=ParametersMat[ContributionFilter,:]
    ExtraPeaksMat[0,:]=ParametersMat[-1,:].copy()
    ExtraPeaksMat[-1,:]=ParametersMat[0,:]
    ExtraPeaksMat[:,2]=ParametersMat[0,2]/100    
    ParametersMat=np.append(ParametersMat,ExtraPeaksMat,axis=0)
    ParametersMat=ParametersMat[ParametersMat[:,0].argsort(),:]
    GaussianParMatCons=np.append(GaussianParMatCons,ExtraPeaksMat,axis=0)
    GaussianParMatCons=GaussianParMatCons[GaussianParMatCons[:,0].argsort(),:]    
    return [ParametersMat,GaussianParMatCons]
