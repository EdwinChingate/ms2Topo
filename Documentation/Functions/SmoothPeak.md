## Description

The `SmoothPeak` function smooths chromatographic data by first applying a Fourier transform using the `SmoothFourier` function, followed by a Savitzky-Golay filter using the `SmoothSavgol` function, and returns the smoothed data in `smooth_savgol`.

---
## Key operations

- It uses `SmoothFourier` to perform an initial smoothing, then uses `SmoothSavgol` to perform a Savitzky-Golay smoothing, and outputs the result in `smooth_savgol`.

---
## Code

```python
from SmoothFourier import *
from SmoothSavgol import *
def SmoothPeak(PeakChr,stdDistance=1,SavgolWindowTimes=2,minPoly=5,int_col=1,RT_col=2):
    smooth_fourier,SavgolWindow_odd=SmoothFourier(PeakChr=PeakChr,stdDistance=stdDistance,SuggestSavgolWindow=True,RT_col=RT_col,int_col=int_col,SavgolWindowTimes=SavgolWindowTimes)
    smooth_savgol=SmoothSavgol(PeakChr=smooth_fourier,int_col=1,minWindow=SavgolWindow_odd,minPoly=minPoly)
    return smooth_savgol

```
---

## Parameters

---

## Input

- [[PeakChr]]
- [[stdDistance]]
- [[RT_col]]
- [[SavgolWindowTimes]]
- [[int_col]]
- [[minPoly]]

---

## Output

- [[smooth_savgol]]

---

## Functions

- [[SmoothFourier]]
- [[SmoothSavgol]]

---

## Called by

- [[ResolvingChromatogram]]
