from scipy.signal import find_peaks
import numpy as np
from overlapping_gauss_peaks import *
def SplitParametersMat(RT_vec,ParametersMat,TresholdList,prominence=1,distance=5,stdDistance=3):
    ChromatogramMatrix=overlapping_gauss_peaks(RT_vec=RT_vec,ParametersMat=ParametersMat,stdDistance=2*stdDistance)
    GaussFitSignal=sum(ChromatogramMatrix.T)
    peaksMin=find_peaks(-GaussFitSignal,prominence=prominence,distance=distance)[0]
    TresholdList=TresholdList+list(RT_vec[peaksMin])
    TresholdList.sort()
    NGauss=len(ParametersMat[:,0])
    min_RTLoc=TresholdList[0]
    ZerosVec=np.zeros(NGauss)
    ChromPeaks=[]
    for max_RTLoc in TresholdList[1:]:
        SplitLoc=(ParametersMat[:,0]>=min_RTLoc)&(ParametersMat[:,0]<=max_RTLoc)
        ChromPeakMat=ParametersMat[SplitLoc,:]
        ZerosVec[SplitLoc]=1
        GaussPeakFitSignal=np.matmul(ChromatogramMatrix,ZerosVec)
        MaxInt=np.max(GaussPeakFitSignal)
        RTLoc=np.where(GaussPeakFitSignal==MaxInt)[0]
        RT=RT_vec[RTLoc]
        min_RTVec=ChromPeakMat[:,0]-stdDistance*ChromPeakMat[:,1]
        min_RT=np.min(min_RTVec)
        max_RTVec=ChromPeakMat[:,0]+stdDistance*ChromPeakMat[:,1]
        max_RT=np.max(max_RTVec)
        Area=np.sum(ChromPeakMat[:,2])
        ChromPeaks.append([RT,min_RT,max_RT,Area])
        ZerosVec[SplitLoc]=0
        min_RTLoc=max_RTLoc
    return ChromPeaks
