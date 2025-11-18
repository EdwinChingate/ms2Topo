## Description

The `EvaluatePopulation` function assesses how well each parameter set in a population fits a smoothed chromatogram, returning a list of r2 values for each parameter set.

---
## Key operations

- It iterates through each individual in the population, uses `OverlappingGaussPeaks` to model a chromatogram based on the individual's parameters, and then uses `r2_Model` to compare the modeled chromatogram with the smoothed signal and obtain the r2 value.

---
## Code

```python
import numpy as np
from r2_Model import *
from OverlappingGaussPeaks import *
def EvaluatePopulation(Population,smooth_peaks):
    NIndividuals=len(Population)
    RT_vec=smooth_peaks[:,0]
    Int_vec=smooth_peaks[:,1]
    r2List=[]
    for individual in np.arange(NIndividuals, dtype='int'):
        ChromatogramMatrix=OverlappingGaussPeaks(RT_vec=RT_vec,ParametersMat=Population[individual])
        Int_model=sum(ChromatogramMatrix.T)
        r2=r2_Model(RawSignal=Int_vec,ModelSignal=Int_model)
        r2List.append(r2)
    r2Vec=np.array(r2List,dtype='f2')
    return r2Vec

```
---

## Parameters

---

## Input

- [[Population]]
- [[smooth_peaks]]

---

## Output

- [[r2Vec]]

---

## Functions

- [[r2_Model]]
- [[OverlappingGaussPeaks]]

---

## Called by

- [[Mate_Generations]]
- [[Mate_GenerationsColumns]]
- [[Mate_MutantGenerations]]
- [[RefinePop_OnePeak]]
- [[GeneticChromatogram]]
- [[Mate_WildGenerations]]
- [[Mate_FineGenerations]]
