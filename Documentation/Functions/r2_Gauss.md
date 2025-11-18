## Description

The `r2_Gauss` function assesses the goodness of fit of a Gaussian curve to a peak by calculating the r² value.

---
## Key operations

- It generates the Gaussian curve using the provided `GaussianParameters` and the `GaussianPeak` function.
- It calculates the total sum of squares (SS_tot), which is the sum of the squared differences between the observed intensities and the mean of the observed intensities.
- It calculates the residual sum of squares (SS_res), which is the sum of the squared differences between the observed intensities and the Gaussian curve intensities.
- It calculates the r² as 1 - (SS_res / SS_tot).

---
## Code

```python
import numpy as np
from GaussianPeak import *
def r2_Gauss(PeakData,GaussianParameters):
    mz=GaussianParameters[0]
    mz_std=GaussianParameters[1]
    I_total=GaussianParameters[2]    
    Gaussian_Int=GaussianPeak(PeakData[:,0],mz,mz_std,I_total)
    I_mean=np.mean(PeakData[:,1])
    SS_tot=np.sum((PeakData[:,1]-I_mean)**2)
    SS_res=np.sum((Gaussian_Int-PeakData[:,1])**2)
    r2=1-SS_res/SS_tot
    return [r2]

```
---

## Parameters

---

## Input

- [[PeakData]]
- [[GaussianParameters]]

---

## Output

- [[r2]]

---

## Functions

- [[GaussianPeak]]

---

## Called by

- [[Normal_Fit]]
