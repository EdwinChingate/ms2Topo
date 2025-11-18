## Description

The `ChargeDataSet` function loads a mass spectrometry dataset from a specified file into a pyopenms `MSExperiment` object.

---
## Key operations

- The function uses the `MzMLFile().load()` method from pyopenms to load the data from the specified file path.

---
## Code

```python
import os
from pyopenms import *
def ChargeDataSet(DataSetName):
    home=os.getcwd()
    path=home+'/Data'
    DataSet=MSExperiment()
    MzMLFile().load(path+'/'+DataSetName, DataSet)
    return DataSet

```
---

## Parameters

---

## Input

- [[DataSetName]]

---

## Output

- [[DataSet]]

---

## Functions


---

## Called by

