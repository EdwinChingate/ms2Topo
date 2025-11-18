## Description

The `FitnessSelector` function selects the fittest parameter sets from a population based on their r2 scores, using `BiggestSelector` to get the indices of the best individuals.

---
## Key operations

- It iterates through the r2 values and selects the individuals with the highest scores from the `Population` until the `NSelect` number of individuals is reached, and it also uses `BiggestSelector` to make the selection.

---
## Code

```python
import numpy as np
from BiggestSelector import *
def FitnessSelector(r2Vec,Population,NSelect=0):
    if NSelect==0:
        NSelect=len(Population)
    FitPopulation=[]
    r2Vec_unique=np.array(list(set(r2Vec.copy())))
    Sortr2Vec=(-r2Vec_unique).argsort()  
    r2Vec_unique=r2Vec_unique[Sortr2Vec]
    r2ListFit=[]
    for r2 in r2Vec_unique:
        FittestIndividual_id=BiggestSelector(r2=r2,r2Vec=r2Vec,Population=Population)
        if FittestIndividual_id>=0:
            FittestIndividual=Population[FittestIndividual_id]
            FitPopulation.append(Population[FittestIndividual_id])
            r2ListFit.append(r2Vec[FittestIndividual_id])   
        if len(FitPopulation)==NSelect:
            break
    return [FitPopulation,r2ListFit]

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

- [[r2ListFit]]
- [[FitPopulation]]

---

## Functions

- [[BiggestSelector]]

---

## Called by

- [[Mate_Generations]]
- [[Mate_GenerationsColumns]]
- [[Mate_MutantGenerations]]
- [[RefinePop_OnePeak]]
- [[GeneticChromatogram]]
- [[Mate_WildGenerations]]
- [[Mate_FineGenerations]]
- [[RawGaussSeed]]
