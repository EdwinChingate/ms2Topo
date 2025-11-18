## Description

The `DistanceDistribution` function computes the minimum value and the mean difference between consecutive signal intensities, which helps in understanding the signal's distribution.

---
## Key operations

- It sorts the input signal vector, calculates the differences between consecutive values, computes the mean of these differences, and stores the minimum signal and the mean difference into the output list.

---
## Code

```python
import numpy as np
def DistanceDistribution(SignalVec0):
    SignalVec=SignalVec0[SignalVec0.argsort()].copy()
    Low_Signal=SignalVec[:-1]
    High_Signal=SignalVec[1:]
    Dif_Signal=High_Signal-Low_Signal
    Dif_Int_mean=np.mean(Dif_Signal)
    Dif_Int_std=np.mean(Dif_Signal)
    Signal_min=SignalVec[0]
    LowerSignalDist=[Signal_min,Dif_Int_mean]
    return LowerSignalDist

```
---

## Parameters

---

## Input

- [[SignalVec0]]

---

## Output

- [[LowerSignalDist]]

---

## Functions


---

## Called by

- [[Feat_RT_edges]]
