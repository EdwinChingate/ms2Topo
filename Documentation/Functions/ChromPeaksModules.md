## Description

The `ChromPeaksModules` function takes grouped feature indices and returns the start and end retention times of each module, using the data from `SummaryChromPeaks`.

---
## Key operations

- It iterates through the `Modules`, extracts the corresponding chromatographic peaks from `SummaryChromPeaks`, and determines the minimum and maximum retention times for each module.

---
## Code

```python
import numpy as np
def ChromPeaksModules(SummaryChromPeaks,Modules,minSpec=10):
    ChromPeaks=[]
    for mod in Modules:
        ChromPeak=SummaryChromPeaks[mod,:]
        early_RT=int(np.min(ChromPeak[:,4]))
        late_RT=int(np.max(ChromPeak[:,5]))
        ChromPeaks.append([early_RT,late_RT])
    ChromPeaks=np.array(ChromPeaks)
    LocMinSpec=ChromPeaks[:,1]-ChromPeaks[:,0]
    ChromPeaks=ChromPeaks[LocMinSpec>minSpec,:]
    return ChromPeaks

```
---

## Parameters

---

## Input

- [[Modules]]
- [[SummaryChromPeaks]]
- [[minSpec]]

---

## Output

- [[ChromPeaks]]

---

## Functions


---

## Called by

