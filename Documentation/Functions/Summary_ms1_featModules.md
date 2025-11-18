## Description

`Summary_ms1_featModules` extracts and organizes the most intense peak information from each module in `SummaryPeaks` and outputs them as a single list named `mz_feat`.

---
## Key operations

- The function iterates through each module, extracts the corresponding peaks from `SummaryPeaks`, sorts them by a specific column, and appends the last peak of the sorted peaks to the `mz_feat` list.

---
## Code

```python
import numpy as np
def Summary_ms1_featModules(Modules,SummaryPeaks):
    mz_feat=[]
    for mod in Modules:
        summary_peak=SummaryPeaks[mod,:]
        summary_peak=summary_peak[summary_peak[:,1].argsort(),:]
        mz_feat.append(summary_peak[-1,:])
    mz_feat=np.array(mz_feat)
    return mz_feat

```
---

## Parameters

---

## Input

- [[Modules]]
- [[SummaryPeaks]]

---

## Output

- [[mz_feat]]

---

## Functions


---

## Called by

- [[mz_mz_std_ms1]]
