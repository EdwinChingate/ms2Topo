## Description

The `mzPeak` function locates a peak in a mass spectrum, calculates its gaussian parameters using a recursive approach to refine the m/z standard deviation.

---
## Key operations

- It uses `Find_mzPeak` to locate the peak within the spectrum.
- It calculates the Gaussian parameters using `mz_Gauss_std`.
- If the calculated `mz_std` is greater than the input `mz_std`, it calls itself recursively with the new `mz_std`.

---
## Code

```python
from Find_mzPeak import *
from mz_Gauss_std import *
def mzPeak(DataSet,spectrum_idVec,mz,mz_std=2e-3,stdDistance=3,count=0,MaxCount=3,Points_for_regression=5,minSignals=7,minInt=1e3):
    PeakData_and_meta=Find_mzPeak(DataSet=DataSet,spectrum_idVec=spectrum_idVec,mz=mz,mz_std=mz_std,stdDistance=stdDistance,MaxCount=MaxCount,minInt=minInt) 
    if len(PeakData_and_meta)==0:
        return []
    PeakData=PeakData_and_meta[0]
    spectrum_id=PeakData_and_meta[1]
    GaussStats=mz_Gauss_std(PeakData,Points_for_regression=Points_for_regression)
    New_mz_std=GaussStats[1]
    if New_mz_std>mz_std and count<MaxCount:
        PeakData=mzPeak(DataSet=DataSet,spectrum_idVec=spectrum_idVec,mz=mz,mz_std=New_mz_std,count=count+1,minInt=minInt)[0]
    PeakData_and_Stats=[PeakData,GaussStats,spectrum_id]
    return PeakData_and_Stats

```
---

## Parameters

---

## Input

- [[spectrum_idVec]]
- [[mz]]
- [[Points_for_regression]]
- [[stdDistance]]
- [[MaxCount]]
- [[DataSet]]
- [[minInt]]
- [[count]]
- [[mz_std]]
- [[minSignals]]

---

## Output

- [[]]
- [[PeakData_and_Stats]]

---

## Functions

- [[mz_Gauss_std]]
- [[Find_mzPeak]]

---

## Called by

- [[ms2_features_stats]]
