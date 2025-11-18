## Description

The `AllSubChromatograms` function extracts a chromatogram based on an m/z and m/z standard deviation, and then splits it into sub-chromatograms based on retention time differences.

---
## Key operations

- It uses `MaxIntChromatogram` to extract the chromatogram from `AllRawPeaks`. It then uses `SplitChromatogram` to divide the chromatogram into sub-chromatograms based on the `RT_tol` and `minSignals`.

---
## Code

```python
from MaxIntChromatogram import *
from SplitChromatogram import *
def AllSubChromatograms(mz,mz_std,AllRawPeaks,stdDistance=3,RT_tol=5,minSignals=5):
    ChromatogramList=[]
    Chromatogram0=MaxIntChromatogram(mz=mz,mz_std=mz_std,AllRawPeaks=AllRawPeaks,stdDistance=stdDistance)
    ChromatogramList=SplitChromatogram(Chromatogram0=Chromatogram0,RT_tol=5,minSignals=5,minInt=1)
    return ChromatogramList

```
---

## Parameters

---

## Input

- [[mz]]
- [[stdDistance]]
- [[AllRawPeaks]]
- [[RT_tol]]
- [[mz_std]]
- [[minSignals]]

---

## Output

- [[ChromatogramList]]

---

## Functions

- [[MaxIntChromatogram]]
- [[SplitChromatogram]]

---

## Called by

- [[ResolveFullChromatogram]]
