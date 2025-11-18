## Description

The `Mate_square_GaussParPop` function generates a new population of parameter sets, `Population`, by combining parameter matrices from the `SeedPopulation`.

---
## Key operations

- It iterates through all pairs of individuals in the `SeedPopulation`. For each pair, it creates a new parameter matrix using the parameters of the first individual, and appends it to the `Population` list.

---
## Code

```python
import numpy as np
def Mate_square_GaussParPop(SeedPopulation):
    NSeedIndividuals=len(SeedPopulation)
    NPeaks=len(SeedPopulation[0])
    Population=[]
    for individual_1 in np.arange(NSeedIndividuals,dtype='int'):
        ParametersMat_i1=SeedPopulation[individual_1]        
        for individual_2 in np.arange(individual_1,NSeedIndividuals,dtype='int'):
            ParametersMat_i2=SeedPopulation[individual_2]
            randomCut_seed=np.random.random()
            randomCut_loc=int(randomCut_seed*(NPeaks-2))+1
            ParametersMat=ParametersMat_i1.copy()
            ParametersMat[randomCut_loc:,:]=ParametersMat_i2[randomCut_loc:,:]
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

- [[Mate_Generations]]
- [[Mate_MutantGenerations]]
- [[Mate_FineGenerations]]
