## Description

The `GaussianPeak` function calculates and returns a Gaussian curve intensity, `Gaussian_Int`, based on the input m/z values, center m/z, standard deviation, and total intensity.

---
## Key operations

- It applies the Gaussian function formula using the inputs `mz_vec`, `mz`, `mz_std`, and `I_total` and returns a NumPy array representing the Gaussian peak intensity across the given `mz_vec`.

---
## Code

```python
import numpy as np
def GaussianPeak(mz_vec,mz,mz_std,I_total):
    LogVec=-((mz_vec-mz)/mz_std)**2/2
    f1_sqrt2pi=0.3989422804014327 #1/np.sqrt(np.pi*2) 
    Gaussian_Int=np.exp(LogVec)*f1_sqrt2pi*I_total/mz_std
    return Gaussian_Int

```
---

## Parameters

---

## Input

- [[mz_vec]]
- [[mz]]
- [[I_total]]
- [[mz_std]]

---

## Output

- [[Gaussian_Int]]

---

## Functions


---

## Called by

- [[Normal_Fit]]
- [[r2_Gauss]]
