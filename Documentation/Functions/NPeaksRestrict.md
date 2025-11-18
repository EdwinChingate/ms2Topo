## Description

The `NPeaksRestrict` function calculates a number of peaks to keep, `NPeaks_std_cut`, based on the cumulative standard deviations of the Gaussian parameters of the peaks in `GaussianParMat`, after sorting them by standard deviation and using `stdDistance`. The function uses `boundsMat` to calculate a threshold for the standard deviation.

---
## Key operations

- It sorts the `GaussianParMat` by the standard deviation of the peaks. It then calculates the cumulative standard deviation of the peaks, multiplying the result by `stdDistance`. The function determines the number of peaks to keep (`NPeaks_std_cut`) based on this cumulative standard deviation, and the parameter boundaries from `boundsMat`, although the exact criteria for this is not detailed in the source code.

---
## Code

```python
import numpy as np
def NPeaksRestrict(GaussianParMat,boundsMat,stdDistance=4):
    GaussianParMat=GaussianParMat[GaussianParMat[:,1].argsort(),:]
    NPeaks=len(GaussianParMat[:,0])
    std_Acum_Vec=np.zeros(NPeaks)
    RT_interval=boundsMat[0,2]
    std_Acum_Vec[0]=GaussianParMat[0,1]
    for peak_id in np.arange(1,NPeaks):
        std_Acum_Vec[peak_id]=std_Acum_Vec[peak_id-1]+GaussianParMat[peak_id,1]
    std_Acum_Vec=std_Acum_Vec*stdDistance
    NPeaks_std_cut=np.where(std_Acum_Vec<RT_interval)[0][-1]+2
    return NPeaks_std_cut

```
---

## Parameters

---

## Input

- [[stdDistance]]
- [[boundsMat]]
- [[GaussianParMat]]

---

## Output

- [[NPeaks_std_cut]]

---

## Functions


---

## Called by

- [[RawParametersCut]]
