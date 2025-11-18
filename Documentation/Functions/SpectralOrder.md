## Description

The `SpectralOrder` function orders the peaks in two input mass spectra, by filtering based on a minimum intensity fraction, and determines the ordered indices for each spectrum. It returns those indices in `L_spec1` and `L_spec2`.

---
## Key operations

- It filters both input spectra based on `min_Int_Frac`, and if `Spectrum_2` has more peaks than `Spectrum_1`, it swaps them. It then determines the indices of the ordered peaks within each spectrum, and stores them in `L_spec1` and `L_spec2`.

---
## Code

```python
def SpectralOrder(Spectrum_1,Spectrum_2,min_Int_Frac=2):
    Spec_1_Filter=Spectrum_1[:,9]>min_Int_Frac
    Spectrum_1=Spectrum_1[Spec_1_Filter,:]
    Spec_2_Filter=Spectrum_2[:,9]>min_Int_Frac
    Spectrum_2=Spectrum_2[Spec_2_Filter,:]    
    L_spec1=len(Spectrum_1[:,0])
    L_spec2=len(Spectrum_2[:,0])
    if L_spec2>L_spec1:
        TempSpec=Spectrum_1.copy()
        Spectrum_1=Spectrum_2.copy()
        Spectrum_2=TempSpec
        L_temp=L_spec1
        L_spec1=L_spec2        
        L_spec2=L_temp
    return [Spectrum_1,Spectrum_2,L_spec1,L_spec2]

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

- [[Spectrum_2]]
- [[L_spec2]]
- [[L_spec1]]
- [[Spectrum_1]]

---

## Functions


---

## Called by

- [[Similarity_2Spectra]]
- [[Cosine_2Spectra]]
