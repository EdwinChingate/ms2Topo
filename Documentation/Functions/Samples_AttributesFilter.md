## Description

The `Samples_AttributesFilter` function recursively filters a Pandas DataFrame (`SamplesInfDF`) based on specified attributes. It uses `AttributeList` to define the column names, and the `attributeList` to specify the values to filter by, returning a boolean `Filter` array that can be used to select a subset of the dataframe.

---
## Key operations

- The function is recursive, and iterates through the `attributeList` and `AttributeList` variables to filter the `SamplesInfDF` dataframe.
- If the length of `attributeList` is equal to zero, then the `Filter` is returned.
- The `SamplesInfDF` is filtered based on the first element of `AttributeList` and `attributeList`, using the `SamplesInfDF` itself.
- The function then calls itself recursively, with the rest of the elements in `attributeList` and `AttributeList`.

---
## Code

```python
def Samples_AttributesFilter(SamplesInfDF,AttributeList,attributeList,Filter=[]):
    if len(AttributeList)==0:
        return []
    Filter=Samples_AttributesFilter(SamplesInfDF=SamplesInfDF,AttributeList=AttributeList[1:],attributeList=attributeList[1:])
    Attribute=AttributeList[0]
    attribute=attributeList[0]
    Filt=(SamplesInfDF[Attribute]==attribute)
    if len(Filter)>0:
        Filter=Filt&Filter
    else:
        Filter=Filt
    return Filter

```
---

## Parameters

---

## Input

- [[AttributeList]]
- [[Filter]]
- [[attributeList]]
- [[SamplesInfDF]]

---

## Output

- [[]]
- [[Filter]]

---

## Functions


---

## Called by

- [[SamplesNames_common_Attributes]]
