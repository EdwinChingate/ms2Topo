## Description

The `GaussianLambda` function returns a lambda function, `GaussianLam`, that can be used to generate a chromatogram based on the provided retention time vector, and a variable number of parameters for the Gaussian peaks, using `GaussianChromatogram`.

---
## Key operations

- The function defines a lambda function, `GaussianLam`, that takes a location and a variable number of parameters as input and uses `GaussianChromatogram` to generate a Gaussian curve.

---
## Code

```python
from GaussianChromatogram import *
def GaussianLambda(RT_vec):
    GaussianLam=lambda loc,*ParametersList: GaussianChromatogram(loc,RT_vec,*ParametersList)
    return GaussianLam

```
---

## Parameters

---

## Input

- [[RT_vec]]

---

## Output

- [[GaussianLam]]

---

## Functions

- [[GaussianChromatogram]]

---

## Called by

