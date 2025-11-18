## Description

The function reduces the number of features by grouping similar MS2 spectra into modules, thereby simplifying data for downstream analysis.

---
## Key operations

- It loads MS2 spectra summary data from a file using pandas.
- It filters the spectra by m/z and RT.
- It clusters the spectra using `ms2_SpectralSimilarityClustering`.
- It selects a representative spectrum from each module.

---
## Code

```python
import numpy as np
import pandas as pd
import os
from ms2_SpectralSimilarityClustering import *
def ms2_SpectralRedundancy(SummaryFile,min_RT=0,max_RT=1500,min_mz=0,max_mz=1200,ms2FolderName='ms2_spectra',ToReplace='mzML-ms2Summary.xlsx',mz_col=1,RT_col=2,RT_tol=20,mz_Tol=1e-2,sample_id_col=-1,ms2_spec_id_col=0,ToAdd='mzML',min_Int_Frac=2,cos_tol=0.9):
    home=os.getcwd()
    ms2Folder=home+'/'+ms2FolderName
    SummaryFileName=ms2Folder+'/'+SummaryFile
    SummMS2_raw=np.array(pd.read_excel(SummaryFileName))
    Filter=(SummMS2_raw[:,1]>min_mz)&(SummMS2_raw[:,1]<max_mz)&(SummMS2_raw[:,2]>min_RT)&(SummMS2_raw[:,2]<max_RT)
    SummMS2_raw=SummMS2_raw[Filter,:]
    SampleName=SummaryFile.replace(ToReplace,'')
    Modules=ms2_SpectralSimilarityClustering(SummMS2_raw=SummMS2_raw,SampleName=SampleName,mz_col=mz_col,RT_col=RT_col,RT_tol=RT_tol,mz_Tol=mz_Tol,sample_id_col=sample_id_col,ms2_spec_id_col=ms2_spec_id_col,ms2Folder=ms2Folder,ToAdd=ToAdd,min_Int_Frac=min_Int_Frac,cos_tol=cos_tol)
    N_modules=len(Modules)
    SummMS2=[]
    for mod_p in np.arange(N_modules,dtype='int'):
        mod=Modules[mod_p]
        mod_loc=0
        SummMS2_mod=SummMS2_raw[mod,:].copy()
        min_RT=np.min(SummMS2_mod[:,2])
        max_RT=np.max(SummMS2_mod[:,2])
        N_spec=len(mod)
        if N_spec>1:
            mostInt_ms2Frag=np.max(SummMS2_mod[:,4])
            mostInt_ms2Frag_Filter=SummMS2_mod[:,4]==mostInt_ms2Frag
            mod_loc=int(np.where(mostInt_ms2Frag_Filter)[0])            
        SummMS2_mod=list(SummMS2_mod[mod_loc,:])
        ms2_spec_id=SummMS2_mod[0]
        SummMS2_mod=SummMS2_mod[1:]+[min_RT]+[max_RT]+[N_spec]+[ms2_spec_id]
        SummMS2.append(SummMS2_mod)
    SummMS2=np.array(SummMS2)
    return SummMS2

```
---

## Parameters

---

## Input

- [[max_RT]]
- [[ToReplace]]
- [[mz_col]]
- [[ms2FolderName]]
- [[RT_col]]
- [[mz_Tol]]
- [[sample_id_col]]
- [[min_mz]]
- [[SummaryFile]]
- [[cos_tol]]
- [[min_Int_Frac]]
- [[ms2_spec_id_col]]
- [[max_mz]]
- [[min_RT]]
- [[ToAdd]]
- [[RT_tol]]

---

## Output

- [[SummMS2]]

---

## Functions

- [[ms2_SpectralSimilarityClustering]]

---

## Called by

