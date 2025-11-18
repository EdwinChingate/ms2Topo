## Description

The `mz_RT_spectrum_filter` function filters mass spectra based on their RT and m/z values, and it stores a summary of the filtered data.

---
## Key operations

- It checks the MS level of the spectrum, and if it's not MS2, it returns the `SummMS2` without modification.
- It checks if the retention time (RT) and the precursor m/z are within the specified `min_RT`, `max_RT`, `min_mz`, and `max_mz` values.
- It calculates the total intensity and the fraction of the maximum intensity of the spectrum.
- It appends a summary of the spectrum (`MZ`, `RT`, `spectrum_id`, `TotalInt`, and `maxInt_frac`) to `SummMS2`.

---
## Code

```python
import numpy as np
def mz_RT_spectrum_filter(SpectralSignals,SummMS2,min_RT,max_RT,min_mz,max_mz,spectrum_id):
    MSLevel=SpectralSignals.getMSLevel()
    if MSLevel!=2:    
        return SummMS2
    RT=SpectralSignals.getRT()   
    if RT<min_RT or RT>max_RT:
        return SummMS2
    Precursor=SpectralSignals.getPrecursors()[0]
    MZ=Precursor.getMZ()
    if MZ<min_mz or MZ>max_mz:
        return SummMS2
    Spectrum=np.array(SpectralSignals.get_peaks()).T
    maxInt=np.max(Spectrum[:,1])
    TotalInt=np.sum(Spectrum[:,1])    
    AllInt=np.sum(Spectrum[:,1])
    maxInt_frac=maxInt/AllInt
    SummSpec=np.array([MZ,RT,spectrum_id,TotalInt,maxInt_frac])
    SummMS2.append(SummSpec)
    return SummMS2

```
---

## Parameters

---

## Input

- [[SummMS2]]
- [[max_RT]]
- [[spectrum_id]]
- [[SpectralSignals]]
- [[min_mz]]
- [[max_mz]]
- [[min_RT]]

---

## Output

- [[SummMS2]]

---

## Functions


---

## Called by

- [[AllMS2Data]]
