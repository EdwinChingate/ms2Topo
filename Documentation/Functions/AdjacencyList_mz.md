## Description

`AdjacencyList_mz` creates a list of neighboring MS2 features by comparing their m/z values, using either a confidence interval or a tolerance to determine proximity, and it stores the results in `AdjacencyList`, while also returning the ids of the features that have neighbors.

---
## Key operations

- It calculates the minimum and maximum m/zvalues using the m/zand its confidence interval, or a given tolerance, and it identifies neighboring features within those ranges. It adds the indices of neighboring features to the adjacency list.

---
## Code

```python
import numpy as np
def AdjacencyList_mz(MS2_features,mz_col=3,mz_CI_col=8,mz_Tol=0,stdDistance=3):
    N_possible_feat=len(MS2_features[:,0])
    if mz_Tol==0:
        mz_CI_Vec=MS2_features[:,mz_CI_col]
    else:
        mz_CI_Vec=np.ones(N_possible_feat)*mz_Tol
    mzVec=MS2_features[:,mz_col]
    mzMaxVec=mzVec+mz_CI_Vec*stdDistance
    mzMinVec=mzVec-mz_CI_Vec*stdDistance
    AdjacencyList=[]
    feat_ids=[]
    for feat_id in np.arange(N_possible_feat):
        min_mz=mzMinVec[feat_id]
        max_mz=mzMaxVec[feat_id]       
        NearFilter=(mzMaxVec>=min_mz)&(mzMinVec<=max_mz)
        Neigbours=np.where(NearFilter)[0]    
        AdjacencyList.append(Neigbours)
        if len(Neigbours)>0:
            feat_ids.append(feat_id)
    feat_ids=set(feat_ids)
    return [AdjacencyList,feat_ids]

```
---

## Parameters

---

## Input

- [[mz_CI_col]]
- [[mz_col]]
- [[MS2_features]]
- [[stdDistance]]
- [[mz_Tol]]

---

## Output

- [[AdjacencyList]]
- [[feat_ids]]

---

## Functions


---

## Called by

- [[mz_mz_std_ms1]]
