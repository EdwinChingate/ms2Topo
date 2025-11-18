## Description

The `SmoothSavgol` function uses a Savitzky-Golay filter to smooth the intensity values of a chromatographic peak, by using a minimum window size and polynomial order, and it returns the smoothed signal in the `smooth_savgol` variable.

---
## Key operations

- It applies a Savitzky-Golay filter to the intensity data (`int_col`) in the input `PeakChr`, using the specified `minWindow` and `minPoly` and returns the result in `smooth_savgol`.

---
## Code

```python
from scipy.signal import savgol_filter
def SmoothSavgol(PeakChr,int_col=1,minWindow=11,minPoly=5):
    smooth_savgol=PeakChr.copy()
    NSpec=len(PeakChr[:,int_col])
    wl=min([int(NSpec/4)*2+1,minWindow])
    poly=min([int(wl/3),minPoly])
    SoftInt=savgol_filter(PeakChr[:,int_col], wl, poly)
    smooth_savgol[:,int_col]=SoftInt
    return smooth_savgol

```
---

## Parameters

---

## Input

- [[PeakChr]]
- [[minWindow]]
- [[int_col]]
- [[minPoly]]

---

## Output

- [[smooth_savgol]]

---

## Functions


---

## Called by

- [[SmoothData_and_FindPeaks]]
- [[SmoothPeak]]
