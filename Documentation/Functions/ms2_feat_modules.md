## Description

The `ms2_feat_modules` function uses an adjacency list and a set of MS2 IDs to iteratively group related MS2 features into modules by recursively exploring connected components of a graph.

---
## Key operations

- It iteratively selects an MS2 ID and clusters it using `AdjacencyClustering`.
- It removes the clustered IDs and continues with the rest, until all ids have been clustered.

---
## Code

```python
from AdjacencyClustering import *
def ms2_feat_modules(AdjacencyList,ms2_ids):
    Modules=[]
    while len(ms2_ids)>0:        
        ms2_candidate_id=list(ms2_ids)[0]
        module=AdjacencyClustering(ms2_id=ms2_candidate_id,AdjacencyList=AdjacencyList)
        ms2_ids=ms2_ids-set(module)
        Modules.append(module)
    return Modules

```
---

## Parameters

---

## Input

- [[AdjacencyList]]
- [[ms2_ids]]

---

## Output

- [[Modules]]

---

## Functions

- [[AdjacencyClustering]]

---

## Called by

- [[mz_mz_std_ms1]]
- [[ms2_FeaturesDifferences]]
- [[Cluster_ms2_Features]]
- [[ms2_SpectralSimilarityClustering]]
- [[LowSignalClustering]]
