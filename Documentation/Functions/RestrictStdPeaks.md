## Description

The `RestrictStdPeaks` function filters a set of Gaussian peaks, keeping only those within a defined range based on their cumulative standard deviation and the total retention time range specified by `boundsMat`. It uses `stdDistance` to scale the standard deviation, which determines the interval for filtering.

---
## Key operations

- The function sorts the input `ParametersMat` and `GaussianParMatCons` by the standard deviation of the peaks.
- It calculates the cumulative sum of the standard deviations of the peaks and multiplies them by `stdDistance`.
- It filters out peaks based on their cumulative standard deviation and the total RT range, which is based on the `boundsMat`.

---
## Code

```python
import numpy as np
def RestrictStdPeaks(RawGaussPop,boundsMat,stdDistance=4):
    ParametersMat=RawGaussPop[0]
    GaussianParMatCons=RawGaussPop[1]
    ParametersMat=ParametersMat[GaussianParMatCons[:,1].argsort(),:]
    GaussianParMatCons=GaussianParMatCons[GaussianParMatCons[:,1].argsort(),:]
    NPeaks=len(GaussianParMatCons[:,0])
    std_Acum_Vec=np.zeros(NPeaks)
    RT_interval=boundsMat[0,2]
    std_Acum_Vec[0]=GaussianParMatCons[0,1]
    for peak_id in np.arange(1,NPeaks):
        std_Acum_Vec[peak_id]=std_Acum_Vec[peak_id-1]+GaussianParMatCons[peak_id,1]
    std_Acum_Vec=std_Acum_Vec*stdDistance
    Peak_std_cut=np.where(std_Acum_Vec<RT_interval)[0][-1]+2
    ParametersMat=ParametersMat[:Peak_std_cut,:]
    GaussianParMatCons=GaussianParMatCons[:Peak_std_cut,:]
    return [ParametersMat,GaussianParMatCons]

```
---

## Parameters

---

## Input

- [[stdDistance]]
- [[boundsMat]]
- [[RawGaussPop]]

---

## Output

- [[GaussianParMatCons]]
- [[ParametersMat]]

---

## Functions


---

## Called by

