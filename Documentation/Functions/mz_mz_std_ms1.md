## Description

The `mz_mz_std_ms1` function groups MS1 peaks based on their m/z values, then it calculates a summary of the m/z features for each group, and filters out the features with zero intensities.

---
## Key operations

- It calculates the mean and standard deviation of m/z values for each group of peaks defined by `edgesVecList` using `PeakFeatStats`.
- It generates an adjacency list of the peaks, using `AdjacencyList_mz`, grouping the peaks that are within a certain distance of each other, as defined by `stdDistance`.
- It clusters the peaks based on their adjacency, using `ms2_feat_modules`, resulting in groups of connected peaks.
- It summarizes the MS1 features for each module using `Summary_ms1_featModules`.
- It filters out modules with zero intensity values.

---
## Code

```python
from PeakFeatStats import *
from AdjacencyList_mz import *
from Summary_ms1_featModules import *
from AdjacencyList_mz import *
from ms2_feat_modules import *
def mz_mz_std_ms1(edgesVecList,SomePeaks,stdDistance=3):
    SummaryPeaks=np.array(list(map(lambda edgesVec: PeakFeatStats(edgesVec,Peaks=SomePeaks), edgesVecList)))    
    AdjacencyList,feat_ids=AdjacencyList_mz(MS2_features=SummaryPeaks,mz_col=0,mz_CI_col=1,mz_Tol=0,stdDistance=3)
    Modules=ms2_feat_modules(AdjacencyList=AdjacencyList,ms2_ids=feat_ids)
    mz_feat=Summary_ms1_featModules(Modules=Modules,SummaryPeaks=SummaryPeaks)
    zeroT=mz_feat[:,1]>0
    mz_feat=mz_feat[zeroT,:]
    return mz_feat

```
---

## Parameters

---

## Input

- [[SomePeaks]]
- [[stdDistance]]
- [[edgesVecList]]

---

## Output

- [[mz_feat]]

---

## Functions

- [[ms2_feat_modules]]
- [[AdjacencyList_mz]]
- [[Summary_ms1_featModules]]
- [[PeakFeatStats]]

---

## Called by

