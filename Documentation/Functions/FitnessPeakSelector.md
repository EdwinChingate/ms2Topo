## Description

The `FitnessPeakSelector` function selects the fittest parameter sets from a population based on the product of their r2 score and the intensity of the biggest peak in each set, using `EvaluatePopulationIntensity` to get the peak intensities.

---
## Key operations

- It uses `EvaluatePopulationIntensity` to obtain a vector of the maximum intensity of each individual in the population, and multiplies this value by the r2 of each individual. The function then selects the `NSelect` individuals with the highest score.

---
## Code

```python
import numpy as np
from EvaluatePopulationIntensity import *
def FitnessPeakSelector(r2Vec,Population,NSelect=0):
    if NSelect==0:
        NSelect=len(Population)
    BiggestPeakVec=EvaluatePopulationIntensity(Population=Population)
    BiggestPeak_r2_Vec=BiggestPeakVec*r2Vec
    FitPopulation=[]
    BiggestPeak_r2_Vec_unique=np.array(list(set(BiggestPeak_r2_Vec.copy())))
    SortbpVec=(-BiggestPeak_r2_Vec_unique).argsort()  
    BiggestPeak_r2_Vec_unique=BiggestPeak_r2_Vec_unique[SortbpVec]
    bp_r2ListFit=[]
    for bp_r2 in BiggestPeak_r2_Vec_unique:
        BestIndividual_id=np.where(BiggestPeak_r2_Vec==bp_r2)[0][0]
        FitPopulation.append(Population[BestIndividual_id])
        bp_r2ListFit.append(BestIndividual_id)   
        if len(FitPopulation)==NSelect:
            break
    return [FitPopulation,bp_r2ListFit]

```
---

## Parameters

---

## Input

- [[Population]]
- [[NSelect]]
- [[r2Vec]]

---

## Output

- [[bp_r2ListFit]]
- [[FitPopulation]]

---

## Functions

- [[EvaluatePopulationIntensity]]

---

## Called by

