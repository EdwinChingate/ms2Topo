## Description

The `GaussBoundaries` function calculates and returns a matrix, `boundsMat`, that defines the minimum and maximum allowed values for the parameters (RT, standard deviation, and integral) of a Gaussian function, based on the smoothed chromatographic data.

---
## Key operations

- It calculates the minimum and maximum values for retention time (RT) and the integral from the `smooth_peaks` data. It uses these to create a matrix of boundaries (`boundsMat`) for the Gaussian fitting parameters, such as the RT, standard deviation, and the integral of the Gaussian curve.

---
## Code

```python
from scipy import integrate	
import numpy as np
def GaussBoundaries(smooth_peaks,minValue=1e-5):
    RT_vec=smooth_peaks[:,0]
    Int_vec=smooth_peaks[:,1]
    RT_max=np.max(RT_vec)
    RT_min=np.min(RT_vec)
    RT_maxDif=RT_max-RT_min    
    Integral=integrate.simpson(y=Int_vec,x=RT_vec)
    boundsList=[[RT_min,RT_max,RT_maxDif],[minValue,RT_maxDif,RT_maxDif/6],[minValue,Integral,Integral/2]]
    boundsMat=np.array(boundsList)
    return boundsMat

```
---

## Parameters

---

## Input

- [[minValue]]
- [[smooth_peaks]]

---

## Output

- [[boundsMat]]

---

## Functions


---

## Called by

- [[ToolsGaussianChrom]]
- [[GeneticChromatogram]]
