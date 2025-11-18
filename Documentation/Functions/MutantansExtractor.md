## Description

The `MutantansExtractor` function extracts a list of mutated parameter matrices, `MutantPopulation`, from a `MutationTensor`.

---
## Key operations

- The function iterates through the `MutationTensor`, appending the parameter matrices to `MutantPopulation`.

---
## Code

```python
import numpy as np
def MutantansExtractor(MutationTensor,Mutants):
    MutantPopulation=[]
    for mutant in np.arange(Mutants):
        ParametersMat_mutant=MutationTensor[mutant,:,:]
        ParametersMat_mutant=ParametersMat_mutant[ParametersMat_mutant[:,0].argsort(),:]        
        MutantPopulation.append(ParametersMat_mutant)
    return MutantPopulation

```
---

## Parameters

---

## Input

- [[MutationTensor]]
- [[Mutants]]

---

## Output

- [[MutantPopulation]]

---

## Functions


---

## Called by

- [[MutantOffspring]]
