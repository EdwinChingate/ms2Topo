## Description

The `mz_Gauss_std` function calculates the standard deviation of the m/z values of a peak by fitting a Gaussian model to the peak data and using linear regression.

---
## Key operations

- It identifies the maximum intensity and its corresponding m/z value in `PeakData`.
- It selects the `Points_for_regression` closest data points to the maximum intensity peak.
- It calculates the variance of m/z values relative to the m/z at maximum intensity.
- It performs a linear regression on the logarithm of the intensities versus the variance of the m/z values.
- It calculates the m/z standard deviation (`mz_std`) from the slope of the regression and returns the `GaussStats`.

---
## Code

```python
from scipy import stats
import numpy as np
def mz_Gauss_std(PeakData,Points_for_regression=4):
    PeakData=PeakData[PeakData[:,1]>0,:].copy()
    maxInt=np.max(PeakData[:,1])
    maxInt_Loc=np.where(PeakData[:,1]==maxInt)[0][0]
    mz_maxInt=PeakData[maxInt_Loc,0]
    mz_DifVec=np.abs(PeakData[:,0]-mz_maxInt)
    PeakData=PeakData[mz_DifVec.argsort(),:]
    Closest_PeakData=PeakData[:Points_for_regression,:]
    log_Int_Vec=np.log(Closest_PeakData[:,1]/maxInt)
    Variance_mz_vec=(Closest_PeakData[:,0]-mz_maxInt)**2
    X=log_Int_Vec
    Y=Variance_mz_vec
    reg=stats.linregress(X,Y)
    m=reg[0]
    b=reg[1]
    r2=reg[2]**2
    mz_std=np.sqrt(-m/2)
    sqrt2pi=2.5066282746310002 #np.sqrt(np.pi*2) 
    I_total=maxInt*mz_std*sqrt2pi
    GaussStats=[mz_maxInt,mz_std,b,r2,I_total]      
    return GaussStats    

```
---

## Parameters

---

## Input

- [[PeakData]]
- [[Points_for_regression]]

---

## Output

- [[GaussStats]]

---

## Functions


---

## Called by

- [[ms2Peak]]
- [[mzPeak]]
