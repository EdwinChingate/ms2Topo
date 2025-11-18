## Description

The `MutationTimes` function expands a `Population` of parameter sets by generating mutated offspring using the `MutantOffspring` function, and adding them to the original population. It uses `boundsMat`, `mut_stdVec`, `Mutants` and `stdDistance` to define the mutation process.

---
## Key operations

- The function iterates through each individual's parameter matrix in the input `Population`. For each individual, it generates a set of mutated offspring using the `MutantOffspring` function, using `boundsMat`, `mut_stdVec`, `Mutants` and `stdDistance`. The mutated offspring are added to the original `Population`.

---
## Code

```python
import numpy as np
from MutantOffspring import *
def MutationTimes(Population,boundsMat,mut_stdVec=[0.6,0.7,0.8],Mutants=4,stdDistance=3):
    OriginalPopulation=Population.copy()
    NIndividuals=len(OriginalPopulation)
    for individual in np.arange(NIndividuals,dtype='int'):
        ParametersMat_RawIndividual=OriginalPopulation[individual].copy()
        MutantPopulation=MutantOffspring(ParametersMat=ParametersMat_RawIndividual,boundsMat=boundsMat,Mutants=Mutants,mut_stdVec=mut_stdVec,stdDistance=stdDistance)        
        Population=MutantPopulation+Population
    return Population

```
---

## Parameters

---

## Input

- [[mut_stdVec]]
- [[stdDistance]]
- [[Population]]
- [[0.7]]
- [[0.8]]
- [[Mutants]]
- [[boundsMat]]

---

## Output

- [[Population]]

---

## Functions

- [[MutantOffspring]]

---

## Called by

- [[Mate_MutantGenerations]]
- [[GeneticChromatogram]]
