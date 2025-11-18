## Description

The `CosineMatrix` function calculates the cosine similarity between all pairs of MS2 features, based on their aligned fragment data, returning a matrix of cosine similarity values.

---
## Key operations

- The function iterates through all pairs of MS2 features, extracts the aligned fragment data, and then uses `Cosine_2VecSpec` to calculate the cosine similarity between the two features.

---
## Code

```python
import numpy as np
from Cosine_2VecSpec import *
def CosineMatrix(AlignedFragmentsMat,N_features):
    CosineMat=np.zeros((N_features,N_features))
    for feature_id1 in np.arange(N_features,dtype='int'):
        for feature_id2 in np.arange(feature_id1,N_features,dtype='int'):
            AlignedSpecMat=AlignedFragmentsMat[:,[0,feature_id1+1,feature_id2+1]]
            Cosine=Cosine_2VecSpec(AlignedSpecMat=AlignedSpecMat)
            CosineMat[feature_id1,feature_id2]=Cosine
            CosineMat[feature_id2,feature_id1]=Cosine
    return CosineMat

```
---

## Parameters

---

## Input

- [[N_features]]
- [[AlignedFragmentsMat]]

---

## Output

- [[CosineMat]]

---

## Functions

- [[Cosine_2VecSpec]]

---

## Called by

- [[ms2_FeaturesDifferences]]
