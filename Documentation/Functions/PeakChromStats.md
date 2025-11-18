## Description

The `PeakChromStats` function calculates statistical features of a given chromatographic peak.

---
## Key operations

- The function calculates the mean, standard deviation, minimum, and maximum retention times from the data within the provided boundaries of the chromatographic peak in the `Chromatogram`.

---
## Code

```python
import numpy as np
def PeakChromStats(edgesVec,Chromatogram):
    early_RT=int(edgesVec[0])
    late_RT=int(edgesVec[1])
    Chromatogram=Chromatogram[early_RT:late_RT,:]
    SumIntens=sum(Chromatogram[:,1])
    RelativeInt=Chromatogram[:,1]/SumIntens
    RT_mean=sum(RelativeInt*Chromatogram[:,2])
    l=len(Chromatogram[:,1])   
    if l==1:
        RT_std=0
        RT_min=RT_mean
        RT_max=RT_mean
    else:
        RT_varian=sum(RelativeInt*(Chromatogram[:,2]-RT_mean)**2)*l/(l-1)  
        RT_std=np.sqrt(RT_varian)
        RT_min=np.min(Chromatogram[:,2])
        RT_max=np.max(Chromatogram[:,2])
    peak_feat_stats=[RT_mean,RT_std,RT_min,RT_max,early_RT,late_RT]
    return peak_feat_stats

```
---

## Parameters

---

## Input

- [[Chromatogram]]
- [[edgesVec]]

---

## Output

- [[peak_feat_stats]]

---

## Functions


---

## Called by

