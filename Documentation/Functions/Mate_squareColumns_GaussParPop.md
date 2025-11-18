## Description

The `Mate_squareColumns_GaussParPop` function generates a new population of parameter sets, `Population`, by combining the columns of parameter matrices from the `SeedPopulation`.

---
## Key operations

- It iterates through all pairs of individuals in the `SeedPopulation`. For each pair, it takes the parameter matrix from the first individual, and replaces its last column with the last column of the second individual. The resulting matrix is then appended to the `Population` list.

---
## Code

```python
import numpy as np
def Mate_squareColumns_GaussParPop(SeedPopulation):
    NSeedIndividuals=len(SeedPopulation)
    NPeaks=len(SeedPopulation[0])
    Population=[]
    for individual_1 in np.arange(NSeedIndividuals,dtype='int'):
        ParametersMat_i1=SeedPopulation[individual_1]        
        for individual_2 in np.arange(individual_1,NSeedIndividuals,dtype='int'):
            ParametersMat_i2=SeedPopulation[individual_2]
            ParametersMat=ParametersMat_i1.copy()
            ParametersMat[:,2]=ParametersMat_i2[:,2]
            Population.append(ParametersMat)
    return Population

```
---

## Parameters

---

## Input

- [[SeedPopulation]]

---

## Output

- [[Population]]

---

## Functions


---

## Called by

- [[Mate_GenerationsColumns]]
