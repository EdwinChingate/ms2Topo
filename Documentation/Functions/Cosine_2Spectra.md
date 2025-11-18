## Description

The `Cosine_2Spectra` function calculates the cosine similarity between two mass spectra after aligning and ordering their peaks.

---
## Key operations

- The function first uses `SpectralOrder` to order the peaks in the spectra. Then it uses `AlignSpectra` to align the peaks. Finally, it calls `Cosine_2VecSpec` to calculate the cosine similarity between the aligned spectra.

---
## Code

```python
from SpectralOrder import *
from AlignSpectra import *
from Cosine_2VecSpec import *
def Cosine_2Spectra(Spectrum_1,Spectrum_2):
    Spectrum_1,Spectrum_2,L_spec1,L_spec2=SpectralOrder(Spectrum_1=Spectrum_1,Spectrum_2=Spectrum_2)    
    AlignedSpecMat=AlignSpectra(Spectrum_1=Spectrum_1,Spectrum_2=Spectrum_2,L_spec1=L_spec1,L_spec2=L_spec2)
    Cosine=Cosine_2VecSpec(AlignedSpecMat=AlignedSpecMat)
    return Cosine

```
---

## Parameters

---

## Input

- [[Spectrum_2]]
- [[Spectrum_1]]

---

## Output

- [[Cosine]]

---

## Functions

- [[Cosine_2VecSpec]]
- [[AlignSpectra]]
- [[SpectralOrder]]

---

## Called by

