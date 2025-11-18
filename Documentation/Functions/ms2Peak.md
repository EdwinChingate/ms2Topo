## Description

`ms2Peak` locates, characterizes, and refines the m/z of a peak within an MS2 spectrum using `Find_ms2Peak` to locate the peak and `mz_Gauss_std` to refine the standard deviation, using recursion to refine the peak fit.

---
## Key operations

- The function uses `Find_ms2Peak` to locate a peak and `mz_Gauss_std` to calculate the standard deviation of the m/z values of the peak. If the new standard deviation is larger than the initial, it recursively calls itself, otherwise it returns the peak data and statistics.

---
## Code

```python
from Find_ms2Peak import *
from mz_Gauss_std import *
def ms2Peak(RawSpectrum,mz,mz_std=2e-3,stdDistance=3,minSignals=4,count=0,MaxCount=3,minInt=1e3,Points_for_regression=4):
    PeakData=Find_ms2Peak(RawSpectrum=RawSpectrum,mz=mz,mz_std=mz_std,stdDistance=stdDistance,minSignals=minSignals,MaxCount=MaxCount,minInt=minInt)
    if len(PeakData)==0:
        return []
    GaussStats=mz_Gauss_std(PeakData,Points_for_regression=Points_for_regression)
    New_mz_std=GaussStats[1]
    if New_mz_std>mz_std and count<MaxCount:
        PeakData=ms2Peak(RawSpectrum=RawSpectrum,mz=mz,mz_std=New_mz_std,stdDistance=stdDistance,minSignals=minSignals,count=count+1,MaxCount=MaxCount,minInt=minInt,Points_for_regression=Points_for_regression)[0]
    PeakData_and_Stats=[PeakData,GaussStats]
    return PeakData_and_Stats

```
---

## Parameters

---

## Input

- [[mz]]
- [[Points_for_regression]]
- [[stdDistance]]
- [[MaxCount]]
- [[minInt]]
- [[count]]
- [[RawSpectrum]]
- [[mz_std]]
- [[minSignals]]

---

## Output

- [[]]
- [[PeakData_and_Stats]]

---

## Functions

- [[mz_Gauss_std]]
- [[Find_ms2Peak]]

---

## Called by

- [[ms2_peak_stats]]
