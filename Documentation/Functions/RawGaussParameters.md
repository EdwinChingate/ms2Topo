## Description

The `RawGaussParameters` function generates initial parameters for Gaussian peak fitting using smoothed data and identified peak maxima, and adds two extra peaks.

---
## Key operations

- The function constructs a matrix of peak "umbrellas" around the identified peak maxima, calculates statistical properties within these umbrellas using `UmbrellasStats`, and refines the parameters using `RefineParameters`. It also appends two extra peaks to the `ParametersMat` and sorts the parameters based on their retention time.

---
## Code

```python
import numpy as np
from UmbrellasStats import *
from RefineParameters import *
def RawGaussParameters(smooth_peaks,peaksMax,boundsMat,minContribution=2):
    NPeaks=len(peaksMax)
    NSignals=int(len(smooth_peaks[:,0]))
    PeaksUmbrellaMat=np.zeros((NPeaks,7))
    ExtraPeaksMat=np.zeros((2,3))
    PeaksUmbrellaMat[:,0]=peaksMax
    PeakValley=np.array((peaksMax[1:]+peaksMax[:-1])/2,dtype='int')
    PeaksUmbrellaMat[1:,1]=PeakValley
    PeaksUmbrellaMat[:-1,2]=PeakValley
    PeaksUmbrellaMat[-1,2]=NSignals
    PeaksUmbrellaMat=UmbrellasStats(smooth_peaks=smooth_peaks,PeaksUmbrellaMat=PeaksUmbrellaMat,NPeaks=NPeaks)
    PeaksUmbrellaMat=PeaksUmbrellaMat[PeaksUmbrellaMat[:,6].argsort(),:]
    ParametersMat=PeaksUmbrellaMat[:,4:]
    ParametersMat=RefineParameters(ParametersList=ParametersMat,smooth_peaks=smooth_peaks,boundsMat=boundsMat,minContribution=minContribution)
    ExtraPeaksMat[0,:]=ParametersMat[-1,:].copy()
    ExtraPeaksMat[-1,:]=ParametersMat[0,:]
    ExtraPeaksMat[:,2]=ParametersMat[0,2]/100    
    ParametersMat=np.append(ParametersMat,ExtraPeaksMat,axis=0)
    ParametersMat=ParametersMat[ParametersMat[:,0].argsort(),:]
    return ParametersMat

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

---

## Functions

- [[UmbrellasStats]]
- [[RefineParameters]]

---

## Called by

- [[first_round_chromatogram_deconvolution]]
