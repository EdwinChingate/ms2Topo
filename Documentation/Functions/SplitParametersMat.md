## Description

The `SplitParametersMat` function divides a matrix of Gaussian parameters into smaller sub-matrices, using the valleys of a chromatogram constructed from the parameters as the splitting points, and outputs a list of the split parameters in `ChromPeaks`.

---
## Key operations

- It constructs a chromatogram using the `OverlappingGaussPeaks` function and the input parameters. It finds valleys in the constructed chromatogram using `find_peaks`, and uses those valleys to define retention time thresholds. Finally, it splits the `ParametersMat` based on the retention time thresholds and outputs the results in `ChromPeaks`.

---
## Code

```python
from scipy.signal import find_peaks
import numpy as np
from OverlappingGaussPeaks import *
def SplitParametersMat(RT_vec,ParametersMat,TresholdList,prominence=1,distance=5,stdDistance=3):
    ChromatogramMatrix=OverlappingGaussPeaks(RT_vec=RT_vec,ParametersMat=ParametersMat,stdDistance=2*stdDistance)
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

```
---

## Parameters

---

## Input

- [[distance]]
- [[prominence]]
- [[stdDistance]]
- [[TresholdList]]
- [[ParametersMat]]
- [[RT_vec]]

---

## Output

- [[ChromPeaks]]

---

## Functions

- [[OverlappingGaussPeaks]]

---

## Called by

- [[ResolveChromPeaks]]
