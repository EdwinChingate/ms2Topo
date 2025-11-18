## Description

The `r2_Model` function quantifies the goodness of fit between a model and the original data by calculating the r² value.

---
## Key operations

- It calculates the mean of the `RawSignal`.
- It calculates the total sum of squares (SS_tot) as the sum of the squared differences between the `RawSignal` and its mean.
- It calculates the residual sum of squares (SS_res) as the sum of the squared differences between the `ModelSignal` and `RawSignal`.
- It calculates the r² value as 1 - (SS_res / SS_tot).

---
## Code

```python
import numpy as np
def r2_Model(RawSignal,ModelSignal):
    Signal_mean=np.mean(RawSignal)
    SS_tot=np.sum((RawSignal-Signal_mean)**2)
    SS_res=np.sum((ModelSignal-RawSignal)**2)
    r2=1-SS_res/SS_tot
    return r2

```
---

## Parameters

---

## Input

- [[ModelSignal]]
- [[RawSignal]]

---

## Output

- [[r2]]

---

## Functions


---

## Called by

- [[EvaluatePopulation]]
