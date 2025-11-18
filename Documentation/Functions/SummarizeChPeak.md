## Description

`SummarizeChPeak` calculates and stores key information about a chromatographic peak, including its integral and retention time boundaries, using `IntegrateChromatographicPeak` to determine the area under the curve.

---
## Key operations

- The function uses `IntegrateChromatographicPeak` to calculate the area under the peak, and identifies the minimum and maximum retention times. The function then returns the summarized data, including the calculated integral and retention time boundaries.

---
## Code

```python
from IntegrateChromatographicPeak import *
def SummarizeChPeak(EarlyLoc,LateLoc,Chromatogram,BaseLinePoints_2=3):
    ChPeak=Chromatogram[EarlyLoc:LateLoc,:].copy()   
    Integral=IntegrateChromatographicPeak(EarlyLoc,LateLoc,Chromatogram,BaseLinePoints_2=BaseLinePoints_2)
    ChPeak=ChPeak[(-ChPeak[:,5]).argsort(),:]
    min_RT=np.min(ChPeak[:,2])
    max_RT=np.max(ChPeak[:,2])
    ChPeak[0,5]=Integral
    ChPeak[0,12]=min_RT
    ChPeak[0,13]=max_RT
    SummaryChPeak=ChPeak[0,:]
    return SummaryChPeak

```
---

## Parameters

---

## Input

- [[LateLoc]]
- [[BaseLinePoints_2]]
- [[Chromatogram]]
- [[EarlyLoc]]

---

## Output

- [[SummaryChPeak]]

---

## Functions

- [[IntegrateChromatographicPeak]]

---

## Called by

- [[ModuleChromSummaries]]
