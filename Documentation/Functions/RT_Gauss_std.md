## Description

The `RT_Gauss_std` function calculates parameters of a Gaussian curve fitted to a chromatographic peak.

---
## Key operations

- This function calculates the parameters of a Gaussian curve fitted to a chromatographic peak. It selects data points around the maximum intensity, performs a linear regression to estimate the standard deviation, and then computes other parameters such as the total intensity, and the r-squared value, returning them in `GaussStats`.

---
## Code

```python
from scipy import stats
import numpy as np
def RT_Gauss_std(PeakData,MaxRTLoc,EarlyLoc,LateLoc,RT_col=0,int_col=1,Points_for_regression=4):
    RT_maxInt=PeakData[MaxRTLoc,RT_col]
    maxInt=PeakData[MaxRTLoc,int_col]
    PeakData=PeakData[EarlyLoc:LateLoc,:].copy()
    PeakData=PeakData[PeakData[:,int_col]>0,:]
    RT_DifVec=np.abs(PeakData[:,RT_col]-RT_maxInt)
    PeakData=PeakData[RT_DifVec.argsort(),:]
    Closest_PeakData=PeakData[:Points_for_regression,:]
    log_Int_Vec=np.log(Closest_PeakData[:,int_col]/maxInt)
    Variance_RT_vec=(Closest_PeakData[:,RT_col]-RT_maxInt)**2
    X=log_Int_Vec
    Y=Variance_RT_vec
    reg=stats.linregress(X,Y)
    m=reg[0]
    b=reg[1]
    r2=reg[2]**2
    if m>0:
        return [0,0,0,0,0,0]          
    RT_std=np.sqrt(-m/2)
    sqrt2pi=2.5066282746310002 #np.sqrt(np.pi*2) 
    I_total=maxInt*RT_std*sqrt2pi
    GaussStats=[maxInt,RT_maxInt,RT_std,I_total,b,r2]      
    return GaussStats    

```
---

## Parameters

---

## Input

- [[PeakData]]
- [[Points_for_regression]]
- [[RT_col]]
- [[LateLoc]]
- [[EarlyLoc]]
- [[MaxRTLoc]]
- [[int_col]]

---

## Output

- [[GaussStats]]
- [[0]]

---

## Functions


---

## Called by

