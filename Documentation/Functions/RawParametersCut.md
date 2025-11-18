## Description

The `RawParametersCut` function generates initial Gaussian parameters based on smoothed data and peak maxima, refines these parameters, and then reduces the number of parameters based on their standard deviations.

---
## Key operations

- The function constructs a matrix of peak "umbrellas" around the identified peak maxima and calculates statistical properties using `UmbrellasStats`. It then refines the parameters using `RefineParameters` and determines the number of peaks to keep based on the standard deviation using `NPeaksRestrict`.

---
## Code

```python
import numpy as np
from UmbrellasStats import *
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
    PeaksUmbrellaMat=UmbrellasStats(smooth_peaks=smooth_peaks,PeaksUmbrellaMat=PeaksUmbrellaMat,NPeaks=NPeaks)
    ParametersMat=PeaksUmbrellaMat[:,3:]       
    GaussianParMat=RefineParameters(ParametersMat=ParametersMat,smooth_peaks=smooth_peaks,boundsMat=boundsMat)
    NPeaks_std_cut=NPeaksRestrict(GaussianParMat=GaussianParMat,boundsMat=boundsMat,stdDistance=4)  
    return [ParametersMat,NPeaks_std_cut]

```
---

## Parameters

---

## Input

- [[minContribution]]
- [[peaksMax]]
- [[boundsMat]]
- [[smooth_peaks]]

---

## Output

- [[ParametersMat]]
- [[NPeaks_std_cut]]

---

## Functions

- [[NPeaksRestrict]]
- [[UmbrellasStats]]
- [[RefineParameters]]

---

## Called by

