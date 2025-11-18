## Description

The `Cosine_2VecSpec` function calculates the cosine similarity between two vectors, providing a measure of their similarity.

---
## Key operations

- The function calculates the dot product of the two vectors, divides it by the product of their magnitudes and returns the resulting value.

---
## Code

```python
import numpy as np
def Cosine_2VecSpec(AlignedSpecMat):
    S1_dot_S2=np.sum(AlignedSpecMat[:,1]*AlignedSpecMat[:,2])
    S1_dot_S1=np.sum(AlignedSpecMat[:,1]*AlignedSpecMat[:,1])
    S2_dot_S2=np.sum(AlignedSpecMat[:,2]*AlignedSpecMat[:,2])
    dotXdot=S1_dot_S1*S2_dot_S2
    if dotXdot==0:
        return 0
    Cosine=S1_dot_S2/np.sqrt(dotXdot)
    return Cosine

```
---

## Parameters

---

## Input

- [[AlignedSpecMat]]

---

## Output

- [[Cosine]]
- [[0]]

---

## Functions


---

## Called by

- [[Similarity_2Spectra]]
- [[CosineMatrix]]
- [[Cosine_2Spectra]]
