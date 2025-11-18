## Description

`ToolsGaussianChrom` prepares a chromatogram for Gaussian fitting by smoothing it, identifying peaks, generating initial parameter estimates using  `RawGaussSeed`, `RedistributeSampling` and `GaussBoundaries` for setting boundaries.

---
## Key operations

- This function uses `SmoothData_and_FindPeaks` to smooth the chromatogram and identify peaks. It then uses `RawGaussSeed` to calculate parameters for Gaussian fitting and `RedistributeSampling` to adjust the density of data points. It also uses `GaussBoundaries` to calculate the boundaries of the parameters for Gaussian curve fitting.

---
## Code

```python
import numpy as np
from RawGaussSeed import *
from RedistributeSampling import *
from SmoothData_and_FindPeaks import *
from GaussBoundaries import *
def ToolsGaussianChrom(Chromatogram,RT_col=2,int_col=1,MaxSignals=100,distance=2):
    smooth_peaks,peaksMax=SmoothData_and_FindPeaks(Chromatogram=Chromatogram,MaxSignals=100,distance=2)
    if len(peaksMax)==0:
        return [[],[],[]]
    L=len(smooth_peaks[:,1])
    SChrom=RedistributeSampling(PeakChr=Chromatogram,N_new=L,RT_col=RT_col,int_col=int_col)
    boundsMat=GaussBoundaries(smooth_peaks=smooth_peaks)
    ParametersMat=RawGaussSeed(smooth_peaks=smooth_peaks,peaksMax=peaksMax,boundsMat=boundsMat)
    NPeaks=len(ParametersMat[:,0])
    minVec=np.array([boundsMat[:,0]]*NPeaks)
    maxVec=np.array([boundsMat[:,1]]*NPeaks)
    minList=minVec.flatten()
    maxList=maxVec.flatten()
    bounds=(minList, maxList)
    ParametersList=ParametersMat.flatten()    
    return [SChrom,ParametersList,bounds]

```
---

## Parameters

---

## Input

- [[distance]]
- [[MaxSignals]]
- [[RT_col]]
- [[Chromatogram]]
- [[int_col]]

---

## Output

- [[]]
- [[SChrom]]
- [[bounds]]
- [[ParametersList]]

---

## Functions

- [[RedistributeSampling]]
- [[GaussBoundaries]]
- [[SmoothData_and_FindPeaks]]
- [[RawGaussSeed]]

---

## Called by

- [[ResolvingGaussianChromatogram]]
