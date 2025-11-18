## Description

The `Features_ms2_SamplesAligment` function aligns MS2 features across multiple samples by creating a matrix using `JoiningFeatures` and `ms2_SpectralSimilarityClustering` and storing the intensity of each feature for each sample.

---
## Key operations

- It uses `JoiningFeatures` to combine feature tables from different samples, and then uses `ms2_SpectralSimilarityClustering` to group the features. It then iterates through each feature and fills the matrix with the feature's intensity for each sample.

---
## Code

```python
import numpy as np
import pandas as pd
import os
import datetime
from JoiningFeatures import *
from ms2_SpectralSimilarityClustering import *
def Features_ms2_SamplesAligment(ResultsFolderName,mz_min=254,mz_max=255,RT_min=0,RT_max=2000,RT_tol=30,mz_Tol=0,min_Int_Frac=1,cos_tol=0.9,ToReplace='.mzML.xlsx',ms2Folder='ms2_spectra',ToAdd='mzML',saveAlignedTable=False,name="SamplesAligment"):
    home=os.getcwd()
    ResultsFolder=home+'/'+ResultsFolderName
    All_FeaturesTable,SamplesNames=JoiningFeatures(ResultsFolder=ResultsFolder,mz_min=mz_min,mz_max=mz_max,RT_min=RT_min,RT_max=RT_max,ToReplace=ToReplace)
    Modules=ms2_SpectralSimilarityClustering(SummMS2_raw=All_FeaturesTable,SamplesNames=SamplesNames,mz_col=3,RT_col=2,RT_tol=RT_tol,mz_Tol=mz_Tol,sample_id_col=16,ms2_spec_id_col=15,ms2Folder=ms2Folder,ToAdd=ToAdd,min_Int_Frac=min_Int_Frac,cos_tol=cos_tol)
    N_samples=len(SamplesNames)
    N_Features=len(Modules)
    AlignedSamplesMat=np.zeros((N_Features,N_samples+7))
    AlignedSamples_RT_Mat=np.zeros((N_Features,N_samples+7))
    for feature_id in np.arange(N_Features,dtype='int'):
        Feature_module=Modules[feature_id]
        FeatureTable=All_FeaturesTable[Feature_module,:]
        AlignedSamplesMat[feature_id,0]=np.mean(FeatureTable[:,3])
        AlignedSamplesMat[feature_id,1]=np.mean(FeatureTable[:,4])
        AlignedSamplesMat[feature_id,2]=np.mean(FeatureTable[:,8])
        AlignedSamplesMat[feature_id,3]=np.mean(FeatureTable[:,9])
        AlignedSamplesMat[feature_id,4]=np.mean(FeatureTable[:,2])
        AlignedSamplesMat[feature_id,5]=np.min(FeatureTable[:,12])
        AlignedSamplesMat[feature_id,6]=np.max(FeatureTable[:,13])
        Samples_ids=np.array(FeatureTable[:,16],dtype='int')
        AlignedSamplesMat_loc=Samples_ids+7
        AlignedSamplesMat[feature_id,AlignedSamplesMat_loc]=FeatureTable[:,5]
        AlignedSamples_RT_Mat[feature_id,AlignedSamplesMat_loc]=FeatureTable[:,2]
    AlignedSamples_RT_Mat[:,:7]=AlignedSamplesMat[:,:7].copy()
    AlignedSamplesMat=AlignedSamplesMat[AlignedSamplesMat[:,0].argsort()]    
    AlignedSamples_RT_Mat=AlignedSamples_RT_Mat[AlignedSamples_RT_Mat[:,0].argsort()]   
    Columns=['mz_(Da)','mz_std_(Da)','mz_ConfidenceInterval_(Da)','mz_ConfidenceInterval_(ppm)','RT_(s)','min_RT_(s)','max_RT_(s)']+SamplesNames
    AlignedSamplesDF=pd.DataFrame(AlignedSamplesMat,columns=Columns)
    AlignedSamples_RT_DF=pd.DataFrame(AlignedSamples_RT_Mat,columns=Columns)
    if saveAlignedTable:
        date=datetime.datetime.now()
        string_date=str(date)
        string_date=string_date[:16].replace(':',"_")
        string_date=string_date.replace(' ',"_")
        name=name+"_"+string_date+'.xlsx'
        AlignedSamplesDF.to_excel(name)
        AlignedSamples_RT_DF.to_excel('RT_'+name)
    return [AlignedSamplesDF,AlignedSamples_RT_DF]

```
---

## Parameters

---

## Input

- [[ToReplace]]
- [[RT_max]]
- [[ms2Folder]]
- [[RT_min]]
- [[mz_Tol]]
- [[ResultsFolderName]]
- [[mz_min]]
- [[mz_max]]
- [[cos_tol]]
- [[min_Int_Frac]]
- [[ToAdd]]
- [[RT_tol]]
- [[name]]
- [[saveAlignedTable]]

---

## Output

- [[AlignedSamples_RT_DF]]
- [[AlignedSamplesDF]]

---

## Functions

- [[JoiningFeatures]]
- [[ms2_SpectralSimilarityClustering]]

---

## Called by

