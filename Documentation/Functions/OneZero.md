## Description

The `OneZero` function generates a `SelectorVectorList` containing binary selection vectors of length `NPeaks`, with different combinations of ones and zeros, that are used to select or deselect peaks.

---
## Key operations

- The function generates a list of binary vectors, `SelectorVectorList`, where each vector is a combination of 0's and 1's. Each binary vector has a length equal to the number of peaks, which is provided in the `NPeaks` variable.

---
## Code

```python
import numpy as np
def OneZero(SelectorVector,NPeaks,SelectorVectorList=[]):
    OnesVec=np.where(SelectorVector==1)[0]
    for one in OnesVec:
        SelectorOne=SelectorVector.copy()
        SelectorOne[one]=0
        if sum(SelectorOne)>NPeaks:
            SelectorVectorList=OneZero(SelectorVector=SelectorOne,NPeaks=NPeaks,SelectorVectorList=SelectorVectorList)
        else:
            SelectorVectorList.append(SelectorOne)
    return SelectorVectorList

```
---

## Parameters

---

## Input

- [[SelectorVector]]
- [[SelectorVectorList]]
- [[NPeaks]]

---

## Output

- [[SelectorVectorList]]

---

## Functions


---

## Called by

- [[EvaluatingCombinationsFromVec]]
