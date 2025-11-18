## Description

The `mz_Edges` function is used to determine the edges of the m/z regions in a mass spectrum by calculating the differences between consecutive m/z values and grouping the adjacent ones into regions.

---
## Key operations

- It samples the `AllRawPeaks` array using `FractionSample` to avoid using the whole data set when calculating the edges.
- It sorts the m/z values in ascending order.
- It calculates the differences between consecutive m/z values.
- It identifies locations where the differences between consecutive m/z values are greater than `mz_tol`, and the result is used to define the start and end indexes of the m/zedges.

---
## Code

```python
import numpy as np
def mz_Edges(AllRawPeaks,FractionSample=30,mz_tol=2e-3):
    NPeaks=len(AllRawPeaks[:,0])    
    NSample=int(NPeaks*FractionSample/100)
    SampleVec=np.linspace(0,NPeaks-1,NSample,dtype='int')
    SomePeaks=AllRawPeaks[SampleVec,:]
    low_mzVec=SomePeaks[:-1,0]
    high_mzVec=SomePeaks[1:,0]
    mz_difVec=high_mzVec-low_mzVec
    difLoc=np.where(mz_difVec>mz_tol)[0]+1
    N_difLoc=len(difLoc)
    mz_divMat=np.zeros((N_difLoc+1,2))
    mz_divMat[0,0]=0
    mz_divMat[1:,0]=difLoc
    mz_divMat[:-1,1]=difLoc
    mz_divMat[-1,1]=len(SomePeaks[:,0])
    edgesVecList=list(mz_divMat)
    return [edgesVecList,SomePeaks]

```
---

## Parameters

---

## Input

- [[AllRawPeaks]]
- [[mz_tol]]
- [[FractionSample]]

---

## Output

- [[SomePeaks]]
- [[edgesVecList]]

---

## Functions


---

## Called by

