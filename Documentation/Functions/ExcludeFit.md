## Description

The `ExcludeFit` function compares a set of parameters with a previously identified best set of parameters, and based on the result it indicates whether the set should be kept or excluded.

---
## Key operations

- It calls `ParametersMat_1_1_Comparison` to compare parameters from the `FitPopulation` against the `FittestIndividual`, and returns `True` or `False` based on the result of the comparison.

---
## Code

```python
from ParametersMat_1_1_Comparison import *
def ExcludeFit(FittestIndividual,FitPopulation):
    for ParametersMat in FitPopulation:
        ParametersMat2=ParametersMat
        Pass=ParametersMat_1_1_Comparison(ParametersMat1=FittestIndividual,ParametersMat2=ParametersMat2,RelDifsAc=20)
        if not Pass:
            return False
    return True

```
---

## Parameters

---

## Input

- [[FittestIndividual]]
- [[FitPopulation]]

---

## Output

- [[True]]
- [[False]]

---

## Functions

- [[ParametersMat_1_1_Comparison]]

---

## Called by

