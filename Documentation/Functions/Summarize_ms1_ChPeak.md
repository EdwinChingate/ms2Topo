## Description

`Summarize_ms1_ChPeak` calculates and stores key information about an MS1 chromatographic peak, using `IntegrateChromatographicPeak` to calculate the peak area and identifying the retention time boundaries.

---
## Key operations

- The function utilizes `IntegrateChromatographicPeak` to calculate the area of the peak. It also identifies the minimum and maximum retention times and stores this information, along with the calculated integral, in the `SummaryChPeak` variable.

---
## Code

```python
import numpy as np
from IntegrateChromatographicPeak import *
def Summarize_ms1_ChPeak(EarlyLoc,LateLoc,Chromatogram,int_col,RT_col,minIntFrac=1,BaseLinePoints_2=3):
    ChPeak=Chromatogram[EarlyLoc:LateLoc,:].copy()   
    ChPeak=ChPeak[ChPeak[:,2].argsort()]
    Integral=IntegrateChromatographicPeak(EarlyLoc=EarlyLoc,LateLoc=LateLoc,minIntFrac=minIntFrac,Chromatogram=Chromatogram,int_col=int_col,RT_col=RT_col,BaseLinePoints_2=BaseLinePoints_2)
    ChPeak=ChPeak[(-ChPeak[:,int_col]).argsort(),:]
    min_RT=np.min(ChPeak[:,RT_col])
    max_RT=np.max(ChPeak[:,RT_col])
    mz=ChPeak[0,0]
    RT=ChPeak[0,RT_col]
    SummaryChPeak=[RT]+[min_RT]+[max_RT]+[Integral]
    return SummaryChPeak

```
---

## Parameters

---

## Input

- [[RT_col]]
- [[LateLoc]]
- [[BaseLinePoints_2]]
- [[Chromatogram]]
- [[EarlyLoc]]
- [[minIntFrac]]
- [[int_col]]

---

## Output

- [[SummaryChPeak]]

---

## Functions

- [[IntegrateChromatographicPeak]]

---

## Called by

- [[Chrom_ms1Peaks_Summaries]]
