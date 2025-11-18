## Description

`UpdatingChromMat` scales the contribution of each peak in a chromatogram matrix based on a vector of pre-calculated contributions, modifying the `ChromatogramMatrix` to produce `Updated_ChromatogramMatrix`.

---
## Key operations

- The function multiplies the chromatogram matrix by the contributions vector to scale the contribution of each peak.

---
## Code

```python
import numpy as np
def UpdatingChromMat(ChromatogramMatrix,ContributionsVec):
    Updated_ChromatogramMatrix=ChromatogramMatrix.copy()
    NContributions=len(ContributionsVec)
    for peak_id in np.arange(NContributions,dtype='int'):
        Updated_ChromatogramMatrix[:,peak_id]=ChromatogramMatrix[:,peak_id]*ContributionsVec[peak_id]
    return Updated_ChromatogramMatrix

```
---

## Parameters

---

## Input

- [[ContributionsVec]]
- [[ChromatogramMatrix]]

---

## Output

- [[Updated_ChromatogramMatrix]]

---

## Functions


---

## Called by

- [[first_round_chromatogram_deconvolution]]
- [[RefineChromPeak]]
- [[RefineParameters]]
