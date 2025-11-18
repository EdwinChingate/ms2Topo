## Description

`AdjacencyList_ms2Fragments` creates a list of neighboring MS2 fragments by comparing their m/z values, using the fragment m/z and a tolerance to determine proximity and storing the results in `AdjacencyList`, also returning a set of indices for fragments that have neighbors.

---
## Key operations

- It calculates the minimum and maximum m/zvalues for each fragment using the m/zand its confidence interval, and it identifies neighboring fragments within these ranges. The indices of neighboring fragments are added to the adjacency list.

---
## Code

```python
import numpy as np
def AdjacencyList_ms2Fragments(All_ms2):
    N_fragments=len(All_ms2[:,0])
    mzMaxVec=All_ms2[:,0]+All_ms2[:,5]
    mzMinVec=All_ms2[:,0]-All_ms2[:,5]
    AdjacencyList=[]
    frag_ids=[]
    for feat_id in np.arange(N_fragments):
        mz=All_ms2[feat_id,0]
        mz_CI=All_ms2[feat_id,5]
        min_mz=mz-mz_CI
        max_mz=mz+mz_CI        
        NearFilter=(mzMaxVec>min_mz)&(mzMinVec<max_mz)
        Neigbours=np.where(NearFilter)[0]    
        AdjacencyList.append(Neigbours)
        if len(Neigbours)>0:
            frag_ids.append(feat_id)
    frag_ids=set(frag_ids)
    return [AdjacencyList,frag_ids]

```
---

## Parameters

---

## Input

- [[All_ms2]]

---

## Output

- [[AdjacencyList]]
- [[frag_ids]]

---

## Functions


---

## Called by

- [[ms2_FeaturesDifferences]]
