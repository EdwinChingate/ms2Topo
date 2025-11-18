## Description

The `Normal_Fit` function fits a Gaussian curve to peak data using the `curve_fit` function, calculates the r-squared value using `r2_Gauss`, and returns the Gaussian parameters and r-squared value as `NormalParameters`.

---
## Key operations

- It unpacks the `PeakData` and `GaussStats` from the input `PeakData_and_Stats`. It uses the `curve_fit` function from `scipy.optimize` to fit a Gaussian curve to the `PeakData`, using the `GaussianPeak` function, and returns the optimized parameters. It uses the `r2_Gauss` function to calculate the r-squared value between the fitted Gaussian curve and the original peak data. The function returns the Gaussian parameters along with the r-squared value as `NormalParameters`.

---
## Code

```python
from scipy.optimize import curve_fit
from GaussianPeak import *
from r2_Gauss import *
def Normal_Fit(PeakData_and_Stats):
    PeakData=PeakData_and_Stats[0]
    GaussStats=PeakData_and_Stats[1]      
    mz=GaussStats[0]
    mz_std=GaussStats[1]
    I_total=GaussStats[4]
    GaussianParameters=list(curve_fit(GaussianPeak, xdata=PeakData[:,0], ydata=PeakData[:,1],p0=[mz,mz_std,I_total])[0])
    r2=r2_Gauss(PeakData,GaussianParameters)
    NormalParameters=GaussianParameters+r2
    return NormalParameters

```
---

## Parameters

---

## Input

- [[PeakData_and_Stats]]

---

## Output

- [[NormalParameters]]

---

## Functions

- [[GaussianPeak]]
- [[r2_Gauss]]

---

## Called by

- [[ms2_peak_stats]]
- [[ms2_features_stats]]
