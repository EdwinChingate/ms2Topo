## Description

The `RemoveChromBackGround` function filters the peaks from a chromatogram, based on their width and standard deviations, to reduce the complexity of the data, returning the filtered parameters, and the thresholds for the RT.

---
## Key operations

- The function calculates a new, evenly spaced RT axis, based on the input chromatogram and the number of `ChromPoints`. It then filters the input `GaussianParameters`, removing those parameters that are below the threshold.

---
## Code

```python
import numpy as np
def RemoveChromBackGround(PeakSeed,stdDistance,ChromPoints,stdDistanceDiv=4):
    Chromatogram=PeakSeed[1]
    GaussianParameters=PeakSeed[0]
    min_RT=min(Chromatogram[:,2])
    max_RT=max(Chromatogram[:,2])
    max_std=(max_RT-min_RT)/stdDistanceDiv
    RT_vec=np.linspace(min_RT,max_RT,ChromPoints)
    std_Loc=GaussianParameters[:,1]<max_std
    ParametersMat=GaussianParameters[std_Loc,:]
    TresholdList=[min_RT,max_RT]
    return [ParametersMat,TresholdList,RT_vec]

```
---

## Parameters

---

## Input

- [[ChromPoints]]
- [[stdDistance]]
- [[PeakSeed]]
- [[stdDistanceDiv]]

---

## Output

- [[TresholdList]]
- [[ParametersMat]]
- [[RT_vec]]

---

## Functions


---

## Called by

- [[ResolveChromPeaks]]
