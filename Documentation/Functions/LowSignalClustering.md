## Description

The `LowSignalClustering` function clusters low-intensity signals from the input `SignalVec0`, using `CloseNeighboursList` and `ms2_feat_modules`, and returns a list, `NoiseTresList`, containing the noise threshold and the indices of the signals that are considered low intensity signals, after calculating the statistics of the modules using `SignalsModulesStats`.

---
## Key operations

- It filters the `SignalVec0` to keep only positive signal values. It uses the `CloseNeighboursList` function to find neighboring signals and the `ms2_feat_modules` function to cluster the signals based on the proximity. Then, the function calculates the descriptive statistics of each module of signals using `SignalsModulesStats`. Finally, it selects one of the modules, based on the noise threshold and returns the `NoiseTresList`.

---
## Code

```python
from CloseNeighboursList import *
from ms2_feat_modules import *
from SignalsModulesStats import *
def LowSignalClustering(SignalVec0,minSignal=0):
    ZeroFil=SignalVec0>0
    SignalVec=SignalVec0[ZeroFil]    
    NeighboursList,SignalsSet=CloseNeighboursList(SignalVec,minSignal=minSignal)
    Modules=ms2_feat_modules(AdjacencyList=NeighboursList,ms2_ids=SignalsSet)
    ModulesStats=SignalsModulesStats(Modules,SignalVec)
    NoiseTresVec=ModulesStats[0,:]
    modLoc=int(NoiseTresVec[-1])
    Module=Modules[modLoc]
    NoiseTresList=[NoiseTresVec,Module]
    return NoiseTresList

```
---

## Parameters

---

## Input

- [[minSignal]]
- [[SignalVec0]]

---

## Output

- [[NoiseTresList]]

---

## Functions

- [[ms2_feat_modules]]
- [[CloseNeighboursList]]
- [[SignalsModulesStats]]

---

## Called by

- [[CuttingFreq]]
- [[Feat_RT_edges]]
