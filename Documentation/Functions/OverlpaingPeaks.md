## Description

The `OverlpaingPeaks` function identifies and stores the indices of overlapping peaks between `Spectrum_1` and `Spectrum_2` in `SharedPeaks_1` and `SharedPeaks_2`, respectively. The function uses the unique m/z values in `UniquePeaks_2` to determine if there is an overlap.

---
## Key operations

- The function iterates through each peak in `Spectrum_1`, and checks if its m/z value is present in `UniquePeaks_2` (a vector of unique m/z values of the peaks from `Spectrum_2`) within a tolerance (not explicitly defined). If a match is found, the index of the peak in `Spectrum_1` is added to `SharedPeaks_1`, and the corresponding index in `Spectrum_2` is added to `SharedPeaks_2`.

---
## Code

```python
import numpy as np
def OverlpaingPeaks(Spectrum_1,Spectrum_2,UniquePeaks_2):
    SharedPeaks_2=[]
    SharedPeaks_1=[]    
    for peak_id in UniquePeaks_2:
        min_mz_peak=Spectrum_2[peak_id,7]
        max_mz_peak=Spectrum_2[peak_id,8]
        OverlapFilter=(Spectrum_1[:,7]>max_mz_peak)|(Spectrum_1[:,8]<min_mz_peak)
        OverlapLoc=np.where(~OverlapFilter)[0]
        if len(Spectrum_1[OverlapLoc,:])==1:
            SharedPeaks_1.append(int(OverlapLoc))
            SharedPeaks_2.append(peak_id)
        elif len(Spectrum_1[OverlapLoc,:])>1:
            OverlapLoc=OverlapLoc[0]
            SharedPeaks_1.append(int(OverlapLoc))
            SharedPeaks_2.append(peak_id)
    UniquePeaks_2=np.delete(UniquePeaks_2,SharedPeaks_2)
    return [SharedPeaks_1,SharedPeaks_2,UniquePeaks_2]    

```
---

## Parameters

---

## Input

- [[Spectrum_2]]
- [[UniquePeaks_2]]
- [[Spectrum_1]]

---

## Output

- [[UniquePeaks_2]]
- [[SharedPeaks_2]]
- [[SharedPeaks_1]]

---

## Functions


---

## Called by

- [[AlignSpectra]]
