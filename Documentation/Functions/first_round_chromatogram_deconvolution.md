## Description

`first_round_chromatogram_deconvolution` performs an initial deconvolution of a chromatogram, by calling `SmoothData_and_FindPeaks` to smooth and find peaks, `RawGaussParameters` to initialize peak parameters, `OverlappingGaussPeaks` to create a matrix of peaks, `AdjustingPeaksContributions` and `UpdatingChromMat` to refine the matrix, and `ParametersFitGaussPeaks` to generate final peak parameters.

---
## Key operations

- The function calls `SmoothData_and_FindPeaks` to smooth the chromatogram and identify peaks, then `RawGaussParameters` to estimate initial Gaussian parameters, then `OverlappingGaussPeaks` to construct the chromatogram matrix. It then calls `AdjustingPeaksContributions` to adjust the contributions of each peak, and `UpdatingChromMat` to refine the matrix, followed by `ParametersFitGaussPeaks` to fit the peaks using the calculated parameters.

---
## Code

```python
from SmoothData_and_FindPeaks import *
from RawGaussParameters import *
from OverlappingGaussPeaks import *
from AdjustingPeaksContributions import *
from UpdatingChromMat import *
from ParametersFitGaussPeaks import *
def first_round_chromatogram_deconvolution(Chromatogram,IntegralFrac=0.1):    
    smooth_peak,peaksMin=SmoothData_and_FindPeaks(Chromatogram=Chromatogram)
    ParametersList=RawGaussParameters(smooth_peak=smooth_peak,peaksMin=peaksMin)
    RT_vec=smooth_peak[:,0]
    ChromatogramMatrix=OverlappingGaussPeaks(RT_vec=RT_vec,ParametersList=ParametersList)
    ContributionsVec=AdjustingPeaksContributions(smooth_peak=smooth_peak,ChromatogramMatrix=ChromatogramMatrix)
    Updated_ChromatogramMatrix=UpdatingChromMat(ChromatogramMatrix,ContributionsVec)
    GaussianParList=ParametersFitGaussPeaks(RT_vec=RT_vec,ChromatogramMatrix=Updated_ChromatogramMatrix,ParametersList=ParametersList,minIntegral=minIntegral)
    return GaussianParList

```
---

## Parameters

---

## Input

- [[IntegralFrac]]
- [[Chromatogram]]

---

## Output

- [[GaussianParList]]

---

## Functions

- [[OverlappingGaussPeaks]]
- [[AdjustingPeaksContributions]]
- [[RawGaussParameters]]
- [[ParametersFitGaussPeaks]]
- [[SmoothData_and_FindPeaks]]
- [[UpdatingChromMat]]

---

## Called by

