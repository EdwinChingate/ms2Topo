## Description

The `ReResolvingChromatograms` function re-processes and refines the boundaries of chromatographic peaks, by applying the `ResolvingChromatogram` function to each peak in a list.

---
## Key operations

- The function iterates through each chromatographic peak in `ChromPeaks`, it re-processes each peak using `ResolvingChromatogram` to refine its boundaries, and then concatenates the results into `ChrPeakMat`.

---
## Code

```python
import numpy as np
from ResolvingChromatogram import *
def ReResolvingChromatograms(Chromatogram,ChromPeaks,minSpec=10,int_col=1):
    FirstChPeak=True
    for chrom_peak in ChromPeaks:
        EarlyLoc=int(chrom_peak[0])
        LateLoc=int(chrom_peak[1])
        ChrMat=ResolvingChromatogram(EarlyLoc=EarlyLoc,LateLoc=LateLoc,Chromatogram=Chromatogram,minSpec=minSpec,int_col=int_col)
        if FirstChPeak:
            ChrPeakMat=ChrMat
            FirstChPeak=False
        else:
            ChrPeakMat=np.append(ChrPeakMat,ChrMat,axis=0)    
    return ChrPeakMat    

```
---

## Parameters

---

## Input

- [[Chromatogram]]
- [[minSpec]]
- [[ChromPeaks]]
- [[int_col]]

---

## Output

- [[ChrPeakMat]]

---

## Functions

- [[ResolvingChromatogram]]

---

## Called by

