## Description

The `MutateParameter` function generates a set of mutated parameter values, `Mutants`, for a single parameter, using a truncated normal distribution constrained by `boundsVec`, with `parameter_std` controlling the magnitude of the mutation.

---
## Key operations

- It uses a truncated normal distribution from `scipy.stats.truncnorm` to generate a set of `Mutants` mutated parameter values, ensuring that the mutated values remain within the range specified by `boundsVec`, using `parameter_std` to control the magnitude of the mutation.

---
## Code

```python
import scipy.stats as stats
def MutateParameter(parameter,boundsVec,parameter_std,Mutants):
    parameter_min=boundsVec[0]
    parameter_max=boundsVec[1]       
    Mutants=stats.truncnorm.rvs((parameter_min-parameter)/parameter_std,(parameter_max-parameter)/parameter_std,loc=parameter,scale=parameter_std,size=Mutants)
    return Mutants

```
---

## Parameters

---

## Input

- [[boundsVec]]
- [[parameter_std]]
- [[parameter]]
- [[Mutants]]

---

## Output

- [[Mutants]]

---

## Functions


---

## Called by

- [[MutateParameterLambda]]
