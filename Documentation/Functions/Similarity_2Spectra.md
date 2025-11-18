## Description

The `Similarity_2Spectra` function computes the cosine and Tanimoto similarity scores of two mass spectra, using `SpectralOrder` for peak ordering and `AlignSpectra` for spectrum alignment. The resulting similarity scores are then returned.

---
## Key operations

- It uses `SpectralOrder` to order the peaks of the two input spectra, and `AlignSpectra` to align the spectra. Then it calculates the cosine similarity between the aligned spectra using `Cosine_2VecSpec`.

---
## Code

```python
from SpectralOrder import *
from AlignSpectra import *
from Cosine_2VecSpec import *
def Similarity_2Spectra(Spectrum_1,Spectrum_2,min_Int_Frac=2):
    Spectrum_1,Spectrum_2,L_spec1,L_spec2=SpectralOrder(Spectrum_1=Spectrum_1,Spectrum_2=Spectrum_2,min_Int_Frac=min_Int_Frac)    
    if len(Spectrum_1)==0 or len(Spectrum_2)==0:
        return [0,0]
    AlignedSpecMat,TanimotoSim,AlignedSpec_Inf=AlignSpectra(Spectrum_1=Spectrum_1,Spectrum_2=Spectrum_2,L_spec1=L_spec1,L_spec2=L_spec2)
    Cosine=Cosine_2VecSpec(AlignedSpecMat=AlignedSpecMat)
    return [Cosine,TanimotoSim]

```
---

## Parameters

---

## Input

- [[Spectrum_2]]
- [[Spectrum_1]]
- [[min_Int_Frac]]

---

## Output

- [[Cosine]]
- [[TanimotoSim]]
- [[0]]

---

## Functions

- [[Cosine_2VecSpec]]
- [[AlignSpectra]]
- [[SpectralOrder]]

---

## Called by

- [[GoodNeigbour]]
