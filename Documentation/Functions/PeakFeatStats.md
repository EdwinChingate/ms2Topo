## Description

The `PeakFeatStats` function calculates the mean and standard deviation of the m/z values for a given set of peaks.

---
## Key operations

- The function calculates the mean and standard deviation of m/z values from the input `Peaks` array, within the provided boundaries defined by `edgesVec`.

---
## Code

```python
import numpy as np
def PeakFeatStats(edgesVec,Peaks):
    low_mz=int(edgesVec[0])
    high_mz=int(edgesVec[1])
    Peak=Peaks[low_mz:high_mz,:]
    SumIntens=sum(Peak[:,1])
    RelativeInt=Peak[:,1]/SumIntens
    mz_mean=sum(RelativeInt*Peak[:,0])
    l=len(Peak[:,1])   
    if l==1:
        mz_std=0
    else:
        mz_varian=sum(RelativeInt*(Peak[:,0]-mz_mean)**2)*l/(l-1)  
        mz_std=np.sqrt(mz_varian)
    peak_feat_stats=[mz_mean,mz_std]
    return peak_feat_stats

```
---

## Parameters

---

## Input

- [[Peaks]]
- [[edgesVec]]

---

## Output

- [[peak_feat_stats]]

---

## Functions


---

## Called by

- [[mz_mz_std_ms1]]
