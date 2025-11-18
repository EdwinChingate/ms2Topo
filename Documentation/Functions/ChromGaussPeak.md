## Description

The `ChromGaussPeak` function generates a Gaussian curve given a retention time, standard deviation, and integral, returning the Gaussian intensities along a given RT vector.

---
## Key operations

- The function calculates a Gaussian intensity vector by using the provided parameters.

---
## Code

```python
import numpy as np
def ChromGaussPeak(RT_vec,RT,RT_std,Integral,stdDistance=3):
    NSignals=len(RT_vec)
    Gaussian_Int=np.zeros(NSignals)
    min_RT=RT-stdDistance*RT_std
    max_RT=RT+stdDistance*RT_std
    RTLoc=(RT_vec>min_RT)&(RT_vec<max_RT)
    LogVec=-((RT_vec[RTLoc]-RT)/RT_std)**2/2
    f1_sqrt2pi=0.3989422804014327 #1/np.sqrt(np.pi*2) 
    Gaussian_Int[RTLoc]=np.exp(LogVec)*f1_sqrt2pi*Integral/RT_std
    return Gaussian_Int    

```
---

## Parameters

---

## Input

- [[RT]]
- [[RT_std]]
- [[stdDistance]]
- [[RT_vec]]
- [[Integral]]

---

## Output

- [[Gaussian_Int]]

---

## Functions


---

## Called by

- [[OverlappingGaussPeaks]]
