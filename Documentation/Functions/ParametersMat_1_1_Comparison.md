## Description

The `ParametersMat_1_1_Comparison` function compares two sets of Gaussian peak parameters, returning a boolean value indicating if the two sets are similar.

---
## Key operations

- The function calculates the relative difference between corresponding elements of the two input matrices. It then compares these differences with `RelDifsAc` to determine if the matrices are similar, and sets the boolean `Pass` accordingly.

---
## Code

```python
import numpy as np
def ParametersMat_1_1_Comparison(ParametersMat1,ParametersMat2,RelDifsAc=10):
    ParametersMatDif=sum(np.abs(ParametersMat1-ParametersMat2))
    ParametersMatSum=sum(ParametersMat1+ParametersMat2)
    RelativeComparison=ParametersMatDif/ParametersMatSum*100
    #print(RelativeComparison)
    RelativeComparisonTest=RelativeComparison<RelDifsAc
    RelativeComparisonTestLoc=np.where(RelativeComparisonTest)[0]
    if len(RelativeComparisonTestLoc)<2:
        Pass=True
    else:
        Pass=False
    return Pass

```
---

## Parameters

---

## Input

- [[ParametersMat2]]
- [[RelDifsAc]]
- [[ParametersMat1]]

---

## Output

- [[Pass]]

---

## Functions


---

## Called by

- [[ExcludeFit]]
