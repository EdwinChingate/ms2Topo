## Description

The `Samples_NFeatures_Filter` function filters samples based on feature abundance. It uses the `SamplesNames_common_Attributes` to identify samples with matching attributes, then creates a boolean array to select samples that have more or fewer features than a given threshold.

---
## Key operations

- It filters samples by comparing the number of features in each sample to `Min_Feat`, using the boolean `MoreThan` to determine the comparison.

---
## Code

```python
import numpy as np
from SamplesNames_common_Attributes import *
def Samples_NFeatures_Filter(AlignedSamplesDF,SamplesInfDF,AttributeList,attributeList,Min_Feat,MoreThan=True):
    Index=SamplesNames_common_Attributes(SamplesInfDF=SamplesInfDF,AttributeList=AttributeList,attributeList=attributeList)    
    SamplesDF=AlignedSamplesDF[Index].copy()
    SampLocMat=np.array(SamplesDF.copy())
    SampOnesLoc=np.where(SampLocMat>0)
    SampLocMat[SampOnesLoc]=1
    Filter=sum(SampLocMat.T)>=Min_Feat
    if MoreThan:        
        return [Filter,Index]
    else:
        return [~Filter,Index]

```
---

## Parameters

---

## Input

- [[Min_Feat]]
- [[MoreThan]]
- [[AttributeList]]
- [[attributeList]]
- [[SamplesInfDF]]
- [[AlignedSamplesDF]]

---

## Output

- [[Index]]
- [[Filter]]

---

## Functions

- [[SamplesNames_common_Attributes]]

---

## Called by

- [[RemoveBlankFeatures]]
