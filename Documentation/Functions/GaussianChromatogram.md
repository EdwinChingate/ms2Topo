## Description

The `GaussianChromatogram` function generates a chromatogram signal, `Int_model`, by creating and summing a series of overlapping Gaussian peaks defined by the input `ParametersList` and `RT_vec`, using the function `OverlappingGaussPeaks`.

---
## Key operations

- It takes a list of parameters, reshapes it into a matrix, and uses `OverlappingGaussPeaks` to create a matrix of Gaussian peaks. Then, it sums the columns of this matrix to create a single vector representing the combined chromatogram signal (`Int_model`).

---
## Code

```python
from OverlappingGaussPeaks import *
def GaussianChromatogram(RT_vec,*ParametersList):
    NPeaks=int(len(ParametersList)/3)
    ParametersMat=np.array(ParametersList).reshape(NPeaks, 3)
    ChromatogramMatrix=OverlappingGaussPeaks(RT_vec=RT_vec,ParametersMat=ParametersMat)    
    Int_model=sum(ChromatogramMatrix.T)
    return Int_model

```
---

## Parameters

---

## Input

- [[RT_vec]]
- [[ParametersList]]

---

## Output

- [[Int_model]]

---

## Functions

- [[OverlappingGaussPeaks]]

---

## Called by

- [[ResolvingGaussianChromatogram]]
- [[GaussianLambda]]
