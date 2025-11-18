## Description

The `EvaluatePopulationIntensity` function assesses the fitness of each individual in a population based on the intensity of the largest peak in the chromatogram generated with each individual's parameters.

---
## Key operations

- It iterates through each individual (parameter set) in the `Population`, calculates the intensity of the most intense peak, and stores these values in the output array.

---
## Code

```python
import numpy as np
def EvaluatePopulationIntensity(Population):
    NIndividuals=len(Population)
    BiggestPeakVec=np.zeros(NIndividuals)
    for individual_id in np.arange(NIndividuals, dtype='int'):
        Individual=Population[individual_id]
        MostIntensePeakInt=np.max(Individual[:,2]/Individual[:,1])
        BiggestPeakVec[individual_id]=MostIntensePeakInt    
    return BiggestPeakVec

```
---

## Parameters

---

## Input

- [[Population]]

---

## Output

- [[BiggestPeakVec]]

---

## Functions


---

## Called by

- [[FitnessPeakSelector]]
