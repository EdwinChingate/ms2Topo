## Description

The `RandomVecGen` function generates a vector of random numbers with the size defined by `NPeaks`.

---
## Key operations

- The function uses a random number generator to create a NumPy array of random floats with a size specified by `NPeaks`.

---
## Code

```python
import numpy as np
def RandomVecGen(NPeaks):
    rng = np.random.default_rng()
    RandomVec=rng.random(size=NPeaks)
    return RandomVec

```
---

## Parameters

---

## Input

- [[NPeaks]]

---

## Output

- [[RandomVec]]

---

## Functions


---

## Called by

- [[Mutate]]
