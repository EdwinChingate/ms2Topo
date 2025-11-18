## Description

The `MutantOffspring` function generates a new population of mutated parameters, `MutantPopulation`, by creating a tensor of the original parameters, and using `MutateParameters` to apply mutations, guided by `boundsMat` and `mut_stdVec`. It extracts the mutated parameters using `MutantansExtractor`.

---
## Key operations

- It creates a tensor (`MutationTensor`) by stacking copies of the input `ParametersMat`. It then iterates through each parameter in `ParametersMat`, using the `boundsMat` and `mut_stdVec` to determine the allowed range and the standard deviation for the mutation.  The `MutateParameters` function is used to generate the mutated parameters for each individual. Finally, it extracts the mutated parameters from the `MutationTensor` using `MutantansExtractor`, and saves them to `MutantPopulation`.

---
## Code

```python
import numpy as np
from MutateParameters import *
from MutantansExtractor import *
def MutantOffspring(ParametersMat,boundsMat,stdDistance,Mutants=4,mut_stdVec=[0.6,0.7,0.8]):
    NPeaks=len(ParametersMat[:,0])
    NParameters=len(ParametersMat[0,:])
    MutationTensor=np.stack([ParametersMat]*Mutants,axis=0)
    try:
        for parameter_id in np.arange(NParameters):
            boundsVec=boundsMat[parameter_id,:]
            parameter_interval=boundsMat[parameter_id,2]
            mut_std=mut_stdVec[parameter_id]
            ParametersVec=ParametersMat[:,parameter_id]
            MutationTensor[:,:,parameter_id]=MutateParameters(ParametersVec=ParametersVec,boundsVec=boundsVec,parameter_std=mut_std,Mutants=Mutants)
    except:
        ShowDF(boundsMatRef)
    MutantPopulation=MutantansExtractor(MutationTensor=MutationTensor,Mutants=Mutants)
    return MutantPopulation

```
---

## Parameters

---

## Input

- [[mut_stdVec]]
- [[stdDistance]]
- [[ParametersMat]]
- [[0.7]]
- [[0.8]]
- [[Mutants]]
- [[boundsMat]]

---

## Output

- [[MutantPopulation]]

---

## Functions

- [[MutantansExtractor]]
- [[MutateParameters]]

---

## Called by

- [[MutationTimes]]
