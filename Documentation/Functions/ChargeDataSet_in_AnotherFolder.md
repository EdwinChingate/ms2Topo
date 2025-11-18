## Description

This function provides the means to load mass spectrometry data from a specified file path, providing the basis for the other analysis functions.

---
## Key operations

- It takes `DataSetName` and `DataFolder`.
- The function uses `MzMLFile().load()` method from pyopenms to load the data from the specified file path using the provided `DataSetName` and `DataFolder`.
- It outputs the loaded data as a pyopenms `MSExperiment` object.

---
## Code

```python
import os
from pyopenms import *
def ChargeDataSet_in_AnotherFolder(DataSetName,DataFolder):
    DataSet=MSExperiment()
    MzMLFile().load(DataFolder+'/'+DataSetName, DataSet)
    return DataSet

```
---

## Parameters

---

## Input

- [[DataSetName]]
- [[DataFolder]]

---

## Output

- [[DataSet]]

---

## Functions


---

## Called by

- [[RefineFeaturesTable_withChromatogram]]
