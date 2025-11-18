## Description

The `ResolvingGaussianChromatogram` function resolves a chromatogram by fitting gaussian curves to the peaks, after preparing the chromatogram and identifying the parameters to be used.

---
## Key operations

- The function first prepares the chromatogram for gaussian fitting by calling `ToolsGaussianChrom`, it then fits Gaussian curves to the peaks using `curve_fit`, which calls the `GaussianChromatogram` function. If the fitting fails and `ShowErrorChrom` is True, it plots the chromatogram and the parameters.

---
## Code

```python
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from GaussianChromatogram import *
from ToolsGaussianChrom import *
from ShowDF import *
def ResolvingGaussianChromatogram(Chromatogram,RT_col=2,int_col=1,MaxSignals=100,distance=2,ShowErrorChrom=False):
    SChrom,ParametersList,bounds=ToolsGaussianChrom(Chromatogram=Chromatogram,RT_col=RT_col,int_col=int_col,MaxSignals=MaxSignals,distance=distance)
    if len(SChrom)==0:
        return []
    RT_vec=SChrom[:,0]
    Int_vec=SChrom[:,1]
    try:
        GaussianParametersList=list(curve_fit(GaussianChromatogram, xdata=RT_vec, ydata=Int_vec,p0=ParametersList,bounds=bounds)[0])
        NPeaks=int(len(GaussianParametersList)/3)
        GaussianParameters=np.array(GaussianParametersList).reshape(NPeaks, 3)
        GaussianParameters=GaussianParameters[GaussianParameters[:,0].argsort(),:]
        return GaussianParameters
    except:
        if ShowErrorChrom:
            ShowDF(ParametersList)
            plt.plot(Chromatogram[:,RT_col],Chromatogram[:,int_col],'.')
            plt.show()
        return []

```
---

## Parameters

---

## Input

- [[distance]]
- [[ShowErrorChrom]]
- [[MaxSignals]]
- [[RT_col]]
- [[Chromatogram]]
- [[int_col]]

---

## Output

- [[]]
- [[GaussianParameters]]

---

## Functions

- [[ToolsGaussianChrom]]
- [[GaussianChromatogram]]
- [[ShowDF]]

---

## Called by

- [[ResolveFullChromatogram]]
