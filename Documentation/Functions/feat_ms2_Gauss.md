## Description

`feat_ms2_Gauss` calculates and stores statistical features of MS2 spectra using Gaussian fitting, by calling `ms2_features_stats` to calculate peak statistics, and then storing the results for each feature in the `MS2_features` array.

---
## Key operations

- The function iterates through each MS2 feature in `SummMS2` and calls `ms2_features_stats` to calculate statistics based on Gaussian fitting. It then appends these stats to a list called `MS2_features`, which is returned as an array.

---
## Code

```python
import numpy as np
from ms2_features_stats import *
from Cluster_ms2_Features import *
def feat_ms2_Gauss(DataSet,SummMS2,MS1IDVec,mz_std=2e-3,MS2_to_MS1_ratio=10,stdDistance=3,MaxCount=3,Points_for_regression=5,minSignals=7):
    MS2_features=[]
    N_MS2_features=len(SummMS2[:,0])
    for MS2_id in np.arange(N_MS2_features,dtype='int'):         
        while True:
            try:
                min_RT=SummMS2[MS2_id,5]
                max_RT=SummMS2[MS2_id,6]
                N_spec=SummMS2[MS2_id,7]
                ms2_spec_id=int(SummMS2[MS2_id,8])
                features_stats=ms2_features_stats(DataSet=DataSet,MS2_id=MS2_id,SummMS2=SummMS2,MS1IDVec=MS1IDVec,mz_std=mz_std,MS2_to_MS1_ratio=MS2_to_MS1_ratio,stdDistance=stdDistance,MaxCount=MaxCount,Points_for_regression=Points_for_regression,minSignals=minSignals)
                if len(features_stats)>0:
                    MS2_features.append(features_stats+[min_RT]+[max_RT]+[N_spec]+[ms2_spec_id])                
                break
            except:
                print('error',MS2_id)
                break
    MS2_features=np.array(MS2_features)
    MS2_features=MS2_features[MS2_features[:,3].argsort(),:]
   # ms2_FeaturesDF=Cluster_ms2_Features(MS2_features)
    return MS2_features#ms2_FeaturesDF

```
---

## Parameters

---

## Input

- [[SummMS2]]
- [[Points_for_regression]]
- [[stdDistance]]
- [[MaxCount]]
- [[MS1IDVec]]
- [[MS2_to_MS1_ratio]]
- [[DataSet]]
- [[mz_std]]
- [[minSignals]]

---

## Output

- [[MS2_features#ms2_FeaturesDF]]

---

## Functions

- [[ms2_features_stats]]
- [[Cluster_ms2_Features]]

---

## Called by

