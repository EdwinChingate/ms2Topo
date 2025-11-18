## Description

The `CloseNeighboursList` function generates a list of neighboring signals within a signal vector based on a minimum signal intensity threshold.

---
## Key operations

- It iterates through the signal vector, compares each signal to others based on a minimum intensity difference (`minSignal`), and builds a list where each element contains the indices of the neighboring signals.

---
## Code

```python
import numpy as np
def CloseNeighboursList(SignalVec,minSignal=0):
    if minSignal==0:
        minSignal=np.min(SignalVec)
    NeighboursList=[]
    NSignals=len(SignalVec)
    SignalsSet=set(np.arange(NSignals,dtype='int'))
    for signal_id in SignalsSet:
        signal=SignalVec[signal_id]
        DifSignalVec=np.abs(SignalVec-signal)
        NeighboursLoc=np.where(DifSignalVec<minSignal)[0]
        NeighboursList.append(NeighboursLoc)
    return [NeighboursList,SignalsSet]

```
---

## Parameters

---

## Input

- [[minSignal]]
- [[SignalVec]]

---

## Output

- [[SignalsSet]]
- [[NeighboursList]]

---

## Functions


---

## Called by

- [[LowSignalClustering]]
