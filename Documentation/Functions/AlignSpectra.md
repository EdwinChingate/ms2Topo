## Description

`AlignSpectra` aligns two mass spectra based on their overlapping peaks, using `OverlpaingPeaks` to identify those peaks, and it returns the aligned matrix, the Tanimoto coefficient and the spectra metadata.

---
## Key operations

- It calls the `OverlpaingPeaks` function to find shared and unique peaks between the two spectra, and it creates a matrix of aligned spectra based on those shared peaks. It calculates the Tanimoto coefficient based on the aligned spectra.

---
## Code

```python
import numpy as np
from OverlpaingPeaks import *
def AlignSpectra(Spectrum_1,Spectrum_2,L_spec1,L_spec2,AlignedSpecMat=[]):
    UniquePeaks_1=np.arange(L_spec1)
    UniquePeaks_2=np.arange(L_spec2)
    SharedPeaks_1,SharedPeaks_2,UniquePeaks_2=OverlpaingPeaks(Spectrum_1=Spectrum_1,Spectrum_2=Spectrum_2,UniquePeaks_2=UniquePeaks_2)    
    N_sharedpeaks=len(SharedPeaks_2)
    N_UniquePeaks_2=L_spec2-N_sharedpeaks
    N_AllPeaks=L_spec1+N_UniquePeaks_2    
    if len(AlignedSpecMat)==0:
        AlignedSpecMat=np.zeros((L_spec1,3))  
        AlignedSpecMat[UniquePeaks_1,:2]=Spectrum_1[:,[0,2]].copy()
    else:
        L_spec=len(AlignedSpecMat[:,0])
        NewColumn=np.zeros(L_spec).reshape(-1, 1)
        AlignedSpecMat=np.append(AlignedSpecMat,NewColumn,axis=1)
    AlignedSpecMat[SharedPeaks_1,-1]=Spectrum_2[SharedPeaks_2,2]            
    TanimotoSim=N_sharedpeaks/N_AllPeaks
    if N_UniquePeaks_2>0:
        N_AlignedSpec=len(AlignedSpecMat[0,:])
        UniquePeaksMat=np.zeros((N_UniquePeaks_2,N_AlignedSpec))
        UniquePeaksMat[:,0]=Spectrum_2[UniquePeaks_2,0]
        UniquePeaksMat[:,-1]=Spectrum_2[UniquePeaks_2,2]
        AlignedSpecMat=np.append(AlignedSpecMat,UniquePeaksMat,axis=0)
    AlignedSpec_Inf=np.append(Spectrum_1,Spectrum_2[UniquePeaks_2,:],axis=0)
    return [AlignedSpecMat,TanimotoSim,AlignedSpec_Inf]

```
---

## Parameters

---

## Input

- [[Spectrum_2]]
- [[L_spec2]]
- [[L_spec1]]
- [[Spectrum_1]]
- [[AlignedSpecMat]]

---

## Output

- [[AlignedSpec_Inf]]
- [[TanimotoSim]]
- [[AlignedSpecMat]]

---

## Functions

- [[OverlpaingPeaks]]

---

## Called by

- [[Similarity_2Spectra]]
- [[Cosine_2Spectra]]
