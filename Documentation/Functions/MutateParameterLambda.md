## Description

The `MutateParameterLambda` function returns a lambda function, `MutanteLambda`, that can generate a set of mutated parameters using `MutateParameter`, with boundaries and the number of mutants defined by the input variables.

---
## Key operations

- It defines a lambda function `MutanteLambda` that takes a parameter as an input and uses the `MutateParameter` function to return a set of mutated parameters, using the `boundsVec`, `parameter_std` and `Mutants` parameters to define the boundaries and number of mutated parameters.

---
## Code

```python
from MutateParameter import *
def MutateParameterLambda(boundsVec,parameter_std,Mutants):
    MutanteLambda=lambda parameter: MutateParameter(parameter,boundsVec=boundsVec,parameter_std=parameter_std,Mutants=Mutants)
    return MutanteLambda

```
---

## Parameters

---

## Input

- [[boundsVec]]
- [[parameter_std]]
- [[Mutants]]

---

## Output

- [[MutanteLambda]]

---

## Functions

- [[MutateParameter]]

---

## Called by

- [[MutateParameters]]
