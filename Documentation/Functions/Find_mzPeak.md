## Description

The `Find_mzPeak` function locates a peak within a specified m/z range in a given spectrum, and returns the peak data and the spectrum id, using a recursive search that increases the m/z window, or searches in the next spectrum, if no peak is initially found.

---
## Key operations

- It filters a spectrum from the `DataSet` to find peaks within a specified m/z range, and if no peak is found, it recursively calls itself, increasing the `stdDistance`, or it looks for a peak in the next spectrum in the `spectrum_idVec` list.

---
## Code

```python
import numpy as np
def Find_mzPeak(DataSet,spectrum_idVec,mz,spectrum_id_Loc=0,mz_std=2e-3,stdDistance=3,minSignals=7,count=0,MaxCount=3,minInt=1e3):
    if spectrum_id_Loc==len(spectrum_idVec):
        return []    
    spectrum_id=spectrum_idVec[spectrum_id_Loc]    
    SpectralSignals=DataSet[int(spectrum_id)]
    spectrum=np.array(SpectralSignals.get_peaks()).T
    min_mz_peak=mz-mz_std*stdDistance
    max_mz_peak=mz+mz_std*stdDistance
    peakFilter=(spectrum[:,0]>min_mz_peak)&(spectrum[:,0]<max_mz_peak)&(spectrum[:,1]>minInt)
    PeakData=spectrum[peakFilter,:]
    if (len(PeakData)==0) or ((len(PeakData[:,0])<minSignals) and (count==MaxCount)):
        PeakData_and_meta=Find_mzPeak(DataSet=DataSet,spectrum_idVec=spectrum_idVec,spectrum_id_Loc=spectrum_id_Loc+1,mz=mz,mz_std=mz_std,stdDistance=stdDistance,minInt=minInt,minSignals=minSignals)
    elif (len(PeakData[:,0])<minSignals) and (count<MaxCount):
        PeakData_and_meta=Find_mzPeak(DataSet=DataSet,spectrum_idVec=spectrum_idVec,spectrum_id_Loc=spectrum_id_Loc,mz=mz,mz_std=mz_std,stdDistance=stdDistance+1,count=count+1,minInt=minInt,minSignals=minSignals)
    else:
        PeakData_and_meta=[PeakData,spectrum_id]
    return PeakData_and_meta

```
---

## Parameters

---

## Input

- [[spectrum_idVec]]
- [[mz]]
- [[stdDistance]]
- [[MaxCount]]
- [[DataSet]]
- [[minInt]]
- [[count]]
- [[mz_std]]
- [[spectrum_id_Loc]]
- [[minSignals]]

---

## Output

- [[]]
- [[PeakData_and_meta]]

---

## Functions


---

## Called by

- [[mzPeak]]
