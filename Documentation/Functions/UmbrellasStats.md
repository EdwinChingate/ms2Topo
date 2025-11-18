## Description

`UmbrellasStats` calculates statistics for peak umbrellas by calling `WeightGauss` to determine parameters, updating the `PeaksUmbrellaMat` with each peak's calculated parameters and characteristics.

---
## Key operations

- This function iterates through each peak umbrella and uses `WeightGauss` to calculate statistics based on the intensity and retention time values within the umbrella. It then updates the `PeaksUmbrellaMat` with the results.

---
## Code

```python
from WeightGauss import *
def UmbrellasStats(smooth_peaks,PeaksUmbrellaMat,NPeaks,RT_col=0,int_col=1,Points_for_regression=4):
    for pseudo_peak_id in np.arange(NPeaks,dtype='int'):
        EarlyLoc=int(PeaksUmbrellaMat[pseudo_peak_id,1])
        LateLoc=int(PeaksUmbrellaMat[pseudo_peak_id,2])
        MaxRTLoc=int(PeaksUmbrellaMat[pseudo_peak_id,0])   
        RT=smooth_peaks[MaxRTLoc,RT_col]
        RT_vec=smooth_peaks[EarlyLoc:LateLoc,RT_col]
        Int_vec=smooth_peaks[EarlyLoc:LateLoc,int_col]
        Stats=WeightGauss(RT_vec=RT_vec,Int_vec=Int_vec,RT=RT)
        PeaksUmbrellaMat[pseudo_peak_id,3:]=Stats
    return PeaksUmbrellaMat

```
---

## Parameters

---

## Input

- [[Points_for_regression]]
- [[RT_col]]
- [[NPeaks]]
- [[int_col]]
- [[PeaksUmbrellaMat]]
- [[smooth_peaks]]

---

## Output

- [[PeaksUmbrellaMat]]

---

## Functions

- [[WeightGauss]]

---

## Called by

- [[RawGaussCouple]]
- [[RawParametersCut]]
- [[RawGaussParameters]]
- [[RawGaussSeed]]
