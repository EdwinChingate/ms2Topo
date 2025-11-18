## Description

The `SamplesNames_common_Attributes` function filters a DataFrame of sample information (`SamplesInfDF`) based on given attributes and their values. It uses `Samples_AttributesFilter` to apply the filtering based on the `AttributeList` and `attributeList`, and then returns a Pandas Index object with the indices of the filtered samples.

---
## Key operations

- The function calls `Samples_AttributesFilter` to get a boolean filter based on the `SamplesInfDF`, `AttributeList`, and `attributeList`.
- It extracts the index from the filtered `SamplesInfDF`.

---
## Code

```python
import numpy as np
from Samples_AttributesFilter import *
def SamplesNames_common_Attributes(SamplesInfDF,AttributeList,attributeList):
    if len(AttributeList)!=len(attributeList):
        print('The list of attributes should match its list of values')
        return 0
    Filter=Samples_AttributesFilter(SamplesInfDF=SamplesInfDF,AttributeList=AttributeList,attributeList=attributeList)
    Index=SamplesInfDF[Filter].index
    Index=np.array(Index,dtype='str')
    return Index

```
---

## Parameters

---

## Input

- [[AttributeList]]
- [[attributeList]]
- [[SamplesInfDF]]

---

## Output

- [[Index]]
- [[0]]

---

## Functions

- [[Samples_AttributesFilter]]

---

## Called by

- [[Samples_NFeatures_Filter]]
