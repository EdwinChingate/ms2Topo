## Description

The `FitnessSelectorVector` function selects the fittest parameter sets from a population based on their r2 scores, using selector vectors to choose which parameter set should be evaluated, and using `BiggestSelector` to get the indices of the best individuals.

---
## Key operations

- It iterates through the r2 values and selects the individuals with the highest scores from the `Population` based on the `SelectorVectorList`, until the `NSelect` number of individuals is reached, and it also uses `BiggestSelector` to make the selection.

---
## Code

```python
import numpy as np
from BiggestSelector import *
def FitnessSelectorVector(r2Vec,SelectorVectorList,NSelect=0):
    if NSelect==0:
        NSelect=len(SelectorVectorList)
    FitPopulation=[]
    r2Vec_unique=np.array(list(set(r2Vec.copy())))
    Sortr2Vec=(-r2Vec_unique).argsort()  
    r2Vec_unique=r2Vec_unique[Sortr2Vec]
    r2ListFit=[]
    for r2 in r2Vec_unique:
        FittestIndividual_id=np.where(r2Vec==r2)[0][0]
        FittestIndividual=SelectorVectorList[FittestIndividual_id]
        FitPopulation.append(FittestIndividual)
        r2ListFit.append(r2Vec[FittestIndividual_id])   
        if len(FitPopulation)==NSelect:
            break
    return [FitPopulation,r2ListFit]

```
---

## Parameters

---

## Input

- [[SelectorVectorList]]
- [[NSelect]]
- [[r2Vec]]

---

## Output

- [[r2ListFit]]
- [[FitPopulation]]

---

## Functions

- [[BiggestSelector]]

---

## Called by

- [[EvaluatingCombinationsFromVec]]
