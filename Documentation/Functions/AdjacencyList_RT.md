## Description

`AdjacencyList_RT` creates a list of neighboring chromatographic peaks by comparing their retention times, using confidence intervals or a specified tolerance and a standard distance to determine proximity, and it stores them in `AdjacencyList`, also returning the ids of the peaks that have neighbors.

---
## Key operations

- It calculates the minimum and maximum RT values based on the RT confidence intervals or the given tolerance, and it identifies neighboring peaks within these ranges using a specified standard distance (`stdDistance`). It builds a list of neighboring peak indices in `AdjacencyList`.

---
## Code

```python
import numpy as np
def AdjacencyList_RT(ChromPeaks,RT_col=3,RT_CI_col=8,RT_Tol=0,stdDistance=3):
    N_signals=len(ChromPeaks[:,0])
    if RT_Tol==0:
        RT_CI_Vec=ChromPeaks[:,RT_CI_col]
    else:
        RT_CI_Vec=np.ones(N_signals)*RT_Tol
    RTVec=ChromPeaks[:,RT_col]
    RTMaxVec=RTVec+RT_CI_Vec*stdDistance
    RTMinVec=RTVec-RT_CI_Vec*stdDistance
    AdjacencyList=[]
    peak_ids=[]
    for peak_id in np.arange(N_signals):
        min_RT=RTMinVec[peak_id]
        max_RT=RTMaxVec[peak_id]       
        NearFilter=(RTMaxVec>=min_RT)&(RTMinVec<=max_RT)
        Neigbours=np.where(NearFilter)[0]    
        AdjacencyList.append(Neigbours)
        if len(Neigbours)>0:
            peak_ids.append(peak_id)
    peak_ids=set(peak_ids)
    return [AdjacencyList,peak_ids]

```
---

## Parameters

---

## Input

- [[stdDistance]]
- [[RT_CI_col]]
- [[RT_col]]
- [[ChromPeaks]]
- [[RT_Tol]]

---

## Output

- [[AdjacencyList]]
- [[peak_ids]]

---

## Functions


---

## Called by

