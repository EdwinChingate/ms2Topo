## Description

The `Retrieve_and_Join_ms2_for_feature` function retrieves and combines MS2 spectra for a set of features. It uses the `All_FeaturesTable`, `Feature_module`, `SamplesNames`, `ms2Folder`, and other parameters to locate and load spectra, filtering them based on `min_Int_Frac`.

---
## Key operations

- The function iterates through the features in the `Feature_module`.
- For each feature, the function extracts the sample id and the spectrum id.
- The function constructs a file path to retrieve the ms2 spectrum based on the sample id, and spectrum id, and then loads the spectrum from the file.
- It filters the extracted MS2 spectra based on the `min_Int_Frac` and returns the filtered spectra in the `All_ms2` variable.

---
## Code

```python
import pandas as pd
import numpy as np
import os
def Retrieve_and_Join_ms2_for_feature(All_FeaturesTable,Feature_module,SamplesNames,sample_id_col=16,ms2_spec_id_col=15,ms2Folder='ms2_spectra',ToAdd='mzML',min_Int_Frac=2):
    N_features=len(Feature_module)
    FeatureTable=All_FeaturesTable[Feature_module,:].copy()
    firstSpec=True
    All_ms2=[]
    for feature_id in np.arange(N_features,dtype='int'):
        features_stats=FeatureTable[feature_id,:]
        if sample_id_col>0:
            sample_id=int(features_stats[sample_id_col])
        else:
            sample_id=0
        ms2_spec_id=str(int(features_stats[ms2_spec_id_col]))
        sample_name_id=SamplesNames[sample_id]+ToAdd
        ms2_spectrumLoc=ms2Folder+'/'+sample_name_id+'/'+ms2_spec_id+'.csv'
        ExistSpectrum=os.path.exists(ms2_spectrumLoc)
        if ExistSpectrum:
            ms2_spectrumDF=pd.read_csv(ms2_spectrumLoc,index_col=0)
            ms2_spectrum=np.array(ms2_spectrumDF)
            N_peaks=len(ms2_spectrum[:,0])
            SpectrumLocVec=np.ones(N_peaks).reshape(-1,1)*feature_id
            ms2_spectrum=np.append(ms2_spectrum,SpectrumLocVec,axis=1)
            if firstSpec:
                All_ms2=ms2_spectrum
                firstSpec=False
            else:
                All_ms2=np.append(All_ms2,ms2_spectrum,axis=0)   
    if len(All_ms2)==0:
        return []                
    IntFrac_ms2_filter=All_ms2[:,9]>min_Int_Frac
    All_ms2=All_ms2[IntFrac_ms2_filter,:]    
    return All_ms2

```
---

## Parameters

---

## Input

- [[ms2Folder]]
- [[All_FeaturesTable]]
- [[sample_id_col]]
- [[SamplesNames]]
- [[min_Int_Frac]]
- [[ms2_spec_id_col]]
- [[Feature_module]]
- [[ToAdd]]

---

## Output

- [[]]
- [[All_ms2]]

---

## Functions


---

## Called by

- [[ms2_FeaturesDifferences]]
