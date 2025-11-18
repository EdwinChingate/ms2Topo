## Description

The `OverlappingGaussPeaks` function creates a matrix of overlapping Gaussian peaks, `ChromatogramMatrix`, by calling the `ChromGaussPeak` function for each peak in `ParametersMat`, using the `RT_vec` and `stdDistance`.

---
## Key operations

- The function iterates through each row of the `ParametersMat` which represents the parameters for one peak, calling the `ChromGaussPeak` function with the retention time vector `RT_vec`, and the parameters for each peak, generating a chromatographic profile for each peak. The function accumulates the individual peaks profiles in the `ChromatogramMatrix`.

---
## Code

```python
import numpy as np
from ChromGaussPeak import *
def OverlappingGaussPeaks(RT_vec,ParametersMat,stdDistance=3):
    NPeaks=int(len(ParametersMat[:,0]))
    NPoints=len(RT_vec)
    ChromatogramMatrix=np.zeros((NPoints,NPeaks))
    for peak_id in np.arange(NPeaks):      
        RT,RT_std,Integral=ParametersMat[peak_id,:]
        ChromatogramMatrix[:,peak_id]=ChromGaussPeak(RT_vec=RT_vec,RT=RT,RT_std=RT_std,Integral=Integral,stdDistance=stdDistance)
    return ChromatogramMatrix

```
---

## Parameters

---

## Input

- [[stdDistance]]
- [[ParametersMat]]
- [[RT_vec]]

---

## Output

- [[ChromatogramMatrix]]

---

## Functions

- [[ChromGaussPeak]]

---

## Called by

- [[first_round_chromatogram_deconvolution]]
- [[GaussianChromatogram]]
- [[SplitParametersMat]]
- [[RefineChromPeak]]
- [[EvaluatePopulation]]
- [[RefineParameters]]
