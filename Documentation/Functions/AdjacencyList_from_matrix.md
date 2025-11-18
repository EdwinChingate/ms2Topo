## Description

`AdjacencyList_from_matrix` transforms a matrix of spectral relationships into a list of neighboring indices, using a minimum adjacency threshold to define neighbors, for use in graph-based clustering.

---
## Key operations

- It initializes an empty adjacency list. It iterates through the adjacency matrix, and if a similarity value is above the `minAdjacency` threshold, the index of the neighboring spectra is added to the adjacency list.

---
## Code

```python
import numpy as np
def AdjacencyList_from_matrix(AdjacencyMatrix,N_ms2_spectra,minAdjacency=0):
    AdjacencyList=[]
    ms2_ids=[]
    for ms2_candidate_id in np.arange(N_ms2_spectra,dtype='int'):
        Neigbours=np.where(AdjacencyMatrix[ms2_candidate_id,:]>minAdjacency)[0]
        if len(Neigbours)>0:
            ms2_ids.append(ms2_candidate_id)
        AdjacencyList.append(Neigbours)
    ms2_ids=set(ms2_ids) 
    return [AdjacencyList,ms2_ids]

```
---

## Parameters

---

## Input

- [[minAdjacency]]
- [[AdjacencyMatrix]]
- [[N_ms2_spectra]]

---

## Output

- [[AdjacencyList]]
- [[ms2_ids]]

---

## Functions


---

## Called by

- [[ms2_FeaturesDifferences]]
