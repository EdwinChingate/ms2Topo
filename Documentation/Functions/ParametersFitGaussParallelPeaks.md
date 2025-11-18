## Description

The `ParametersFitGaussParallelPeaks` function fits Gaussian curves to individual peaks in `ChromatogramMatrix` using the `WeightGauss` function, updates the `ParametersMat` with the fitted parameters, normalizes the integral of the peaks using `boundsMat`, and stores the results in `GaussianPopulation`.

---
## Key operations

- The function iterates through each peak in `ParametersMat`. For each peak, it extracts the corresponding intensity vector from the `ChromatogramMatrix` and the retention time from `ParametersMat`, and fits a Gaussian curve using the `WeightGauss` function. It updates the parameter matrix with the new parameters, and appends this updated parameter matrix to the `GaussianPopulation`. The function normalizes the integral of the peaks based on `boundsMat`.

---
## Code

```python
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

```
---

## Parameters

---

## Input

- [[stdDistance]]
- [[ParametersMat]]
- [[RT_vec]]
- [[boundsMat]]
- [[ChromatogramMatrix]]

---

## Output

- [[GaussianPopulation]]

---

## Functions

- [[WeightGauss]]

---

## Called by

- [[RefineChromPeak]]
