## Description

The `SignalsModulesStats` function calculates and stores statistical information about groups of signals, such as mean, standard deviation, maximum and minimum intensity values and the number of signals. The results are stored in the `ModulesStats` variable for analysis of the signal groups.

---
## Key operations

- It calculates the mean, standard deviation, maximum, and minimum of signals within each module, and it appends the number of signals to the statistics. It then sorts the modules by maximum signal.

---
## Code

```python
import numpy as np
def SignalsModulesStats(Modules,SignalVec):
    ModulesStats=[]
    modLoc=0
    for module in Modules:
        Signals=SignalVec[module]
        Signals_mean=np.mean(Signals)
        Signals_std=np.std(Signals)
        Signals_max=np.max(Signals)
        Signals_min=np.min(Signals)
        NSignals=len(module)
        ModulesStats.append([Signals_mean,Signals_std,Signals_max,Signals_min,NSignals,int(modLoc)])
        modLoc+=1
    ModulesStats=np.array(ModulesStats)
    ModulesStats=ModulesStats[ModulesStats[:,2].argsort(),:]
    return ModulesStats

```
---

## Parameters

---

## Input

- [[Modules]]
- [[SignalVec]]

---

## Output

- [[ModulesStats]]

---

## Functions


---

## Called by

- [[LowSignalClustering]]
