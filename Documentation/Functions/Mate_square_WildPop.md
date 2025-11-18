## Description

The `Mate_square_WildPop` function generates a new population of parameter sets, `Population`, by combining parameter matrices from the `SeedPopulation`, using the `UniquePeaks` function to remove overlapping peaks, and creating `NOffspring` new parameter sets, while ensuring that the integrals are consistent with the `boundsMat`.

---
## Key operations

- It iterates through all pairs of individuals in the `SeedPopulation`. For each pair, it concatenates the parameter matrices from both individuals, sorts the resulting matrix by retention time, and uses the `UniquePeaks` function to remove overlapping peaks. Then, it creates a new set of `NOffspring` parameter matrices by randomly selecting peaks from the merged matrix. Finally, it adjusts the integral of each offspring matrix to match the original value.

---
## Code

```python
import numpy as np
from UniquePeaks import *
def Mate_square_WildPop(SeedPopulation,boundsMat,NOffspring=3):
    NSeedIndividuals=len(SeedPopulation)
    Integral=boundsMat[2,1]
    NPeaks=len(SeedPopulation[0])
    Population=SeedPopulation.copy()
    for individual_1 in np.arange(NSeedIndividuals,dtype='int'):
        ParametersMat_i1=SeedPopulation[individual_1].copy()        
        for individual_2 in np.arange(individual_1,NSeedIndividuals,dtype='int'):
            ParametersMat_i2=SeedPopulation[individual_2].copy()
            ParametersMat=np.append(ParametersMat_i1,ParametersMat_i2,axis=0)
            ParametersMat=ParametersMat[ParametersMat[:,0].argsort(),:]   
            ParametersMat=UniquePeaks(ParametersMat,PeakTol=[0.1,0.01,1e3])
            NNPeaks=len(ParametersMat[:,0])
            if NNPeaks==NPeaks:
                break
            for offs in np.arange(NOffspring):
                RandomPeaks=np.random.randint(low=0,high=NNPeaks,size=NPeaks)
                NewParametersMat=ParametersMat[RandomPeaks,:]
                PeaksIntegral=np.sum(NewParametersMat[:,2])
                NewParametersMat[:,2]=NewParametersMat[:,2]*Integral/PeaksIntegral
                Population.append(NewParametersMat)
    return Population

```
---

## Parameters

---

## Input

- [[NOffspring]]
- [[SeedPopulation]]
- [[boundsMat]]

---

## Output

- [[Population]]

---

## Functions

- [[UniquePeaks]]

---

## Called by

- [[Mate_WildGenerations]]
