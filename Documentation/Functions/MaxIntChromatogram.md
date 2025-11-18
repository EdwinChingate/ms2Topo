## Description

The `MaxIntChromatogram` function extracts a chromatogram, `Chromatogram`, from a set of raw peaks, `AllRawPeaks`, by filtering based on a defined m/z range (`mz`, `mz_std` and `stdDistance`), and then sorting by retention time.

---
## Key operations

- It defines a m/z range based on the input `mz` and `mz_std`, using `stdDistance` to define the window. It then filters the `AllRawPeaks` to include only those peaks within this range, which are then assigned to the `Chromatogram` variable. Finally it sorts the chromatogram by retention time.

---
## Code

```python
import numpy as np
def MaxIntChromatogram(mz,mz_std,AllRawPeaks,stdDistance=3):
    min_mz=mz-mz_std*stdDistance
    max_mz=mz+mz_std*stdDistance
    mzLoc=np.where((AllRawPeaks[:,0]>min_mz)&(AllRawPeaks[:,0]<max_mz))[0]
    Chromatogram=AllRawPeaks[mzLoc,:]
    Chromatogram=Chromatogram[Chromatogram[:,2].argsort(),:]
    return Chromatogram

```
---

## Parameters

---

## Input

- [[mz]]
- [[stdDistance]]
- [[AllRawPeaks]]
- [[mz_std]]

---

## Output

- [[Chromatogram]]

---

## Functions


---

## Called by

- [[Chrom_ms1Peaks_Summaries]]
- [[AllSubChromatograms]]
- [[PlotChromatogram]]
