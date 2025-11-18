## Description

The `SmoothData_and_FindPeaks` function smooths a chromatogram using Fourier and Savitzky-Golay filters, and then detects peaks based on prominence and distance criteria. It returns both the smoothed data and the indices of the detected peaks.

---
## Key operations

- It smooths the input `Chromatogram` using `SmoothFourier` and `SmoothSavgol`, then it uses `find_peaks` to detect peaks in the smoothed data, and outputs both the smoothed data, and the indices of the peaks.

---
## Code

```python
from SmoothFourier import *
from SmoothSavgol import *
from scipy.signal import find_peaks
def SmoothData_and_FindPeaks(Chromatogram,minPoly=3,stdDistance=1,prominence=1,distance=10,MaxSignals=50):
    smooth_fourier,SavgolWindow=SmoothFourier(PeakChr=Chromatogram,stdDistance=stdDistance,SuggestSavgolWindow=True,MaxSignals=MaxSignals)
    smooth_peaks=SmoothSavgol(PeakChr=smooth_fourier,int_col=1,minWindow=SavgolWindow,minPoly=minPoly)
    peaksMax=find_peaks(smooth_peaks[:,1],prominence=prominence,distance=distance)[0]
    return [smooth_peaks,peaksMax]

```
---

## Parameters

---

## Input

- [[distance]]
- [[MaxSignals]]
- [[prominence]]
- [[stdDistance]]
- [[Chromatogram]]
- [[minPoly]]

---

## Output

- [[peaksMax]]
- [[smooth_peaks]]

---

## Functions

- [[SmoothFourier]]
- [[SmoothSavgol]]

---

## Called by

- [[ToolsGaussianChrom]]
- [[first_round_chromatogram_deconvolution]]
