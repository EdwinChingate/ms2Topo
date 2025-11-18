## Description

The `ParametersFitGaussPeaks` function fits Gaussian curves to individual peaks in `ChromatogramMatrix` using the `WeightGauss` function, using the original retention time if `keepRTCentroid` is true, updates the `ParametersMat_peak` with the fitted parameters, normalizes the integral of the peaks based on `boundsMat`, and returns `ParametersMat_peak`.

---
## Key operations

- The function iterates through each peak in `ParametersMat`. For each peak, it extracts the corresponding intensity vector from the `ChromatogramMatrix`. If `keepRTCentroid` is true, it keeps the original retention time value from `ParametersMat`, otherwise it allows `WeightGauss` to optimize it. It fits a Gaussian curve to the peak data using the `WeightGauss` function, and updates `ParametersMat_peak` with the fitted parameters. The function normalizes the integral of the peaks based on `boundsMat`.

---
## Code

```python
import numpy as np
from WeightGauss import *
def ParametersFitGaussPeaks(RT_vec,ChromatogramMatrix,boundsMat,ParametersMat,keepRTCentroid=True,stdDistance=3):
    NPeaks=int(len(ParametersMat[:,0]))
    Integral=boundsMat[2,1]
    ParametersMat_peak=ParametersMat.copy()
    RT=0
    for peak_id in np.arange(NPeaks):            
        Int_vec=ChromatogramMatrix[:,peak_id] 
        if keepRTCentroid:
            RT=ParametersMat[peak_id,0]
        GaussianParameters=WeightGauss(RT_vec=RT_vec,Int_vec=Int_vec,RT=RT)
        ParametersMat_peak[peak_id,:]=np.array(GaussianParameters)
    ParametersMat_peak=ParametersMat_peak[ParametersMat_peak[:,0].argsort(),:]
    GaussianIntegral=np.sum(ParametersMat_peak[:,2])
    ParametersMat_peak[:,2]=ParametersMat_peak[:,2]*Integral/GaussianIntegral
    return ParametersMat_peak

```
---

## Parameters

---

## Input

- [[stdDistance]]
- [[ParametersMat]]
- [[keepRTCentroid]]
- [[RT_vec]]
- [[boundsMat]]
- [[ChromatogramMatrix]]

---

## Output

- [[ParametersMat_peak]]

---

## Functions

- [[WeightGauss]]

---

## Called by

- [[first_round_chromatogram_deconvolution]]
- [[RefineParameters]]
