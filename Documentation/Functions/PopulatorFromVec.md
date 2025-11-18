## Description

The `PopulatorFromVec` function creates a population of parameter matrices by selecting subsets of rows from an input parameter matrix, based on a list of binary selector vectors.

---
## Key operations

- The function iterates through each `SelectorVector` in `SelectorVectorList`. For each `SelectorVector`, it identifies the indices where the vector has a value of 1, and it uses these indices to select rows from `ParametersMat` to create a new parameter matrix, which is then added to the `Population` list.

---
## Code

```python
import numpy as np
def PopulatorFromVec(ParametersMat,SelectorVectorList):
    Population=[]
    for SelectorVector in SelectorVectorList:
        KeepVec=np.where(SelectorVector)[0]
        Individual=ParametersMat[KeepVec,:]
        Population.append(Individual)
    return Population

```
---

## Parameters

---

## Input

- [[SelectorVectorList]]
- [[ParametersMat]]

---

## Output

- [[Population]]

---

## Functions


---

## Called by

- [[EvaluatingCombinationsFromVec]]
