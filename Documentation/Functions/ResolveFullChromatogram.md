## Description

The `ResolveFullChromatogram` function resolves a chromatogram into individual peaks by splitting it into sub-chromatograms, applying a gaussian deconvolution to each sub-chromatogram, and optionally saving the parameters to an excel file.

---
## Key operations

- The function splits a chromatogram into sub-chromatograms using `AllSubChromatograms`, and then performs gaussian deconvolution using `ResolvingGaussianChromatogram` on each sub-chromatogram. If `SavePeaks` is True, it also saves the Gaussian parameters to an excel file using `GaussianParametersTable`.

---
## Code

```python
import pandas as pd
from AllSubChromatograms import *
from ResolvingGaussianChromatogram import *
from GaussianParametersTable import *
def ResolveFullChromatogram(mz,mz_std,AllRawPeaks,stdDistance=3,RT_tol=5,minSignals=5,SavePeaks=False,mz_name='-mz'):
    ChromatogramList=AllSubChromatograms(mz=mz,mz_std=mz_std,AllRawPeaks=AllRawPeaks,stdDistance=stdDistance,RT_tol=RT_tol,minSignals=minSignals)
    GaussianParametersList=[]
    for Chromatogram in ChromatogramList:
        GaussianParameters=ResolvingGaussianChromatogram(Chromatogram=Chromatogram,RT_col=2,int_col=1,MaxSignals=100,distance=2)
        if len(GaussianParameters)>0:
            GaussianParametersList.append([GaussianParameters,Chromatogram])
    if SavePeaks:
        GaussianParametersDF=GaussianParametersTable(GaussianParametersList=GaussianParametersList)
        GaussianParametersDF.to_excel(str(mz)+mz_name+'.xlsx')
    return GaussianParametersList

```
---

## Parameters

---

## Input

- [[SavePeaks]]
- [[mz]]
- [[stdDistance]]
- [[AllRawPeaks]]
- [[RT_tol]]
- [[mz_std]]
- [[minSignals]]
- [[mz_name]]

---

## Output

- [[GaussianParametersList]]

---

## Functions

- [[ResolvingGaussianChromatogram]]
- [[AllSubChromatograms]]
- [[GaussianParametersTable]]

---

## Called by

- [[ResolveChromPeaks]]
