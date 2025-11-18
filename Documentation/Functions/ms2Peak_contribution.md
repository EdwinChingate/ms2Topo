## Description

`ms2Peak_contribution` determines the intensity contribution of a peak relative to the total spectral intensity, which is essential for identifying significant fragments in MS/MS spectra.

---
## Key operations

- It filters the `RawSpectrum` to include only data points within the defined m/z range, sums the intensities of these points, and then calculates the percentage of this sum relative to the `TotalInt` of the spectrum.

---
## Code

```python
def ms2Peak_contribution(RawSpectrum,mz,TotalInt,mz_std=2e-3,stdDistance=3):
    min_mz_peak=mz-mz_std*stdDistance
    max_mz_peak=mz+mz_std*stdDistance
    peakFilter=(RawSpectrum[:,0]>min_mz_peak)&(RawSpectrum[:,0]<max_mz_peak)
    PeakData=RawSpectrum[peakFilter,:]            
    PeakInt=sum(PeakData[:,1])    
    relative_contribution=[int(PeakInt/TotalInt*100)]
    return relative_contribution

```
---

## Parameters

---

## Input

- [[mz]]
- [[TotalInt]]
- [[stdDistance]]
- [[RawSpectrum]]
- [[mz_std]]

---

## Output

- [[relative_contribution]]

---

## Functions


---

## Called by

- [[WriteLog]]
