## Description

The `Similarity_AdjacencyMatrix` function constructs a matrix that represents the pairwise spectral similarity between MS2 spectra, by using the `SimilarityNeigbours` function for each spectrum to determine its neighbors and their relationship to it.

---
## Key operations

- It initializes a diagonal adjacency matrix, then iterates through each MS2 spectrum, calling the function `SimilarityNeigbours` to update the matrix.

---
## Code

```python
import numpy as np
from SimilarityNeigbours import *
def Similarity_AdjacencyMatrix(SpectraList,SummMS2,RT_tol=30,cos_tol=0.95,Tanimoto_tol=0.6,mz_maxDif=1e-2,min_Int_Frac=5):    
    N_ms2_spectra=len(SummMS2[:,0])
    AdjacencyMatrix=np.diag(np.ones(N_ms2_spectra))
    for ms2_candidate_id1 in np.arange(N_ms2_spectra,dtype='int'):
        AdjacencyMatrix=SimilarityNeigbours(SpectraList=SpectraList,AdjacencyMatrix=AdjacencyMatrix,SummMS2=SummMS2,ms2_candidate_id1=ms2_candidate_id1,RT_tol=RT_tol,cos_tol=cos_tol,Tanimoto_tol=Tanimoto_tol,mz_maxDif=mz_maxDif,min_Int_Frac=min_Int_Frac)
    return AdjacencyMatrix

```
---

## Parameters

---

## Input

- [[SummMS2]]
- [[Tanimoto_tol]]
- [[SpectraList]]
- [[cos_tol]]
- [[mz_maxDif]]
- [[min_Int_Frac]]
- [[RT_tol]]

---

## Output

- [[AdjacencyMatrix]]

---

## Functions

- [[SimilarityNeigbours]]

---

## Called by

