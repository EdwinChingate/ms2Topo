## Description

`AdjacencyClustering` recursively identifies clusters of related features, using the `AdjacencyList` to navigate a graph structure and the `Module` variable to keep track of already clustered elements.

---
## Key operations

- It uses a recursive approachto identify all connected nodes in a graph represented by the `AdjacencyList`. It ensures that each node is only visited once, avoiding infinite loops, and it builds the clustersby iteratively adding neighboring elements.

---
## Code

```python
import numpy as np
def AdjacencyClustering(ms2_id,AdjacencyList,Module=[]):
    CurrentModule=set(AdjacencyList[ms2_id])
    CurrentModule=CurrentModule-set(Module)   
    Module=Module+list(CurrentModule)
    for ms2_id in CurrentModule: 
        Module=AdjacencyClustering(ms2_id=ms2_id,AdjacencyList=AdjacencyList,Module=Module)
    return Module

```
---

## Parameters

---

## Input

- [[AdjacencyList]]
- [[ms2_id]]
- [[Module]]

---

## Output

- [[Module]]

---

## Functions


---

## Called by

- [[ms2_feat_modules]]
