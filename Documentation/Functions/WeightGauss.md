## Description

`WeightGauss` calculates Gaussian parameters using weighted least squares, based on provided intensity and retention time data, used to describe the shape and size of peaks.

---
## Key operations

- The function calculates the relative intensities, and if no RT is provided, it calculates a weighted average for RT. It then calculates the variance, standard deviation, and total intensity, then stores these values in the output list, `GaussianParameters`.

---
## Code

```python
import numpy as np
def WeightGauss(RT_vec,Int_vec,RT=0):  
    minInt=np.min(Int_vec)
    if minInt<0:
        Int_vec=Int_vec.copy()-minInt
    maxInt=np.max(Int_vec)
    NSignals=len(Int_vec)
    sum_Int=np.sum(Int_vec)
    Relative_Int=Int_vec/sum_Int
    if RT==0:
        RT=sum((RT_vec*Relative_Int))
    RT_Dif=RT_vec-RT
    Varian=np.sum(Relative_Int*RT_Dif**2)*NSignals/(NSignals-1)
    RT_std=np.sqrt(Varian)
    sqrt2pi=2.5066282746310002 #np.sqrt(np.pi*2)     
    I_total=maxInt*RT_std*sqrt2pi
    GaussianParameters=[RT,RT_std,I_total]
    return GaussianParameters

```
---

## Parameters

---

## Input

- [[Int_vec]]
- [[RT]]
- [[RT_vec]]

---

## Output

- [[GaussianParameters]]

---

## Functions


---

## Called by

- [[UmbrellasStats]]
- [[ParametersFitGaussPeaks]]
- [[ParametersFitGaussParallelPeaks]]
