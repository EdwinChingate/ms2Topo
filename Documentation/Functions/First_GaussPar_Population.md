## Description

The `First_GaussPar_Population` function generates a population of parameter sets by taking a matrix of parameters, and creating copies where only one of the peaks has its original intensity, and the rest are set to zero.

---
## Key operations

- It creates a list where the first element is the original `ParametersMat`, and then it creates copies of the `ParametersMat` where each copy has one of the peaks' intensities set to its original value, while the rest are set to zero.

---
## Code

```python
import numpy as np
def First_GaussPar_Population(ParametersMat):
    NParameters=len(ParametersMat[:,0])
    Population=[ParametersMat]
    for individual in np.arange(NParameters,dtype='int'):
        ParametersMat_i=ParametersMat.copy()
        ParametersMat_i[:,2]=0
        ParametersMat_i[individual,2]=ParametersMat[individual,2]
        Population.append(ParametersMat_i)
    return Population

```
---

## Parameters

---

## Input

- [[ParametersMat]]

---

## Output

- [[Population]]

---

## Functions


---

## Called by

