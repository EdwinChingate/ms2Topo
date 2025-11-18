## Description

The `Cluster_ms2_Features` function groups MS2 features based on their adjacency relationships, returning a pandas DataFrame containing the clustered features and their properties.

---
## Key operations

- It uses `AdjacencyListFeatures` to generate an adjacency list and then `ms2_feat_modules` to cluster the features based on this list.

---
## Code

```python
import numpy as np
import pandas as pd
from ms2_feat_modules import *
from AdjacencyListFeatures import *
def Cluster_ms2_Features(MS2_features):    
    AdjacencyList,feat_ids=AdjacencyListFeatures(MS2_features=MS2_features)
    Modules=ms2_feat_modules(AdjacencyList=AdjacencyList,ms2_ids=feat_ids)
    ms2_FeaturesTable=[]
    for mod in Modules:
        MS2_feature=MS2_features[mod,:].copy()
        MS2_feature=MS2_feature[(-MS2_feature[:,5]).argsort(),:]
        min_RT=np.min(MS2_feature[:,12])
        max_RT=np.max(MS2_feature[:,13])  
        N_spec=np.sum(MS2_feature[:,14])
        MS2_feature[0,12]=np.max([min_RT,0])
        MS2_feature[0,13]=max_RT        
        MS2_feature[0,14]=N_spec
        ms2_FeaturesTable.append(MS2_feature[0,:])
    ms2_FeaturesTable=np.array(ms2_FeaturesTable)
    ms2_FeaturesTable=ms2_FeaturesTable[ms2_FeaturesTable[:,3].argsort(),:]
    FeaturesColumns=["ms2_id",
                "ms1_id",
                "RT_(s)",
                "mz_(Da)",
                "mz_std_(Da)",
                "I_tol_1spec",
                "Gauss_r2",
                "N_points_1spec",
                "ConfidenceInterval_(Da)",
                "ConfidenceInterval_(ppm)",
                "min_mz_(Da)",
                "max_mz_(Da)",
                "min_RT_(s)",
               "max_RT_(s)",
               "N_ms2_spec",
                "spectra_id"]
    ms2_FeaturesDF=pd.DataFrame(ms2_FeaturesTable,columns=FeaturesColumns)
    return ms2_FeaturesDF

```
---

## Parameters

---

## Input

- [[MS2_features]]

---

## Output

- [[ms2_FeaturesDF]]

---

## Functions

- [[ms2_feat_modules]]
- [[AdjacencyListFeatures]]

---

## Called by

- [[feat_ms2_Gauss]]
