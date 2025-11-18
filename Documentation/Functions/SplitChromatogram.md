## Description

The `SplitChromatogram` function divides a chromatogram into sub-chromatograms by filtering by minimum intensity, using the `RT_edges` function to define the edges, and returns a list containing the sub-chromatograms.

---
## Key operations

- It filters the input chromatogram `Chromatogram0` based on a minimum intensity, then it uses `RT_edges` to identify the edges of the peaks, and splits the chromatogram into smaller sections based on those edges. It outputs a list of sub-chromatograms, `ChromatogramList`.

---
## Code

```python
import numpy as np
from RT_edges import *
def SplitChromatogram(Chromatogram0,RT_tol=5,minSignals=5,minInt=1):
    edgesVecList=RT_edges(Chromatogram=Chromatogram0,RT_tol=RT_tol)
    ChromatogramList=[]
    for edges in edgesVecList:
        early_RT=int(edges[0])
        late_RT=int(edges[1])
        if (late_RT-early_RT)>minSignals:
            Chromatogram=Chromatogram0[early_RT:late_RT,:].copy()
            LChrom=len(Chromatogram[:,0])
            MaxInt=np.max(Chromatogram[:,1])
            MaxIntF=MaxInt*minInt/100
            MinIntFil=Chromatogram[:,1]>MaxIntF
            Chromatogram=Chromatogram[MinIntFil,:]
            if len(Chromatogram[:,0])<LChrom:
                Chromatograms=SplitChromatogram(Chromatogram0=Chromatogram,RT_tol=5,minSignals=5,minInt=1)
            else:
                Chromatograms=[Chromatogram]
            ChromatogramList=Chromatograms+ChromatogramList
    return ChromatogramList

```
---

## Parameters

---

## Input

- [[Chromatogram0]]
- [[minInt]]
- [[RT_tol]]
- [[minSignals]]

---

## Output

- [[ChromatogramList]]

---

## Functions

- [[RT_edges]]

---

## Called by

- [[AllSubChromatograms]]
