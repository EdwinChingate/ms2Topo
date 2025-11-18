## Description

The `JoiningFeatures` function combines feature tables from different samples within a specified folder into a single NumPy array, `All_FeaturesTable`, also providing the names of the samples, `SamplesNames`.

---
## Key operations

- It reads excel files from the specified `ResultsFolder`. It filters features based on specified m/z and RT ranges (`mz_min`, `mz_max`, `RT_min`, and `RT_max`). Then, it appends all feature tables, adding a sample ID, into a single `All_FeaturesTable`, and extracts the names of the samples into `SamplesNames`.

---
## Code

```python
import pandas as pd
import numpy as np
import os
def JoiningFeatures(ResultsFolder,mz_min=0,mz_max=1200,RT_min=0,RT_max=2000,ToReplace='.mzML.xlsx'):
    SamplesNames=[]
    SamplesList=os.listdir(ResultsFolder)
    SamplesList.sort()
    N_samples=len(SamplesList)
    firstTable=True
    for sample_id in np.arange(N_samples,dtype='int'):   
        features_table=SamplesList[sample_id]
        sample_name=features_table.replace(ToReplace,'')
        SamplesNames.append(sample_name)
        features_table_name=ResultsFolder+'/'+features_table
        FeaturesTableDF=pd.read_excel(features_table_name,index_col=0)
        FeaturesTable=np.array(FeaturesTableDF)
        N_features=len(FeaturesTable[:,0])
        featureLocVec=np.ones(N_features).reshape(-1,1)*sample_id
        FeaturesTable=np.append(FeaturesTable,featureLocVec,axis=1)
        if firstTable:
            All_FeaturesTable=FeaturesTable
            firstTable=False
        else:
            All_FeaturesTable=np.append(All_FeaturesTable,FeaturesTable,axis=0)    
    Filter=(All_FeaturesTable[:,3]>mz_min)&(All_FeaturesTable[:,3]<mz_max)&(All_FeaturesTable[:,2]>RT_min)&(All_FeaturesTable[:,2]<RT_max)
    All_FeaturesTable=All_FeaturesTable[Filter,:]
    return [All_FeaturesTable,SamplesNames]

```
---

## Parameters

---

## Input

- [[ToReplace]]
- [[RT_max]]
- [[RT_min]]
- [[mz_min]]
- [[mz_max]]
- [[ResultsFolder]]

---

## Output

- [[All_FeaturesTable]]
- [[SamplesNames]]

---

## Functions


---

## Called by

- [[Features_ms2_SamplesAligment]]
