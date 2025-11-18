## Description

The `ms2_features_stats` function calculates the statistical properties of an MS2 feature, including its relation to the closest MS1 spectrum, using Gaussian fitting of the peak.

---
## Key operations

- It finds the closest MS1 spectrum using `closest_ms1_spec`.
- It extracts peak data and calculates Gaussian fit parameters using `mzPeak`.
- It fits a Gaussian curve to the peak using `Normal_Fit`.
- It calculates confidence intervals and other statistics based on the Gaussian fit.

---
## Code

```python
from scipy import stats
from mzPeak import *
from closest_ms1_spec import *
from Normal_Fit import *
def ms2_features_stats(DataSet,MS2_id,SummMS2,MS1IDVec,mz_std=2e-3,MS2_to_MS1_ratio=10,stdDistance=3,MaxCount=3,Points_for_regression=5,minSignals=7,alpha=0.01):
    RT=SummMS2[MS2_id,1]
    mz=SummMS2[MS2_id,0]    
    MS2_Fullsignal_id=SummMS2[MS2_id,2]
    spectrum_idVec=closest_ms1_spec(mz=mz,RT=RT,MS2_Fullsignal_id=MS2_Fullsignal_id,SummMS2=SummMS2,MS1IDVec=MS1IDVec,MS2_to_MS1_ratio=MS2_to_MS1_ratio)
    PeakData_and_Stats=mzPeak(DataSet=DataSet,spectrum_idVec=spectrum_idVec,mz=mz,mz_std=mz_std,stdDistance=stdDistance,MaxCount=MaxCount,Points_for_regression=Points_for_regression,minSignals=minSignals)    
    if len(PeakData_and_Stats)==0:
        return []
    spectrum_id=[int(PeakData_and_Stats[2])]
    NormalParameters=Normal_Fit(PeakData_and_Stats=PeakData_and_Stats)
    Nsignals=len(PeakData_and_Stats[0][:,0])
    mz=NormalParameters[0]
    mz_std=NormalParameters[1]
    min_mz=[mz-stdDistance*mz_std]
    max_mz=[mz+stdDistance*mz_std]
    tref=stats.t.interval(1-alpha, Nsignals-1)[1]    
    ConfidenceIntervalDa=[tref*mz_std/np.sqrt(Nsignals)]
    ConfidenceInterval=[tref*mz_std/np.sqrt(Nsignals)/mz*1e6]
    features_stats=[int(MS2_Fullsignal_id)]+spectrum_id+[RT]+NormalParameters+[Nsignals]+ConfidenceIntervalDa+ConfidenceInterval+min_mz+max_mz    
    return features_stats

```
---

## Parameters

---

## Input

- [[SummMS2]]
- [[Points_for_regression]]
- [[stdDistance]]
- [[MaxCount]]
- [[MS1IDVec]]
- [[MS2_to_MS1_ratio]]
- [[DataSet]]
- [[MS2_id]]
- [[alpha]]
- [[mz_std]]
- [[minSignals]]

---

## Output

- [[]]
- [[features_stats]]

---

## Functions

- [[Normal_Fit]]
- [[closest_ms1_spec]]
- [[mzPeak]]

---

## Called by

- [[feat_ms2_Gauss]]
