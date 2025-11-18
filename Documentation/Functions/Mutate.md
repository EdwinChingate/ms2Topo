## Description

The `Mutate` function applies random mutations to a `ParametersMat` based on the `MutationRateVec` and the `boundsMat` using the function `RandomVecGen` to generate random values within the boundaries.

---
## Key operations

- It iterates through each column of the `ParametersMat`, using the `MutationRateVec` to determine the probability of mutation for that parameter, and the `boundsMat` to define the allowed range. It then uses the `RandomVecGen` to generate random values within the specified range, and assigns them to the corresponding column in `ParametersMat`.

---
## Code

```python
from RandomVecGen import *
def Mutate(ParametersMat,MutationRateVec,boundsMat):
    NParameters=len(MutationRateVec)
    NPeaks=len(ParametersMat[:,0])
    for parameter_column in np.arange(NParameters,dtype='int'):
        MutationRate=MutationRateVec[parameter_column]
        bounds=boundsMat[parameter_column,:]
        min_val=bounds[0]
        max_val=bounds[1]
        interval=max_val-min_val
        parameterVec=RandomVecGen(NPeaks)*interval+min_val
        ChoiseVec=RandomVecGen(NPeaks)
        SelectorChoiseVec=ChoiseVec<MutationRate
        #ParametersMat[SelectorChoiseVec,parameter_column]=parameterVec[SelectorChoiseVec]
        ParametersMat[:,parameter_column]=parameterVec
    return ParametersMat

```
---

## Parameters

---

## Input

- [[ParametersMat]]
- [[MutationRateVec]]
- [[boundsMat]]

---

## Output

- [[ParametersMat]]

---

## Functions

- [[RandomVecGen]]

---

## Called by

