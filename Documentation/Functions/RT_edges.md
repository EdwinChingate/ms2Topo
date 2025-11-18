## Description

The `RT_edges` function identifies the start and end indices of chromatographic peaks by detecting significant changes in the retention time.

---
## Key operations

- The function calculates the differences in retention times between consecutive data points, then it identifies the locations where the difference is greater than `RT_tol`. These locations are used to define the start and end of peaks.

---
## Code

```python
import numpy as np
def RT_edges(Chromatogram,RT_tol=10):
    NSignals=len(Chromatogram[:,0])
    low_RTVec=Chromatogram[:-1,2]
    high_RTVec=Chromatogram[1:,2]
    RT_difVec=high_RTVec-low_RTVec
    difLoc=np.where(RT_difVec>RT_tol)[0]+1
    N_difLoc=len(difLoc)
    RT_divMat=np.zeros((N_difLoc+1,2))
    RT_divMat[0,0]=0
    RT_divMat[1:,0]=difLoc
    RT_divMat[:-1,1]=difLoc
    RT_divMat[-1,1]=len(Chromatogram[:,0])
    edgesVecList=list(RT_divMat)
    return edgesVecList

```
---

## Parameters

---

## Input

- [[Chromatogram]]
- [[RT_tol]]

---

## Output

- [[edgesVecList]]

---

## Functions


---

## Called by

- [[SplitChromatogram]]
